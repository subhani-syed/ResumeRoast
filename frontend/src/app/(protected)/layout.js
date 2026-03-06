import { redirect } from "next/navigation";
import { cookies } from "next/headers";
import LogoutButton from "@/lib/auth";
import { config } from "@/lib/config";
import Navbar from "@/components/Navbar";

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

  const navItems = [
    { label: "Upload", href: "/upload" },
    { label: "How It Works", href: "/privacy" },
  ];

  if (res.status === 401) {
    redirect("/login?expired=true");
  }

  return (
    <>
      <Navbar items={navItems} rightComponent={<LogoutButton />} />
      {children}
    </>
  );
}
