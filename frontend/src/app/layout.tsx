import type { Metadata } from "next";
import { ClerkProvider } from "@clerk/nextjs";
import "@/styles/globals.css";
import SyncUser from "@/components/SyncUser";

export const metadata: Metadata = {
  title: "KnowledgeFlow AI",
  description: "AI-powered document assistant",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>
          <SyncUser />
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}