import { useState } from "react";
import API from "../services/api";
import { motion } from "framer-motion";

export default function JobMatches({ resumeData }) {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [expanded, setExpanded] = useState({});

  const getMatches = async () => {
    if (!resumeData) return;

    setLoading(true);

    try {
      const res = await API.post("/match-jobs", {
        resume_text: resumeData,
      });

      setJobs(res.data.matches || []);
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  const toggle = (index) => {
    setExpanded((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  return (
    <div className="space-y-4">

      {/* BUTTON */}
      <button
        onClick={getMatches}
        disabled={!resumeData || loading}
        className={`px-4 py-2 rounded-lg text-white transition ${
          !resumeData || loading
            ? "bg-gray-500 cursor-not-allowed"
            : "bg-purple-600 hover:bg-purple-700"
        }`}
      >
        {loading ? "Finding Matches..." : "Get Job Matches"}
      </button>

      {/* LOADING */}
      {loading && (
        <p className="text-gray-400 animate-pulse">
          Searching best job matches...
        </p>
      )}

      {/* JOB LIST */}
      <div className="grid gap-4">
        {jobs.map((job, index) => {
          const isOpen = expanded[index];
          const text = job.combined_text || "";

          return (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="border rounded-2xl p-4 bg-white/70 dark:bg-gray-900/60"
            >
              {/* TITLE + SCORE */}
              <div className="flex justify-between items-center">
                <h3 className="font-semibold text-gray-800 dark:text-white">
                  {job.title || `Job Match #${index + 1}`}
                </h3>

                <span className="px-3 py-1 text-sm rounded-full bg-gray-200 dark:bg-gray-800">
                  {(job.score * 100).toFixed(1)}%
                </span>
              </div>

              {/* TEXT */}
              <p className="text-sm mt-2 text-gray-600 dark:text-gray-300">
                {isOpen ? text : text.slice(0, 180) + "..."}
              </p>

              {/* READ MORE */}
              <button
                onClick={() => toggle(index)}
                className="text-blue-500 text-sm mt-2"
              >
                {isOpen ? "Show less" : "Read more"}
              </button>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}