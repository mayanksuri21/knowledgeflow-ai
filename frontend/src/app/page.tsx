import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default async function Home() {
  const user = await currentUser();

  if (user) {
    redirect("/dashboard");
  }

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b p-4 flex items-center justify-between">
        <div className="text-xl font-bold">KnowledgeFlow AI</div>
        <div className="flex items-center gap-4">
          <Link href="/sign-in">
            <Button variant="ghost">Sign In</Button>
          </Link>
          <Link href="/sign-up">
            <Button>Get Started</Button>
          </Link>
        </div>
      </header>

      <main className="flex-1 flex flex-col items-center justify-center p-8 text-center">
        <h1 className="text-5xl font-bold mb-4">
          Chat with your documents
        </h1>

        <p className="text-xl text-muted-foreground max-w-2xl mb-8">
          Upload PDFs and get instant answers from AI.
          KnowledgeFlow AI makes your documents interactive.
        </p>

        <Link href="/sign-up">
          <Button size="lg">Try for free</Button>
        </Link>
      </main>
    </div>
  );
}