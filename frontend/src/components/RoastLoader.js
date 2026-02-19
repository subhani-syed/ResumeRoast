"use client";

import { useEffect, useState } from "react";

const messages = [
  "Analyzing structure...",
  "Scanning for buzzwords...",
  "Detecting fluff...",
  "Measuring impact statements...",
  "Consulting recruiter psychology...",
  "Preparing brutal honesty...",
];

export default function RoastLoader() {
  const [currentMessage, setCurrentMessage] = useState(0);
  const [dots, setDots] = useState("");

  useEffect(() => {
    const messageInterval = setInterval(() => {
      setCurrentMessage((prev) => (prev + 1) % messages.length);
    }, 2000);

    const dotInterval = setInterval(() => {
      setDots((prev) => (prev.length >= 3 ? "" : prev + "."));
    }, 400);

    return () => {
      clearInterval(messageInterval);
      clearInterval(dotInterval);
    };
  }, []);

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-md flex items-center justify-center z-50">
      <div className="relative bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-12 w-100 text-center shadow-2xl">

        <div className="absolute -inset-px rounded-3xl bg-linear-to-r from-blue-500 via-cyan-500 to-blue-500 opacity-20 blur-xl animate-pulse -z-10" />

        <h2 className="text-2xl font-bold mb-4">
          🔥 AI is roasting your resume{dots}
        </h2>

        <p className="text-gray-400 transition-opacity duration-500">
          {messages[currentMessage]}
        </p>

        <div className="mt-8 h-2 w-full bg-white/10 rounded-full overflow-hidden">
          <div className="h-full w-1/2 bg-linear-to-r from-blue-500 to-cyan-500 animate-[loading_2s_ease-in-out_infinite]" />
        </div>
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
  );
}
