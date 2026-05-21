import { useState } from "react";
import API from "../services/api";

export default function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  const upload = async () => {
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await API.post("/upload-resume", formData);
      setText(res.data.text);
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div>
      <h2 className="text-lg font-semibold mb-3">📄 Resume Upload</h2>

      <input
        type="file"
        className="mb-3"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button
        onClick={upload}
        disabled={loading}
        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition"
      >
        {loading ? "Uploading..." : "Upload Resume"}
      </button>

      {text && (
        <div className="mt-4 bg-gray-50 p-3 rounded-lg text-sm text-gray-600">
          {text.slice(0, 300)}...
        </div>
      )}
    </div>
  );
}