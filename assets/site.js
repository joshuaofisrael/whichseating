(function () {
  var form = document.getElementById("picker-form");
  var select = document.getElementById("venue-picker");
  if (!form || !select) return;
  function go(event) {
    if (!select.value) return;
    event.preventDefault();
    window.location.href = select.value;
  }
  form.addEventListener("submit", go);
  select.addEventListener("change", go);
})();
