import { useState } from "react";
import API from "../services/api";

export default function ChatBox() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const askAI = async () => {
    if (!query) return;

    setLoading(true);

    try {
      const res = await API.post("/ask-ai", {
        query: query,
      });

      setAnswer(res.data.answer);
    } catch (err) {
      console.error(err);
      setAnswer("Error getting AI response");
    }

    setLoading(false);
  };

  return (
    <div>
      <h2 className="text-lg font-semibold mb-3">🤖 AI Assistant</h2>

      <textarea
        className="w-full border p-2 rounded"
        rows="3"
        placeholder="Ask something about resumes, jobs, or career..."
        onChange={(e) => setQuery(e.target.value)}
      />

      {/* BUTTON */}
      <button
        onClick={askAI}
        className="mt-2 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition"
      >
        Ask AI
      </button>

      {/* LOADING */}
      {loading && (
        <p className="mt-3 text-gray-500">Thinking...</p>
      )}

      {/* ANSWER BOX */}
      {answer && (
        <div className="mt-4 bg-gray-50 p-4 rounded-xl text-sm text-gray-700 whitespace-pre-line">
          {answer}
        </div>
      )}
    </div>
  );
}