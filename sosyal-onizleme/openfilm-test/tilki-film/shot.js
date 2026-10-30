export const clamp = (x) => Math.max(0, Math.min(1, x));
export const ease = (x) => 1 - Math.pow(1 - clamp(x), 3);
export function shot(build, update, duration) {
  const root = document.createElement("div");
  root.id = "root";
  document.body.appendChild(root);
  document.body.style.cssText = "margin:0;overflow:hidden;font-family:Segoe UI,Arial,sans-serif";
  build(root);
  window.film = { duration, frame(t) { update(t); } };
}
