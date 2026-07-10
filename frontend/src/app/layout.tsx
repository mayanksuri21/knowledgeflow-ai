import type { Metadata } from "next";
import "@/styles/globals.css";

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
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
