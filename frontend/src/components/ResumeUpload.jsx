import { useState } from "react";
import API from "../services/api";

export default function ResumeUpload({ setResumeData }) {
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [success, setSuccess] = useState(false);

  const upload = async () => {
    if (!file) return;

    setLoading(true);
    setSuccess(false);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await API.post("/upload-resume", formData);

      const extractedText = res.data.text || "";

      setText(extractedText);
      setSuccess(true);

      if (setResumeData) {
        setResumeData(extractedText);
      }
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) setFile(droppedFile);
  };

  return (
    <div className="space-y-4">

      {/* DROP AREA */}
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragActive(true);
        }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition ${
          dragActive ? "border-blue-500 bg-blue-500/10" : "border-gray-500"
        }`}
      >
        <p className="text-gray-300">📄 Drop Resume Here</p>
        <p className="text-gray-500 text-sm">or click to upload</p>

        <input
          type="file"
          className="hidden"
          id="fileInput"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <label htmlFor="fileInput" className="cursor-pointer block mt-2 text-blue-400">
          Browse File
        </label>
      </div>

      {/* FILE NAME */}
      {file && (
        <div className="text-sm text-green-400">
          Selected: {file.name} ✓
        </div>
      )}

      {/* BUTTON */}
      <button
        onClick={upload}
        disabled={!file || loading}
        className={`px-4 py-2 rounded-lg text-white transition ${
          !file || loading
            ? "bg-gray-500 cursor-not-allowed"
            : "bg-blue-600 hover:bg-blue-700"
        }`}
      >
        {loading ? "Uploading..." : "Upload Resume"}
      </button>

      {/* SUCCESS */}
      {success && (
        <div className="text-green-400 text-sm">
          Resume uploaded & extracted successfully ✔
        </div>
      )}
    </div>
  );
}