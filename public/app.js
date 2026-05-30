// ELIZA chat UI — talks to the Python serverless function in /api/respond.
// The conversation is kept on the client and replayed server-side, so the
// backend stays fully stateless (serverless-friendly).

const els = {
  messages: document.getElementById("messages"),
  form: document.getElementById("composer"),
  input: document.getElementById("input"),
  sendBtn: document.getElementById("sendBtn"),
  resetBtn: document.getElementById("resetBtn"),
  status: document.getElementById("statusText"),
  suggestions: document.getElementById("suggestions"),
  langToggle: document.getElementById("langToggle"),
};

let userMessages = []; // only the user's turns, in order
let language = "de";
let busy = false;
let ended = false;

function addMessage(text, who) {
  const wrap = document.createElement("div");
  wrap.className = `msg ${who}`;
  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = who === "eliza" ? "E" : "Du";
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  wrap.append(avatar, bubble);
  els.messages.appendChild(wrap);
  els.messages.scrollTop = els.messages.scrollHeight;
  return wrap;
}

function showTyping() {
  const wrap = document.createElement("div");
  wrap.className = "msg eliza typing";
  wrap.innerHTML =
    '<div class="avatar">E</div><div class="bubble"><span></span><span></span><span></span></div>';
  els.messages.appendChild(wrap);
  els.messages.scrollTop = els.messages.scrollHeight;
  return wrap;
}

async function api(method, body) {
  const opts = { method, headers: { "Content-Type": "application/json" } };
  if (body) opts.body = JSON.stringify(body);
  const url = method === "GET" ? `/api/respond?lang=${language}` : "/api/respond";
  const res = await fetch(url, opts);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

function setBusy(state) {
  busy = state;
  els.sendBtn.disabled = state;
  els.input.disabled = state || ended;
}

async function sendMessage(text) {
  if (busy || ended) return;
  text = text.trim();
  if (!text) return;

  addMessage(text, "user");
  userMessages.push(text);
  els.input.value = "";
  setBusy(true);

  const typing = showTyping();
  try {
    const data = await api("POST", { messages: userMessages, language });
    // Small delay so the typing indicator reads naturally.
    await new Promise((r) => setTimeout(r, 350 + Math.random() * 350));
    typing.remove();
    addMessage(data.reply, "eliza");
    if (data.quit) {
      ended = true;
      els.status.textContent = "Gespräch beendet — starte ein neues.";
    }
  } catch (e) {
    typing.remove();
    addMessage("Entschuldige, ich konnte den Server nicht erreichen.", "eliza");
    console.error(e);
  } finally {
    setBusy(false);
    if (!ended) els.input.focus();
  }
}

async function startConversation() {
  els.messages.innerHTML = "";
  userMessages = [];
  ended = false;
  setBusy(true);
  els.status.textContent = "ELIZA hört zu …";
  const typing = showTyping();
  try {
    const data = await api("GET");
    typing.remove();
    addMessage(data.reply, "eliza");
  } catch (e) {
    typing.remove();
    addMessage(
      language === "de"
        ? "Guten Tag. Bitte erzähl mir von deinem Problem."
        : "How do you do. Please tell me your problem.",
      "eliza"
    );
    console.error(e);
  } finally {
    setBusy(false);
    els.input.focus();
  }
}

// --- Events ---
els.form.addEventListener("submit", (e) => {
  e.preventDefault();
  sendMessage(els.input.value);
});

els.resetBtn.addEventListener("click", startConversation);

els.suggestions.addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-msg]");
  if (btn) sendMessage(btn.dataset.msg);
});

els.langToggle.addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-lang]");
  if (!btn || btn.dataset.lang === language) return;
  language = btn.dataset.lang;
  [...els.langToggle.children].forEach((b) =>
    b.classList.toggle("active", b === btn)
  );
  els.input.placeholder =
    language === "de"
      ? "Schreib ELIZA, was dich beschäftigt …"
      : "Tell ELIZA what is on your mind …";
  startConversation();
});

startConversation();
