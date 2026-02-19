"use client";

import Link from "next/link";

export default function Navbar() {
  return (
    <header className="fixed top-0 w-full z-50">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between rounded border border-white/10 bg-white/5 backdrop-blur-xl shadow-lg px-6 py-3">
          <Link href="/" className="text-xl font-bold tracking-tight">
            Resume
            <span className="bg-linear-to-r from-blue-500 to-cyan-500 bg-clip-text text-transparent">
              Roast
            </span>
          </Link>
          <nav className="hidden md:flex items-center gap-8 text-sm text-gray-300">
            <Link href="#features" className="hover:text-white transition">
              Features
            </Link>
            <Link href="#reviews" className="hover:text-white transition">
              Reviews
            </Link>
            <Link href="#faq" className="hover:text-white transition">
              FAQ
            </Link>
            <Link href="/privacy" className="hover:text-white transition">
              How It Works
            </Link>
            <Link
              href="/home"
              className="px-6 py-2 rounded bg-linear-to-r from-blue-500 to-cyan-500 text-sm font-semibold hover:opacity-90 transition"
            >
              Get Started
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
}
