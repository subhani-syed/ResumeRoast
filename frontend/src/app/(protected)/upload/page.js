"use client";

import { config } from "@/lib/config";
import { useRef, useState, useEffect } from "react";
import { toast } from "sonner";

const API_BASE = config.apiUrl;

function UploadLoader() {
  const [dots, setDots] = useState("");

  useEffect(() => {
    const interval = setInterval(() => {
      setDots((prev) => (prev.length >= 3 ? "" : prev + "."));
    }, 400);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-md flex items-center justify-center z-50">
      <div className="relative bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-10 w-95 text-center shadow-2xl">
        <div className="absolute -inset-px rounded-3xl bg-linear-to-r from-blue-500 via-cyan-500 to-blue-500 opacity-20 blur-xl -z-10" />

        <h2 className="text-xl font-semibold mb-4">
          📤 Uploading your resume{dots}
        </h2>

        <p className="text-gray-400 text-sm mb-6">
          Securely encrypting & preparing your file...
        </p>

        <div className="h-2 w-full bg-white/10 rounded-full overflow-hidden">
          <div className="h-full w-1/2 bg-linear-to-r from-blue-500 to-cyan-500 animate-[loading_1.5s_ease-in-out_infinite]" />
        </div>

        <style jsx>{`
          @keyframes loading {
            0% {
              transform: translateX(-100%);
            }
            50% {
              transform: translateX(0%);
            }
            100% {
              transform: translateX(100%);
            }
          }
        `}</style>
      </div>
    </div>
  );
}

export default function UploadPage() {
  const fileInputRef = useRef(null);
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [resumeCount, setResumeCount] = useState(0);
  const MAX_SIZE_MB = 5;

  useEffect(() => {
    const getResumeInfo = async () => {
      try {
        const resumeInfo = await fetch(`${API_BASE}/resume/upload`, {
          credentials: "include",
        });
        const resumeInfoData = await resumeInfo.json();
        setResumeCount(resumeInfoData.resume_upload_remaining);
      } catch (err) {
        console.error(err);
      }
    };

    getResumeInfo();
  }, []);

  const handleFileChange = (e) => {
    const selected = e.target.files?.[0];
    if (!selected) return;

    if (selected.type !== "application/pdf") {
      toast.error("Only PDF files are allowed.");
      return;
    }

    if (selected.size > MAX_SIZE_MB * 1024 * 1024) {
      toast.error(`File size must be under ${MAX_SIZE_MB}MB.`);
      return;
    }

    setFile(selected);
  };

  const handleUpload = async () => {
    if (resumeCount <= 0) {
      toast.error("You have reached max limit to upload resumes");
      return;
    }

    if (!file) return;

    try {
      setIsUploading(true);

      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(`${API_BASE}/resume/upload`, {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      if (!res.ok) {
        throw new Error("Upload failed");
      }

      const data = await res.json();

      globalThis.location.href = `/resume/${data.resume_id}`;
    } catch (err) {
      console.error(err);
      toast.error("Upload failed. Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <>
      {isUploading && <UploadLoader />}
      <main className="min-h-screen pt-32 px-6 max-w-4xl mx-auto">
        <h1 className="text-3xl font-semibold mb-2">Upload Resume</h1>
        <p className="text-gray-500 dark:text-gray-400 mb-8">
          Upload your resume in PDF format to get roasted 🔥
        </p>

        <div
          onClick={() => fileInputRef.current.click()}
          className="
            cursor-pointer
            border-2 border-dashed
            rounded
            p-12
            text-center
            transition
            hover:border-gray-400 dark:hover:border-gray-500
            border-gray-300 dark:border-white/20
            bg-white dark:bg-neutral-900
          "
        >
          <input
            ref={fileInputRef}
            type="file"
            accept="application/pdf"
            className="hidden"
            onChange={handleFileChange}
          />

          {file ? (
            <>
              <p className="text-lg font-medium mb-2">Selected File:</p>
              <p className="text-sm truncate">{file.name}</p>
              <p className="text-xs text-gray-500 mt-2">
                {(file.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </>
          ) : (
            <>
              <p className="text-lg font-medium mb-2">
                Drag & drop your PDF here
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                or click to browse (Max {MAX_SIZE_MB}MB)
              </p>
            </>
          )}
        </div>

        <div className="mt-8 flex items-center gap-4">
          <button
            onClick={handleUpload}
            disabled={!file || isUploading}
            className="
              px-6 py-2 rounded
              bg-black text-white
              dark:bg-white dark:text-black
              disabled:opacity-50
              hover:opacity-80 transition
            "
          >
            {isUploading ? "Uploading..." : "Upload & Roast 🔥"}
          </button>

          {file && (
            <button
              onClick={() => setFile(null)}
              className="text-sm text-gray-500 hover:underline"
            >
              Remove file
            </button>
          )}
        </div>

        <div className="mt-12 rounded border p-6 bg-white dark:bg-neutral-900 border-gray-200 dark:border-white/10">
          <h3 className="font-medium mb-2">Your Plan</h3>
          <ul className="text-sm text-gray-500 dark:text-gray-400 space-y-1">
            <li>• Max file size: {MAX_SIZE_MB}MB</li>
            <li>• Resumes remaining : {resumeCount}</li>
          </ul>
        </div>
      </main>
    </>
  );
}
