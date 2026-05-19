import { useState } from "react";
import API from "../services/api";

function ChatBox() {
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

    } catch (error) {
      console.error(error);
      setAnswer("Error getting AI response");
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "20px", marginTop: "40px" }}>
      <h2>AI Career Assistant</h2>

      <textarea
        rows="4"
        cols="60"
        placeholder="Ask AI something..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <br /><br />

      <button onClick={askAI}>
        Ask AI
      </button>

      <hr />

      <h3>AI Response:</h3>

      {loading ? (
        <p>Thinking...</p>
      ) : (
        <p>{answer}</p>
      )}
    </div>
  );
}

export default ChatBox;