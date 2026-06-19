import ResumeUpload from "../components/ResumeUpload";
import JobMatches from "../components/JobMatches";
import ChatBox from "../components/ChatBox";

import { Github, Linkedin } from "lucide-react";
import { useEffect, useState } from "react";

export default function Dashboard() {
  const [resumeData, setResumeData] = useState(null);

  // FORCE DARK MODE ON LOAD
  useEffect(() => {
    document.documentElement.classList.add("dark");
    localStorage.setItem("theme", "dark");
  }, []);

  return (
    <div className="min-h-screen text-white overflow-hidden bg-black">

      {/* BACKGROUND GLOW */}
      <div className="absolute top-0 left-0 w-72 h-72 bg-blue-600 opacity-20 blur-3xl rounded-full"></div>
      <div className="absolute bottom-0 right-0 w-72 h-72 bg-indigo-600 opacity-20 blur-3xl rounded-full"></div>

      {/* NAVBAR */}
      <nav className="sticky top-0 z-50 backdrop-blur-xl bg-black/60 border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

          <h1 className="text-2xl font-extrabold text-white">
            AI Resume Analyzer
          </h1>

          <div className="flex items-center gap-5">

            {/* GITHUB */}
            <a
              href="https://github.com/"
              target="_blank"
              rel="noreferrer"
              className="text-gray-300 hover:text-white transition"
            >
              <Github size={22} />
            </a>

            {/* LINKEDIN */}
            <a
              href="https://linkedin.com/"
              target="_blank"
              rel="noreferrer"
              className="text-gray-300 hover:text-white transition"
            >
              <Linkedin size={22} />
            </a>

          </div>

        </div>
      </nav>

      {/* HERO */}
      <div className="relative flex flex-col items-center justify-center text-center pt-20 pb-14 px-4">
        <h1 className="text-5xl md:text-7xl font-extrabold text-white">
          🚀 AI Resume Analyzer
        </h1>

        <p className="mt-6 text-xl md:text-2xl text-gray-300 max-w-2xl">
          Upload your resume, discover matching jobs, and chat with AI instantly.
        </p>
      </div>

      {/* MAIN GRID */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8 px-6 pb-12">

        {/* LEFT */}
        <div className="space-y-8">

          <div className="bg-gray-900/70 p-7 rounded-3xl border border-gray-800">
            <h2 className="text-2xl font-bold mb-5 text-white">
              📄 Resume Upload
            </h2>
            <ResumeUpload setResumeData={setResumeData} />
          </div>

          <div className="bg-gray-900/70 p-7 rounded-3xl border border-gray-800">
            <h2 className="text-2xl font-bold mb-5 text-white">
              🎯 Job Matches
            </h2>
            <JobMatches resumeData={resumeData} />
          </div>

        </div>

        {/* RIGHT */}
        <div className="bg-gray-900/70 p-7 rounded-3xl border border-gray-800 h-fit">
          <h2 className="text-2xl font-bold mb-5 text-white">
            🤖 AI Assistant
          </h2>

          <ChatBox />
        </div>

      </div>
    </div>
  );
}