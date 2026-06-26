import { useState, useRef, useEffect } from "react";
import API from "../services/api";

export default function ChatBox() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const bottomRef = useRef(null);

  // Auto-scroll to latest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  const askAI = async () => {
    if (!query.trim()) return;

    const userMessage = {
      role: "user",
      text: query,
    };

    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);

    try {
      const res = await API.post("/ask-ai", {
        query,
      });

      const aiMessage = {
        role: "ai",
        text: res.data.answer || "No response",
      };

      setMessages((prev) => [...prev, aiMessage]);

    } catch (err) {

      console.error(err);

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: "Something went wrong. Please try again.",
        },
      ]);
    }

    setQuery("");
    setLoading(false);
  };

  // Press Enter to send
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      askAI();
    }
  };

  return (
    <div className="bg-gray-900 rounded-2xl p-5 shadow-xl border border-gray-800">

      {/* HEADER */}
      <div className="mb-4">
        <h2 className="text-xl font-bold text-white">
          🤖 AI Career Assistant
        </h2>

        <p className="text-gray-400 text-sm mt-1">
          Ask about resumes, interviews, careers, or job skills.
        </p>
      </div>

      {/* CHAT WINDOW */}
      <div className="h-80 overflow-y-auto bg-gray-950 rounded-xl p-4 space-y-3">

        {messages.length === 0 && (
          <div className="text-gray-500 text-sm">
            Start chatting with the AI assistant...
          </div>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`max-w-[85%] p-3 rounded-2xl text-sm whitespace-pre-line ${
              msg.role === "user"
                ? "ml-auto bg-blue-600 text-white"
                : "bg-gray-800 text-gray-100"
            }`}
          >
            {msg.text}
          </div>
        ))}

        {loading && (
          <div className="bg-gray-800 text-gray-300 p-3 rounded-2xl w-fit text-sm animate-pulse">
            AI is thinking...
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* INPUT AREA */}
      <div className="mt-4 space-y-3">

        <textarea
          rows="3"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask something about resumes, jobs, interviews..."
          className="w-full rounded-xl bg-gray-800 border border-gray-700 text-white p-3 outline-none focus:ring-2 focus:ring-green-500 resize-none"
        />

        <button
          onClick={askAI}
          disabled={!query.trim() || loading}
          className={`w-full py-3 rounded-xl font-medium transition ${
            !query.trim() || loading
              ? "bg-gray-700 text-gray-400 cursor-not-allowed"
              : "bg-green-600 hover:bg-green-700 text-white"
          }`}
        >
          {loading ? "Thinking..." : "Ask AI"}
        </button>
      </div>
    </div>
  );
}