import ResumeUpload from "../components/ResumeUpload";
import JobMatches from "../components/JobMatches";
import ChatBox from "../components/ChatBox";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50">

      {/* TOP BAR */}
      <div className="bg-white shadow-sm p-4">
        <h1 className="text-2xl font-bold text-gray-800">
          🚀 AI Resume Analyzer
        </h1>
        <p className="text-sm text-gray-500">
          Upload • Match • Ask AI
        </p>
      </div>

      {/* MAIN GRID */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-6">

        {/* LEFT COLUMN */}
        <div className="space-y-6">

          <div className="bg-white p-6 rounded-2xl shadow hover:shadow-md transition">
            <ResumeUpload />
          </div>

          <div className="bg-white p-6 rounded-2xl shadow hover:shadow-md transition">
            <JobMatches />
          </div>

        </div>

        {/* RIGHT COLUMN */}
        <div className="bg-white p-6 rounded-2xl shadow hover:shadow-md transition">
          <ChatBox />
        </div>

      </div>

    </div>
  );
}