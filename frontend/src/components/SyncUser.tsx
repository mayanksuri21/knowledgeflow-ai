"use client";

import { useUser } from "@clerk/nextjs";
import { useEffect, useRef } from "react";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function SyncUser() {
  const { user, isLoaded } = useUser();
  const synced = useRef(false);

  useEffect(() => {
    if (!isLoaded || !user || synced.current) return;

    synced.current = true;

    async function syncUser() {
      try {
        await fetch(`${API_URL}/api/v1/auth/sync-user`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            clerk_id: user.id,
            email: user.primaryEmailAddress?.emailAddress,
            full_name: user.fullName,
            profile_image: user.imageUrl,
          }),
        });
      } catch (error) {
        console.error("Failed to sync user:", error);
      }
    }

    syncUser();
  }, [isLoaded, user]);

  return null;
}