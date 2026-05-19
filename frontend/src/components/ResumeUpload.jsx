import { useState } from "react";
import API from "../services/api";

function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState("");
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first");
      return;
    }

    console.log("Uploading file:", file);

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      // STEP 1 — Upload resume
      const uploadRes = await API.post("/upload-resume", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log("UPLOAD RESPONSE:", uploadRes.data);

      const resumeText = uploadRes.data.text;
      setResponse(resumeText);

      // STEP 2 — Get job matches
      const matchRes = await API.post("/match-jobs", {
        resume_text: resumeText,
      });

      console.log("MATCH RESPONSE:", matchRes.data);

      setJobs(matchRes.data.matches);

    } catch (error) {
      console.log("ERROR:", error.response?.data || error.message);
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Upload Resume</h2>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br /><br />

      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Processing..." : "Upload Resume"}
      </button>

      <hr />

      <h3>Extracted Text:</h3>
      <p>{response}</p>

      <hr />

      <h3>Top Job Matches:</h3>

      {jobs.length === 0 ? (
        <p>No matches yet</p>
      ) : (
        jobs.map((job, index) => (
          <div key={index} style={{
            marginBottom: "15px",
            padding: "10px",
            border: "1px solid #ccc",
            borderRadius: "8px"
          }}>
            <p><b>Job:</b> {job.combined_text}</p>
            <p><b>Score:</b> {job.score.toFixed(3)}</p>
          </div>
        ))
      )}
    </div>
  );
}

export default ResumeUpload;