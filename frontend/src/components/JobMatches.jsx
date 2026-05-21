import { useState } from "react";
import API from "../services/api";
import { motion } from "framer-motion";

export default function JobMatches() {
  const [resumeText, setResumeText] = useState("");
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);

  const getMatches = async () => {
    if (!resumeText) return;

    setLoading(true);

    try {
      const res = await API.post("/match-jobs", {
        resume_text: resumeText,
      });

      setJobs(res.data.matches);
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div>
      <h2 className="text-lg font-semibold mb-3">💼 Job Matches</h2>

      {/* INPUT */}
      <textarea
        className="w-full border p-2 rounded mb-2"
        rows="3"
        placeholder="Paste resume text here to get job matches..."
        onChange={(e) => setResumeText(e.target.value)}
      />

      <button
        onClick={getMatches}
        className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition"
      >
        Find Matches
      </button>

      {/* LOADING */}
      {loading && (
        <p className="mt-3 text-gray-500">Finding best jobs...</p>
      )}

      {/* JOB LIST */}
      <div className="grid gap-4 mt-4">
        {jobs.map((job, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
            className="border rounded-2xl p-4 bg-white hover:shadow-lg transition"
          >
            {/* HEADER */}
            <div className="flex justify-between items-center">
              <h3 className="font-semibold text-gray-800">
                Job Match #{index + 1}
              </h3>

              <span
                className={`px-3 py-1 rounded-full text-sm font-medium ${
                  job.score > 0.8
                    ? "bg-green-100 text-green-700"
                    : job.score > 0.5
                    ? "bg-yellow-100 text-yellow-700"
                    : "bg-red-100 text-red-600"
                }`}
              >
                {(job.score * 100).toFixed(1)}%
              </span>
            </div>

            {/* CONTENT */}
            <p className="text-sm text-gray-600 mt-2 line-clamp-3">
              {job.combined_text}
            </p>
          </motion.div>
        ))}
      </div>
    </div>
  );
}