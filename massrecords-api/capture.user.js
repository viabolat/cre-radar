// ==UserScript==
// @name         Mass Land Records Capture (All Districts)
// @namespace    massrecords-api
// @version      2.0
// @description  Send the current masslandrecords.com page to your local capture API — generalized to every registry district hosted on masslandrecords.com, not just Suffolk
// @match        https://www.masslandrecords.com/*/D/Default.aspx*
// @downloadURL  https://raw.githubusercontent.com/viabolat/cre-radar/main/massrecords-api/capture.user.js
// @updateURL    https://raw.githubusercontent.com/viabolat/cre-radar/main/massrecords-api/capture.user.js
// ==/UserScript==

/*
 * This script does NOT automate the site. It only runs inside the tab you
 * are already browsing by hand — it reads the page you're looking at and
 * posts it to a local API for parsing/storage. Install it in Tampermonkey,
 * or paste this file's contents into the page's DevTools console — both
 * work now that the API sends the Private Network Access header Chrome
 * requires for a public page's fetch() to reach http://localhost. Use
 * masslandrecords.com exactly as you normally would: search, page through
 * results, open a document's details. Click the button whenever you want
 * that page saved as structured data.
 *
 * v2.0 change: @match was hardcoded to /Suffolk/D/Default.aspx and fired
 * on no other district. It's now a wildcard covering every district on
 * this domain (Middlesex South, Worcester, Dukes, etc.) — but note some MA
 * registries (Barnstable, Berkshire *, several Bristol/Essex/Worcester
 * North, Franklin, Hampden, Hampshire) run on entirely separate domains,
 * not masslandrecords.com, and this script will not fire there at all.
 * Every captured record/image is now tagged with its district, read
 * straight from the URL path, so records from different districts never
 * collide on shared book/page numbers in the same local database.
 */
(function () {
  "use strict";

  const API_BASE = "http://localhost:8787";

  function currentDistrict() {
    // Path shape: https://www.masslandrecords.com/<District>/D/Default.aspx
    const parts = window.location.pathname.split("/").filter(Boolean);
    return parts.length > 0 ? parts[0] : null;
  }

  const district = currentDistrict();

  const btn = document.createElement("button");
  btn.textContent = `\u{1F4E4} Send to Local API (${district || "unknown district"})`;
  Object.assign(btn.style, {
    position: "fixed",
    top: "8px",
    right: "8px",
    zIndex: 999999,
    padding: "8px 12px",
    background: "#1a5",
    color: "#fff",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    fontSize: "13px",
    boxShadow: "0 2px 6px rgba(0,0,0,.3)",
  });

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
    setTimeout(() => (toast.style.display = "none"), 4000);
  }

  function postIngest(payload) {
    return fetch(`${API_BASE}/ingest`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }).then((res) => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    });
  }

  btn.addEventListener("click", async () => {
    btn.disabled = true;
    btn.textContent = "Sending...";
    try {
      const data = await postIngest({
        html: document.documentElement.outerHTML,
        source_query: document.title,
        district: district,
        source_url: window.location.href,
      });
      showToast(
        `[${district}] Parsed ${data.parsed_rows} row(s) — ${data.inserted} new, ${data.updated} updated` +
          (data.detail_attached ? ", detail attached" : ""),
        false
      );
    } catch (err) {
      showToast(
        `Failed to reach local API at ${API_BASE} — is it running? (${err})`,
        true
      );
    } finally {
      btn.disabled = false;
      btn.textContent = `\u{1F4E4} Send to Local API (${district || "unknown district"})`;
    }
  });

  document.body.appendChild(btn);
  document.body.appendChild(toast);
})();
