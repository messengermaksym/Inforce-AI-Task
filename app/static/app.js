(function () {
  const chatEl = document.getElementById("chat");
  const placeholderEl = document.getElementById("placeholder");
  const formEl = document.getElementById("form");
  const inputEl = document.getElementById("message-input");
  const sendBtn = document.getElementById("send-btn");
  const costEl = document.getElementById("total-cost");
  const loadingEl = document.getElementById("loading");
  const errorToast = document.getElementById("error-toast");

  let sessionId = null;

  function showError(message) {
    errorToast.textContent = message;
    errorToast.hidden = false;
    setTimeout(function () {
      errorToast.hidden = true;
    }, 5000);
  }

  function setLoading(loading) {
    loadingEl.hidden = !loading;
    sendBtn.disabled = loading;
  }

  function appendMessage(role, content) {
    if (placeholderEl) placeholderEl.remove();
    const div = document.createElement("div");
    div.className = "msg msg-" + (role === "user" ? "user" : "assistant");
    const roleLabel = role === "user" ? "Ви" : "AI";
    div.innerHTML =
      '<span class="msg-role">' +
      escapeHtml(roleLabel) +
      "</span><p class=\"msg-content\">" +
      escapeHtml(content) +
      "</p>";
    chatEl.appendChild(div);
    chatEl.scrollTop = chatEl.scrollHeight;
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  async function ensureSession() {
    if (sessionId) return sessionId;
    const res = await fetch("/sessions", { method: "POST" });
    if (!res.ok) {
      const err = await res.json().catch(function () {
        return { detail: res.statusText };
      });
      throw new Error(err.detail || "Не вдалося створити сесію");
    }
    const data = await res.json();
    sessionId = data.session_id;
    return sessionId;
  }

  formEl.addEventListener("submit", async function (e) {
    e.preventDefault();
    const text = (inputEl.value || "").trim();
    if (!text) return;

    inputEl.value = "";
    appendMessage("user", text);
    setLoading(true);

    try {
      await ensureSession();
      const url =
        "/sessions/" +
        sessionId +
        "/messages?message_text=" +
        encodeURIComponent(text);
      const res = await fetch(url, { method: "POST" });
      const data = await res.json().catch(function () {
        return {};
      });

      if (!res.ok) {
        throw new Error(data.detail || "Помилка запиту: " + res.status);
      }

      appendMessage("assistant", data.answer);
      costEl.textContent = "$" + (data.total_cost || 0).toFixed(8);
    } catch (err) {
      showError(err.message || "Щось пішло не так");
      setLoading(false);
      return;
    }

    setLoading(false);
  });

  (async function init() {
    try {
      await ensureSession();
    } catch (err) {
      showError(err.message || "Не вдалося ініціалізувати сесію");
    }
  })();
})();
