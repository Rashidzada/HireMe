(function () {
  const chatRoot = document.getElementById("chat-root");
  if (!chatRoot || !window.WebSocket) {
    return;
  }
  const threadId = chatRoot.dataset.threadId;
  const currentUserId = parseInt(chatRoot.dataset.userId, 10);
  const chatLog = document.getElementById("chat-log");
  const input = document.getElementById("chat-message-input");
  const form = document.getElementById("chat-form");

  const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
  const socket = new WebSocket(`${wsScheme}://${window.location.host}/ws/chat/${threadId}/`);

  if (chatLog) {
    chatLog.scrollTop = chatLog.scrollHeight;
  }

  socket.onmessage = function (event) {
    const data = JSON.parse(event.data || "{}");
    if (!data.body) {
      return;
    }
    const wrapper = document.createElement("div");
    wrapper.className = `d-flex ${data.sender_id === currentUserId ? "justify-content-end" : "justify-content-start"} mb-2`;
    wrapper.innerHTML = `
      <div class="p-2 rounded ${data.sender_id === currentUserId ? "bg-primary text-white" : "bg-white border"}" style="max-width: 75%;">
        <div class="small fw-semibold">${data.sender}</div>
        <div>${data.body}</div>
      </div>`;
    chatLog.appendChild(wrapper);
    chatLog.scrollTop = chatLog.scrollHeight;
  };

  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      const message = input.value.trim();
      if (!message) {
        return;
      }
      socket.send(JSON.stringify({ message: message }));
      input.value = "";
    });
  }
})();
