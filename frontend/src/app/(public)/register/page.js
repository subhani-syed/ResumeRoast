"use client";

import { useState } from "react";
import Link from "next/link";
import { toast } from "sonner";
import { useRouter } from "next/navigation";

const API_BASE = "/api";

export default function SignupPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    if (password !== confirmPassword) {
      toast.error("Passwords do not match.");
      setLoading(false);
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Signup failed");
      }
      toast.success("🎉 Account created. Time to face the truth.");
      router.push("/login");
    } catch (err) {
      console.error(err);
      toast.error(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };
  const handleGoogleRegister = () => {
    globalThis.location.href = `${API_BASE}/auth/google/login`;
  };

  return (
    <main className="min-h-screen bg-black text-white flex items-center justify-center px-6 relative">
      <div className="absolute inset-0 -z-10 bg-linear-to-br from-blue-600/20  to-cyan-500/20 blur-3xl" />

      <div className="w-full max-w-md bg-white/5 backdrop-blur-xl border border-white/10 rounded p-10 shadow-2xl">
        <h1 className="text-3xl font-bold text-center mb-2">
          Create Your Account 🚀
        </h1>
        <p className="text-gray-400 text-center mb-8">
          Start roasting resumes in seconds.
        </p>

        <form onSubmit={handleSubmit} className="space-y-5">
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="michaelscott@dundermifflin.com"
            className="w-full p-4 rounded bg-white/10 border border-white/10 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          />

          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="********"
            className="w-full p-4 rounded bg-white/10 border border-white/10 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          />

          <input
            type="password"
            required
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="w-full p-4 rounded bg-white/10 border border-white/10 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 rounded bg-linear-to-r from-blue-500 to-cyan-500 font-semibold hover:opacity-90 transition"
          >
            {loading ? "Creating Account..." : "Sign Up"}
          </button>
        </form>

        <div className="flex items-center my-6">
          <div className="flex-1 h-px bg-white/10" />
          <span className="px-4 text-xs text-gray-400 uppercase tracking-wider">
            or
          </span>
          <div className="flex-1 h-px bg-white/10" />
        </div>

        <button
          onClick={handleGoogleRegister}
          className="w-full flex items-center justify-center gap-3 py-4 rounded-lg
                   bg-white text-black font-medium
                   hover:bg-gray-100 active:scale-[0.99]
                   transition-all duration-200 shadow-md"
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 48 48"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fill="#EA4335"
              d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.68 2.44 30.2 0 24 0 14.82 0 6.88 5.28 2.76 12.96l7.98 6.2C12.58 13.5 17.86 9.5 24 9.5z"
            />
            <path
              fill="#4285F4"
              d="M46.5 24.5c0-1.63-.15-3.2-.42-4.7H24v9h12.7c-.55 2.96-2.24 5.46-4.77 7.13l7.4 5.75C43.98 37.5 46.5 31.5 46.5 24.5z"
            />
            <path
              fill="#FBBC05"
              d="M10.74 28.16A14.47 14.47 0 019.5 24c0-1.45.25-2.85.7-4.16l-7.98-6.2A23.92 23.92 0 000 24c0 3.84.92 7.46 2.22 10.36l8.52-6.2z"
            />
            <path
              fill="#34A853"
              d="M24 48c6.2 0 11.4-2.05 15.2-5.56l-7.4-5.75c-2.05 1.38-4.67 2.2-7.8 2.2-6.14 0-11.42-4-13.26-9.66l-8.52 6.2C6.88 42.72 14.82 48 24 48z"
            />
          </svg>
          <span>Sign up with Google</span>
        </button>

        <p className="text-gray-400 text-sm text-center mt-6">
          Already have an account?{" "}
          <Link href="/login" className="text-blue-400 hover:underline">
            Login
          </Link>
        </p>
      </div>
    </main>
  );
}
