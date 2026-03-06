"use client";

import { useState } from "react";
import Link from "next/link";

export default function Navbar({ items = [], rightComponent }) {
  const [open, setOpen] = useState(false);

  return (
    <header className="fixed top-0 w-full z-50">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="rounded border border-white/10 bg-white/5 backdrop-blur-xl shadow-lg px-6 py-3">
          <div className="flex items-center justify-between">
            <Link href="/home" className="text-xl font-bold tracking-tight">
              Resume
              <span className="bg-linear-to-r from-blue-500 to-cyan-500 bg-clip-text text-transparent">
                Roast
              </span>
            </Link>

            <nav className="hidden md:flex items-center gap-8 text-sm text-gray-300">
              {items.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="hover:text-white transition"
                >
                  {item.label}
                </Link>
              ))}
              {rightComponent}
            </nav>

            <button
              onClick={() => setOpen(!open)}
              className="md:hidden text-white"
            >
              ☰
            </button>
          </div>

          <div
            className={`md:hidden overflow-hidden transition-all duration-300 ${
              open ? "max-h-60 mt-4" : "max-h-0"
            }`}
          >
            <nav className="flex flex-col gap-4 text-gray-300 text-sm">
              {items.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setOpen(false)}
                >
                  {item.label}
                </Link>
              ))}
              {rightComponent}
            </nav>
          </div>
        </div>
      </div>
    </header>
  );
}
