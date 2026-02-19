import { redirect } from "next/navigation";
import { cookies } from "next/headers";
import Link from "next/link";
import LogoutButton from "@/lib/auth";
import { config } from "@/lib/config";

export default async function ProtectedLayout({ children }) {
  const cookieStore = await cookies();
  const cookieHeader = cookieStore
    .getAll()
    .map((cookie) => `${cookie.name}=${cookie.value}`)
    .join("; ");

  const res = await fetch(`${config.apiUrl}/me`, {
    headers: {
      Cookie: cookieHeader,
    },
    cache: "no-store",
  });

  if (res.status === 401) {
    redirect("/login?expired=true");
  }

  return (
    <>
      <header className="fixed top-0 w-full z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between rounded border border-white/10 bg-white/5 backdrop-blur-xl shadow-lg px-6 py-3">
            <Link href="/home" className="text-xl font-bold tracking-tight">
              Resume
              <span className="bg-linear-to-r from-blue-400 to-cyan-500 bg-clip-text text-transparent">
                Roast
              </span>
            </Link>

            <nav className="hidden md:flex items-center gap-8 text-sm text-gray-300">
              <Link href="/upload" className="hover:text-white transition">
                Upload
              </Link>
              <Link href="/privacy" className="hover:text-white transition">
                How It Works
              </Link>
              <LogoutButton />
            </nav>
          </div>
        </div>
      </header>
      {children}
    </>
  );
}
