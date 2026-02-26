"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

export default function NotFound() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div className="relative min-h-screen flex items-center justify-center px-6 bg-white dark:bg-neutral-950 overflow-hidden">
      <div className="absolute -top-50 left-1/2 -translate-x-1/2 w-200 h-100 bg-neutral-300/30 dark:bg-neutral-700/20 blur-3xl rounded-full" />

      <div
        className={`relative max-w-xl w-full text-center transition-all duration-700 ease-out ${
          mounted ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"
        }`}
      >
        <p className="text-6xl font-medium tracking-wide text-neutral-500 dark:text-neutral-400">
          404
        </p>

        <h1 className="mt-4 text-4xl sm:text-5xl font-semibold tracking-tight text-neutral-900 dark:text-white">
          This page doesn’t exist.
        </h1>

        <p className="mt-6 text-base leading-relaxed text-neutral-600 dark:text-neutral-400">
          The page you’re looking for may have been moved, deleted or doesn’t
          exist. Let’s get you back on track.
        </p>
        <div className="mt-10 flex items-center justify-center gap-4">
          <Link
            href="/"
            className="inline-flex items-center justify-center rounded-lg bg-neutral-900 dark:bg-white px-5 py-2.5 text-sm font-medium text-white dark:text-black hover:opacity-90 transition"
          >
            Go back home
          </Link>
        </div>
      </div>
    </div>
  );
}
