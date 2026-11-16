/* Google Analytics 4 loader. Consent Mode v2 defaults are denied.
   gtag.js is requested only after the visitor accepts. */
(function () {
  var KEY = "whichseating_ga_consent";
  var ID = window.WHICH_GA4_ID || "";

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;

  gtag("consent", "default", {
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
    analytics_storage: "denied",
    functionality_storage: "denied",
    personalization_storage: "denied",
    security_storage: "granted",
    wait_for_update: 500
  });

  function loadGtag() {
    if (!ID || window.__whichGaLoaded) return;
    window.__whichGaLoaded = true;
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(ID);
    document.head.appendChild(s);
    gtag("js", new Date());
    gtag("consent", "update", {
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
      analytics_storage: "granted"
    });
    gtag("config", ID, { anonymize_ip: true });
  }

  function denyGtag() {
    if (!window.__whichGaLoaded) return;
    gtag("consent", "update", {
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
      analytics_storage: "denied"
    });
  }

  function showBanner() {
    if (document.getElementById("cookie-banner")) return;
    var b = document.createElement("div");
    b.id = "cookie-banner";
    b.setAttribute("role", "dialog");
    b.setAttribute("aria-label", "Cookie settings");
    b.innerHTML = '<p>Google Analytics 4 stays off until you accept. <a href="/privacy/#analytics">Privacy</a></p><p><button type="button" class="btn" data-consent="yes">Accept</button><button type="button" class="btn alt" data-consent="no">Decline</button></p>';
    b.addEventListener("click", function (e) {
      var v = e.target.getAttribute && e.target.getAttribute("data-consent");
      if (!v) return;
      try { localStorage.setItem(KEY, v); } catch (err) {}
      if (b.parentNode) b.parentNode.removeChild(b);
      if (v === "yes") loadGtag();
      else denyGtag();
    });
    document.body.appendChild(b);
  }

  function openSettings(e) {
    if (e) e.preventDefault();
    showBanner();
  }

  var link = document.getElementById("cookie-settings");
  if (link) link.addEventListener("click", openSettings);

  var choice = null;
  try { choice = localStorage.getItem(KEY); } catch (err) {}
  if (choice === "yes") loadGtag();
  else if (choice !== "no") showBanner();
})();
