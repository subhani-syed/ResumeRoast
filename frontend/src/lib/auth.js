"use client";

import { useRouter } from "next/navigation";
import { toast } from "sonner";

export default function LogoutButton() {
  const router = useRouter();

  const handleLogout = async () => {
    await fetch("api/auth/logout", {
      method: "POST",
      credentials: "include",
    });
    toast.success("You’re logged out. See you soon 👋");
    router.push("/login");
    router.refresh();
  };

  return (
    <button
      onClick={handleLogout}
      className="px-5 py-2 rounded-xl border border-white/20 bg-white/10 hover:bg-white/20 transition text-sm font-medium"
    >
      Logout
    </button>
  );
}
