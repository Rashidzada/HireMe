(function () {
  if (!window.WebSocket) {
    return;
  }
  const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
  const socket = new WebSocket(`${wsScheme}://${window.location.host}/ws/notifications/`);
  const notifCountEl = document.getElementById("notifications-count");
  const msgCountEl = document.getElementById("messages-count");
  const listEl = document.getElementById("notifications-list");

  socket.onmessage = function (event) {
    const data = JSON.parse(event.data || "{}");
    if (notifCountEl && typeof data.unread_notifications !== "undefined") {
      notifCountEl.textContent = data.unread_notifications;
    }
    if (msgCountEl && typeof data.unread_messages !== "undefined") {
      msgCountEl.textContent = data.unread_messages;
    }
    if (listEl && data.verb) {
      const item = document.createElement("li");
      item.innerHTML = `<a class="dropdown-item small" href="${data.target_url || "#"}">${data.actor ? data.actor + " " : ""}${data.verb}</a>`;
      const header = listEl.querySelector(".dropdown-header");
      if (header && header.nextSibling) {
        listEl.insertBefore(item, header.nextSibling);
      } else {
        listEl.appendChild(item);
      }
    }
  };
})();
