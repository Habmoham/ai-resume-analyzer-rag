import { useState } from "react";
import API from "../services/api";

export default function ChatBox() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const askAI = async () => {
    if (!query) return;

    const userMessage = { role: "user", text: query };

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
    }

    setQuery("");
    setLoading(false);
  };

  return (
    <div className="space-y-4">

      {/* CHAT WINDOW */}
      <div className="h-64 overflow-y-auto p-3 bg-gray-900/60 rounded-xl space-y-2">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`p-2 rounded-lg text-sm ${
              msg.role === "user"
                ? "bg-blue-600 text-white ml-auto w-fit"
                : "bg-gray-700 text-white w-fit"
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      {/* INPUT */}
      <textarea
        className="w-full p-3 rounded-lg bg-gray-800 text-white border border-gray-700"
        rows="2"
        placeholder="Ask about resumes, jobs, career..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <button
        onClick={askAI}
        disabled={!query || loading}
        className={`px-4 py-2 rounded-lg text-white transition ${
          !query || loading
            ? "bg-gray-500 cursor-not-allowed"
            : "bg-green-600 hover:bg-green-700"
        }`}
      >
        {loading ? "Thinking..." : "Ask AI"}
      </button>
    </div>
  );
}