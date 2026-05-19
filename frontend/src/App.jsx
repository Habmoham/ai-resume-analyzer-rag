import ResumeUpload from "./components/ResumeUpload";
import ChatBox from "./components/ChatBox";

function App() {
  return (
    <div style={{ padding: "20px" }}>
      <h1>AI Resume Analyzer</h1>

      <ResumeUpload />

      <ChatBox />
    </div>
  );
}

export default App;