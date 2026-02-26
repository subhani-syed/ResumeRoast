"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Link from "next/link";
import RoastLoader from "@/components/RoastLoader";
import { config } from "@/lib/config";
import { toast } from "sonner";

const API_BASE = config.apiUrl;

export default function RoastPage() {
  const params = useParams();
  const resume_id = params.resume_id;

  const [resume, setResume] = useState(null);
  const [roast, setRoast] = useState(null);
  const [jobId, setJobId] = useState(null);

  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [pollingStatus, setPollingStatus] = useState("idle");

  const [resumeToDelete, setResumeToDelete] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        // Get Resume
        const resumeRes = await fetch(`${API_BASE}/resume/${resume_id}`, {
          credentials: "include",
        });
        if (!resumeRes.ok) {
          if (resumeRes.status === 404) {
            toast.error("Resume not found or has been deleted.");
            router.replace("/home");
            return;
          }

          if (resumeRes.status === 401) {
            toast.error("Please login again.");
            router.replace("/login");
            return;
          }

          throw new Error("Failed to fetch resume");
        }
        const resumeData = await resumeRes.json();
        setResume(resumeData);

        // Get Latest Roast
        const roastRes = await fetch(`${API_BASE}/resume/${resume_id}/roast`, {
          credentials: "include",
        });
        if (!roastRes.ok) throw new Error("Failed to fetch roast");
        const roastData = await roastRes.json();

        if (roastData.roast_text && roastData.roast_text !== "") {
          setRoast(roastData);
          setJobId(roastData.job_id);
          setPollingStatus("completed");
        } else if (roastData.roast_id) {
          setJobId(roastData.roast_id);
          setPollingStatus("polling");
        }
      } catch (err) {
        const status = err?.response?.status;
        toast.error("Something went wrong loading this resume.");

        if (status === 404) {
          toast.error("Resume not found or has been deleted.");
          router.replace("/home");
          return;
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [resume_id]);

  useEffect(() => {
    if (!jobId || pollingStatus !== "polling") return;

    let intervalId;
    let attempts = 0;
    const MAX_ATTEMPTS = 40;

    const pollAPI = async () => {
      try {
        attempts++;

        const response = await fetch(
          `${API_BASE}/resume/${resume_id}/roast/${jobId}`,
          { credentials: "include" },
        );

        if (!response.ok) {
          throw new Error("API request failed");
        }

        const result = await response.json();

        // Check if roast failed
        if (result && result.status === "FAILED") {
          setPollingStatus("failed");
          toast.error("Failed to generate Roast.");
          setPollingStatus("idle");
          if (intervalId) clearInterval(intervalId);
          return;
        }

        // Check if roast is complete
        if (result && result.roast_text && result.roast_text !== "") {
          setRoast(result);
          setPollingStatus("completed");
          if (intervalId) clearInterval(intervalId);
          return;
        }

        // Check max attempts
        if (attempts >= MAX_ATTEMPTS) {
          setPollingStatus("failed");
          toast.error("Roast generation timed out");
          if (intervalId) clearInterval(intervalId);
        }
      } catch (err) {
        setPollingStatus("failed");
        toast.error("Failed to check roast status");
        if (intervalId) clearInterval(intervalId);
      }
    };

    pollAPI();

    intervalId = setInterval(pollAPI, 2000);

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [jobId, resume_id, pollingStatus]);

  const handleGenerateRoast = async () => {
    try {
      setGenerating(true);

      const res = await fetch(`${API_BASE}/resume/${resume_id}/roast`, {
        method: "POST",
        credentials: "include",
      });
      if (!res.ok) throw new Error("Failed to create roast");
      const data = await res.json();
      setJobId(data.job_id);
      setPollingStatus("polling");
    } catch (err) {
      console.error(err);
      toast.error("Failed to generate roast.");
    } finally {
      setGenerating(false);
    }
  };

  const handleDelete = async () => {
    if (!resumeToDelete) return;

    try {
      setLoading(true);

      const res = await fetch(`${API_BASE}/resume/${resumeToDelete}`, {
        method: "DELETE",
        credentials: "include",
      });

      if (!res.ok) throw new Error("Delete failed");

      setResume(null);

      toast.success("Successfully deleted Resume.");
      setResumeToDelete(null);
      router.replace("/home");
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <main className="min-h-screen pt-32 px-6">
        <RoastLoader />
      </main>
    );
  }

  return (
    <main className="min-h-screen pt-24 p-4">
      <div className="max-w-7xl mx-auto mb-4 flex items-center justify-between">
        <Link
          href="/home"
          className="text-sm text-gray-500 hover:scale-105 hover:text-white transition"
        >
          Back
        </Link>
        <h1 className="font-medium truncate">{resume?.filename}</h1>
        <button
          onClick={() => setResumeToDelete(resume_id)}
          className="text-red-500 hover:text-red-600 transition hover:scale-105"
        >
          Delete
        </button>
      </div>

      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="rounded border bg-white dark:bg-neutral-900 border-gray-200 dark:border-white/10 overflow-hidden">
          <div className="p-3 border-b border-gray-200 dark:border-white/10 flex items-center justify-between">
            <p className="text-sm font-medium">Resume Preview</p>
            <a
              href={resume?.download_url}
              target="_blank"
              className="text-xs text-blue-500 hover:underline"
            >
              Open Full PDF
            </a>
          </div>

          <div className="h-[75vh] bg-gray-100 dark:bg-neutral-800">
            <iframe
              src={resume?.download_url}
              className="w-full h-full"
              title="Resume PDF"
            />
          </div>
        </div>

        <div className="rounded border bg-white dark:bg-neutral-900 border-gray-200 dark:border-white/10 overflow-hidden">
          {pollingStatus === "idle" && (
            <div className="h-full flex flex-col items-center justify-center p-8 text-center">
              <h2 className="text-xl font-semibold mb-2">No Roast Yet 😇</h2>
              <p className="text-sm text-gray-500 mb-6 max-w-sm">
                This resume hasn’t been roasted yet. Click below to unleash
                brutal, honest AI feedback.
              </p>

              <button
                onClick={handleGenerateRoast}
                disabled={generating}
                className="px-6 py-3 rounded bg-black text-white dark:bg-white dark:text-black text-sm font-medium hover:opacity-90 disabled:opacity-50"
              >
                {generating
                  ? "Roasting in progress... 🔥"
                  : "Generate Roast 🔥"}
              </button>
            </div>
          )}

          {pollingStatus === "completed" && roast && (
            <>
              <div className="p-4 border-b border-gray-200 dark:border-white/10">
                <h2 className="text-lg font-semibold">🔥 Your Resume Roast</h2>
              </div>

              <div className="p-4 max-h-[75vh] overflow-y-auto">
                <div className="prose dark:prose-invert max-w-none">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {roast.roast_text}
                  </ReactMarkdown>
                </div>
              </div>
              <div className="p-4 border-t border-gray-200 dark:border-white/10">
                <button
                  onClick={handleGenerateRoast}
                  disabled={generating}
                  className="px-4 py-2 rounded bg-black text-white dark:bg-white dark:text-black text-sm disabled:opacity-50"
                >
                  {generating ? "Re-roasting..." : "Roast Again 🔥"}
                </button>
              </div>
            </>
          )}

          {pollingStatus === "polling" && <RoastLoader />}
        </div>
      </div>

      {resumeToDelete && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div className="bg-white dark:bg-neutral-900 rounded-xl p-6 w-full max-w-sm shadow-2xl border dark:border-white/10">
            <h2 className="text-lg font-semibold mb-2">Delete Resume?</h2>
            <p className="text-sm text-gray-500 mb-6">
              This resume will be moved to trash. You can't restore it later.
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
