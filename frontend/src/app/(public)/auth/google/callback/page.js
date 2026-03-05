"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function GoogleCallback() {
  const router = useRouter();

  useEffect(() => {
    const validateSession = async () => {
      try {
        const res = await fetch(`/api/me`, {
          credentials: "include",
        });

        if (res.ok) {
          router.replace("/home?welcome=true");
        } else {
          router.replace("/login?error=auth_failed");
        }
      } catch {
        router.replace("/login?error=server_error");
      }
    };

    validateSession();
  }, [router]);

  return <p>Logging you in...</p>;
}
