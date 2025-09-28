export function showToast(message: string) {
  let el = document.getElementById("rr-toast");
  if (!el) {
    el = document.createElement("div");
    el.id = "rr-toast";
    el.style.position = "fixed";
    el.style.bottom = "16px";
    el.style.right = "16px";
    el.style.zIndex = "9999";
    document.body.appendChild(el);
  }
  const item = document.createElement("div");
  item.textContent = message;
  item.style.background = "#111827";
  item.style.color = "white";
  item.style.padding = "8px 12px";
  item.style.marginTop = "8px";
  item.style.borderRadius = "6px";
  el.appendChild(item);
  setTimeout(() => item.remove(), 3000);
}
