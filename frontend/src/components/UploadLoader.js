"use client";

import { useState } from "react";

export default function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [success, setSuccess] = useState(false);

  const handleFile = async (selectedFile) => {
    setFile(selectedFile);
    setUploading(true);
    setSuccess(false);

    let fakeProgress = 0;
    const interval = setInterval(() => {
      fakeProgress += 10;
      setProgress(fakeProgress);
      if (fakeProgress >= 100) {
        clearInterval(interval);
        setUploading(false);
        setSuccess(true);
      }
    }, 200);
  };

  return (
    <div className="w-full max-w-xl mx-auto">
      <div
        className={`relative border border-white/10 rounded-3xl p-10 text-center bg-white/5 backdrop-blur-xl transition ${
          uploading ? "opacity-80" : ""
        }`}
      >
        <div className="absolute -inset-px rounded-3xl bg-linear-to-r from-blue-500 via-cyan-500 to-blue-500 opacity-20 blur-xl -z-10" />

        {!file && (
          <>
            <h2 className="text-2xl font-bold mb-4">Upload Your Resume 📄</h2>
            <p className="text-gray-400 mb-6">
              Drag & drop your resume or click to browse.
            </p>

            <label className="cursor-pointer inline-block px-6 py-3 rounded-xl bg-linear-to-r from-blue-500 to-cyan-500 font-semibold hover:opacity-90 transition">
              Choose File
              <input
                type="file"
                accept=".pdf,.doc,.docx"
                hidden
                onChange={(e) =>
                  e.target.files && handleFile(e.target.files[0])
                }
              />
            </label>
          </>
        )}

        {file && (
          <div className="space-y-4">
            <p className="text-gray-300 font-medium truncate">{file.name}</p>

            {uploading && (
              <div className="w-full bg-white/10 h-2 rounded-full overflow-hidden">
                <div
                  className="h-full bg-linear-to-r from-blue-500 to-cyan-500 transition-all duration-200"
                  style={{ width: `${progress}%` }}
                />
              </div>
            )}

            {uploading && (
              <p className="text-gray-400 text-sm">Uploading... {progress}%</p>
            )}

            {success && (
              <p className="text-green-400 font-medium">✓ Upload complete</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
