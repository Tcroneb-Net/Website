document.getElementById("chat-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const input = document.getElementById("user-input");
  const message = input.value;
  input.value = "";

  const chatBox = document.getElementById("chat-box");
  chatBox.innerHTML += `<div><strong>You:</strong> ${message}</div>`;

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });
  const data = await res.json();
  chatBox.innerHTML += `<div><strong>AI:</strong> ${data.reply}</div>`;
  chatBox.scrollTop = chatBox.scrollHeight;
});