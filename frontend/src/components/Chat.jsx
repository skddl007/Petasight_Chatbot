import { useEffect, useRef, useState } from "react";
import { logout, sendMessage } from "../api/client";
import MessageBubble from "./MessageBubble";

export default function Chat({ email, onLogout }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const inputRef = useRef(null);
  const logRef = useRef(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  useEffect(() => {
    logRef.current?.scrollTo(0, logRef.current.scrollHeight);
  }, [messages]);

  const canSend = input.trim().length > 0 && !loading;

  async function handleSubmit(e) {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) {
      setError("Please enter a message");
      return;
    }

    setError("");
    setLoading(true);
    const userMessage = { role: "user", content: trimmed };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    try {
      const history = messages.map((m) => ({ role: m.role, content: m.content }));
      const res = await sendMessage(trimmed, history);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: res.reply,
          backgroundColor: res.backgroundColor,
          textColor: res.textColor,
          ruleApplied: res.ruleApplied,
          meta: res.meta,
        },
      ]);
    } catch (err) {
      setError(err.message);
      setMessages((prev) => prev.slice(0, -1));
      setInput(trimmed);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  }

  function handleLogout() {
    logout();
    onLogout();
  }

  return (
    <div className="chat-shell">
      <div className="chat-glow" aria-hidden="true" />

      <div className="chat-container">
        <header className="chat-header">
          <div className="chat-header-brand">
            <span className="brand-mark brand-mark--sm" aria-hidden="true">
              <svg width="18" height="18" viewBox="0 0 22 22" fill="none">
                <circle cx="11" cy="11" r="9" stroke="currentColor" strokeWidth="1.5" />
                <path d="M7 11.5c1 2 2.5 3.2 4 3.2s3-1.2 4-3.2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
              </svg>
            </span>
            <div>
              <h1>Petasight Chat</h1>
              <p className="chat-email">{email}</p>
            </div>
          </div>
          <button type="button" onClick={handleLogout} className="btn btn-ghost btn-sm">
            Sign out
          </button>
        </header>

        <div
          className="message-log"
          ref={logRef}
          role="log"
          aria-live="polite"
          aria-relevant="additions"
        >
          {messages.length === 0 && (
            <div className="chat-empty">
              <p className="chat-empty-title">Start a conversation</p>
              <p className="chat-empty-hint">
                Replies arrive in Arabic (Ibn Sina) with English below. Try a color rule:
              </p>
              <div className="chat-suggestions">
                <button
                  type="button"
                  className="suggestion-chip"
                  onClick={() => setInput("Mumbai 32")}
                >
                  Mumbai 32
                </button>
                <button type="button" className="suggestion-chip" onClick={() => setInput("0.42")}>
                  0.42
                </button>
                <button
                  type="button"
                  className="suggestion-chip"
                  onClick={() => setInput("HELP ME NOW")}
                >
                  HELP ME NOW
                </button>
              </div>
            </div>
          )}
          {messages.map((msg, i) => (
            <MessageBubble key={i} {...msg} />
          ))}
        </div>

        <form onSubmit={handleSubmit} className="chat-form">
          {error && (
            <p className="form-error" role="alert">
              {error}
            </p>
          )}
          <div className="chat-input-row">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => {
                setInput(e.target.value);
                if (error) setError("");
              }}
              placeholder="Type a message…"
              aria-label="Message"
              disabled={loading}
            />
            <button type="submit" className="btn btn-primary" disabled={!canSend} aria-label="Send message">
              {loading ? (
                <span className="btn-spinner" aria-hidden="true" />
              ) : (
                <svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
                  <path
                    d="M16 2L8 10M16 2l-5 14-3-6-6-3 14-5z"
                    stroke="currentColor"
                    strokeWidth="1.5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
