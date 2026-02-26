"use client";

import { config } from "@/lib/config";
import Image from "next/image";
import Link from "next/link";
import { toast } from "sonner";

import { useEffect, useState } from "react";

const API_ENDPOINT = config.apiUrl;

export default function HomePage() {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [resumeToDelete, setResumeToDelete] = useState(null);

  const handleDelete = async () => {
    if (!resumeToDelete) return;

    try {
      setLoading(true);

      const res = await fetch(`${API_ENDPOINT}/resume/${resumeToDelete}`, {
        method: "DELETE",
        credentials: "include",
      });

      if (!res.ok) throw new Error("Delete failed");

      setResumes((prev) => prev.filter((r) => r.id !== resumeToDelete));
      toast.success("Successfully deleted Resume");
      setResumeToDelete(null);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const params = new URLSearchParams(globalThis.location.search);
    if (params.get("welcome") === "true") {
      globalThis.history.replaceState({}, "", "/home");
      setTimeout(() => {
        toast.success("Welcome back. Ready to roast? 🔥");
      }, 100);
    }
  }, []);

  useEffect(() => {
    const fetchResumes = async () => {
      try {
        const res = await fetch(`${API_ENDPOINT}/resume`, {
          credentials: "include",
        });
        if (!res.ok) {
          throw new Error(`Failed to fetch: ${res.status}`);
        }
        const data = await res.json();
        setResumes(data);
      } catch (err) {
        console.error(err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchResumes();
  }, []);

  if (loading) return <div className="p-6">Loading resumes...</div>;
  if (error) return <div className="p-6 text-red-500">Error: {error}</div>;

  return (
    <main className="min-h-screen pt-32 px-6 max-w-7xl mx-auto">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-semibold">Your Resumes</h1>
          <p className="text-sm text-gray-500">
            Click a resume to view and roast 🔥
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {resumes.map((resume) => (
          <div
            key={resume.id}
            className="group rounded border justify-center bg-white dark:bg-neutral-900 border-gray-200 dark:border-white/10 hover:shadow-xl transition overflow-hidden"
          >
            <div className="bg-gray-100 dark:bg-neutral-800 flex items-center justify-center">
              {resume.thumbnail == "None" ? (
                <span className="text-6xl">📄</span>
              ) : (
                <Image
                  src={resume.thumbnail}
                  alt="Resume Thumbnail"
                  className="rounded w-full h-auto"
                  width={400}
                  height={400}
                />
              )}
            </div>

            <div className="p-4">
              <p className="font-medium truncate">{resume.filename}</p>

              <div className="mt-3 flex justify-between">
                <a
                  href={`/resume/${resume.id}`}
                  className="text text-orange-500 hover:scale-105 transition"
                >
                  View
                </a>
                <button
                  onClick={() => setResumeToDelete(resume.id)}
                  className="text-red-500 hover:text-red-600 transition hover:scale-105"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {resumes.length === 0 && (
        <div className="mt-20 text-center">
          <p className="text-gray-500 mb-4">No resumes uploaded yet.</p>
          <Link
            href="/upload"
            className="inline-block px-4 py-2 rounded bg-black text-white dark:bg-white dark:text-black"
          >
            Upload your first resume
          </Link>
        </div>
      )}

      {resumeToDelete && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div className="bg-white dark:bg-neutral-900 rounded-xl p-6 w-full max-w-sm shadow-2xl border dark:border-white/10">
            <h2 className="text-lg font-semibold mb-2">Delete Resume?</h2>
            <p className="text-sm text-gray-500 mb-6">
              This resume will be moved to trash. You can&apos;t restore it
              later.
            </p>

            <div className="flex justify-end gap-3">
              <button
                onClick={() => setResumeToDelete(null)}
                className="px-4 py-2 text-sm rounded border dark:border-white/20"
              >
                Cancel
              </button>

              <button
                onClick={handleDelete}
                disabled={loading}
                className="px-4 py-2 text-sm rounded bg-red-500 text-white hover:bg-red-600 transition disabled:opacity-50"
              >
                {loading ? "Deleting..." : "Delete"}
              </button>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
