// ==UserScript==
// @name         Mass Land Records Image Capture (All Districts)
// @namespace    massrecords-api
// @version      2.1
// @description  Send the scanned document page image(s) shown in the ImageViewerEx.aspx popup to your local capture API — generalized to every registry district hosted on masslandrecords.com, not just Suffolk
// @match        https://www.masslandrecords.com/*/D/ImageViewerEx.aspx*
// @downloadURL  https://raw.githubusercontent.com/viabolat/massrecords-api/main/capture-image.user.js
// @updateURL    https://raw.githubusercontent.com/viabolat/massrecords-api/main/capture-image.user.js
// ==/UserScript==

/*
 * Paste this into the DevTools console of the small ImageViewerEx.aspx popup
 * window (the one that opens when you view a document's scanned image) — not
 * the main search-results tab, which already has its own capture script.
 *
 * It does not automate navigation. It reads the page image your browser has
 * already loaded (same tab, same session cookies) and POSTs the bytes to
 * your local API. "Capture This Page" grabs whatever page is on screen right
 * now. "Capture All Pages" walks Next through every page of the document,
 * capturing each, then stops — you can still page through manually first if
 * you'd rather do it one at a time.
 *
 * v2.0 change: @match was hardcoded to /Suffolk/D/ImageViewerEx.aspx and
 * fired on no other district. It's now a wildcard covering every district
 * on this domain. Some MA registries run on entirely separate domains and
 * this script will not fire there. Every captured image is now tagged with
 * its district (read from the URL path) so book/page numbers from different
 * districts never collide in the same local database.
 */
(function () {
  "use strict";

  const API_BASE = "http://localhost:8787";
  const IMG_ID = "ImageViewer1_docImage";
  const PAGE_LABEL_ID = "ImageViewer1_lblPageNum";
  const NEXT_BTN_ID = "ImageViewer1_BtnNext";

  function currentDistrict() {
    // Path shape: https://www.masslandrecords.com/<District>/D/ImageViewerEx.aspx
    const parts = window.location.pathname.split("/").filter(Boolean);
    return parts.length > 0 ? parts[0] : null;
  }

  const district = currentDistrict();

  function getImg() {
    return document.getElementById(IMG_ID);
  }

  function pageInfo() {
    const label = document.getElementById(PAGE_LABEL_ID);
    if (!label) return { pageNum: null, totalPages: null };
    const m = label.textContent.match(/(\d+)\s*of\s*(\d+)/i);
    return m ? { pageNum: +m[1], totalPages: +m[2] } : { pageNum: null, totalPages: null };
  }

  // The results grid in the opener tab flags whichever row you last acted on
  // with the DataGridSelectedRow class (same class parser.py already treats
  // as a valid result row) — reading it here needs no navigation of our own,
  // just observing state the site already set from your own click.
  //
  // Cell layout isn't fixed: a Name Search grid has 11 cells with separate
  // book (index 3) and page (index 4) columns, but a Book/Page Search grid
  // has only 7 cells with a single combined "Book/Page" column (index 2,
  // e.g. "85256/295") — reading cells[3]/cells[4] there grabs Type Desc. and
  // Town instead and silently sends garbage (mirrors the same two-shape
  // split parser.py's SEARCH_COLUMNS / SEARCH_COLUMNS_BOOK_PAGE already
  // handle server-side).
  function selectedBookPage() {
    try {
      const rows = window.opener && window.opener.document
        ? window.opener.document.querySelectorAll("tr.DataGridSelectedRow")
        : [];
      if (rows.length !== 1) return { book: null, page: null };
      const cells = rows[0].cells;
      if (cells.length >= 11) {
        return {
          book: cells[3] ? cells[3].textContent.trim() : null,
          page: cells[4] ? cells[4].textContent.trim() : null,
        };
      }
      if (cells.length >= 7) {
        const combined = cells[2] ? cells[2].textContent.trim() : "";
        const [book, page] = combined.split("/").map((s) => s.trim());
        return { book: book || null, page: page || null };
      }
      return { book: null, page: null };
    } catch (err) {
      return { book: null, page: null };
    }
  }

  function waitForRealImage(prevSrc, timeoutMs) {
    return new Promise((resolve, reject) => {
      const start = Date.now();
      (function poll() {
        const img = getImg();
        const src = img && img.src;
        if (img && img.complete && src && !src.includes("loading.gif") && src !== prevSrc) {
          resolve(img);
        } else if (Date.now() - start > timeoutMs) {
          reject(new Error("Timed out waiting for the next page image to load"));
        } else {
          setTimeout(poll, 200);
        }
      })();
    });
  }

  function blobToBase64(blob) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result.split(",")[1]);
      reader.onerror = () => reject(new Error("Failed to read image blob"));
      reader.readAsDataURL(blob);
    });
  }

  async function captureCurrentPage() {
    const img = getImg();
    if (!img || !img.src || img.src.includes("loading.gif")) {
      throw new Error("No page image loaded yet — wait for it to render first");
    }
    const res = await fetch(img.src, { credentials: "include" });
    if (!res.ok) throw new Error(`Fetching image failed: HTTP ${res.status}`);
    const blob = await res.blob();
    const base64 = await blobToBase64(blob);
    const { pageNum, totalPages } = pageInfo();
    const { book, page } = selectedBookPage();
    const payload = {
      image_base64: base64,
      content_type: blob.type || "image/png",
      page_num: pageNum,
      total_pages: totalPages,
      viewer_url: window.location.href,
      opener_title:
        (window.opener && window.opener.document && window.opener.document.title) || null,
      book: book,
      page: page,
      district: district,
    };
    const ingestRes = await fetch(`${API_BASE}/ingest-image`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!ingestRes.ok) throw new Error(`Ingest failed: HTTP ${ingestRes.status}`);
    return ingestRes.json();
  }

  async function clickNextAndWait() {
    const before = getImg().src;
    const { pageNum: beforeNum } = pageInfo();
    const btn = document.getElementById(NEXT_BTN_ID);
    if (!btn) throw new Error("Next-page button not found");
    btn.click();
    await waitForRealImage(before, 10000);
    const { pageNum: afterNum } = pageInfo();
    if (afterNum === beforeNum) throw new Error("Page number did not advance after clicking Next");
  }

  const toast = document.createElement("div");
  Object.assign(toast.style, {
    position: "fixed",
    top: "44px",
    right: "8px",
    zIndex: 999999,
    padding: "8px 12px",
    background: "#333",
    color: "#fff",
    borderRadius: "6px",
    fontSize: "12px",
    display: "none",
    maxWidth: "320px",
  });

  function showToast(text, isError) {
    toast.textContent = text;
    toast.style.background = isError ? "#a33" : "#333";
    toast.style.display = "block";
    setTimeout(() => (toast.style.display = "none"), 5000);
  }

  const btn = document.createElement("button");
  btn.textContent = `\u{1F4F7} Capture This Page (${district || "unknown district"})`;
  const allBtn = document.createElement("button");
  allBtn.textContent = "\u{1F4DA} Capture All Pages";

  for (const b of [btn, allBtn]) {
    Object.assign(b.style, {
      position: "fixed",
      zIndex: 999999,
      padding: "6px 10px",
      background: "#15a",
      color: "#fff",
      border: "none",
      borderRadius: "6px",
      cursor: "pointer",
      fontSize: "12px",
      boxShadow: "0 2px 6px rgba(0,0,0,.3)",
    });
  }

  btn.style.top = "8px";
  btn.style.right = "8px";
  allBtn.style.top = "8px";
  allBtn.style.right = "220px";

  btn.addEventListener("click", async () => {
    btn.disabled = true;
    try {
      const data = await captureCurrentPage();
      const link = data.record_id
        ? `, linked to record #${data.record_id}`
        : ", NOT linked (no unique selected row found)";
      showToast(`[${district}] Captured page → image #${data.image_id}${link}`, false);
    } catch (err) {
      showToast(String(err.message || err), true);
    } finally {
      btn.disabled = false;
    }
  });

  allBtn.addEventListener("click", async () => {
    allBtn.disabled = true;
    btn.disabled = true;
    try {
      let { pageNum, totalPages } = pageInfo();
      if (!totalPages) throw new Error("Could not read the page count off this viewer");
      let count = 0;
      for (;;) {
        const data = await captureCurrentPage();
        count++;
        const link = data.record_id ? `linked #${data.record_id}` : "NOT linked";
        showToast(
          `[${district}] Captured page ${pageNum || count} of ${totalPages} → image #${data.image_id} (${link})`,
          false
        );
        ({ pageNum, totalPages } = pageInfo());
        if (pageNum >= totalPages) break;
        await clickNextAndWait();
        ({ pageNum, totalPages } = pageInfo());
      }
      showToast(`Done — captured ${count} page(s)`, false);
    } catch (err) {
      showToast(String(err.message || err), true);
    } finally {
      allBtn.disabled = false;
      btn.disabled = false;
    }
  });

  document.body.appendChild(btn);
  document.body.appendChild(allBtn);
  document.body.appendChild(toast);
})();
