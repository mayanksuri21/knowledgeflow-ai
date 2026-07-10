import { UserButton } from "@clerk/nextjs"
import { ReactNode } from "react"

export default function DashboardLayout({
  children,
}: {
  children: ReactNode
}) {
  return (
    <div className="min-h-screen flex">
      <aside className="w-64 border-r bg-background">
        <div className="p-6 border-b">
          <h2 className="text-xl font-bold">KnowledgeFlow</h2>
        </div>
        <nav className="p-4 space-y-2">
          <div className="px-3 py-2 rounded-md bg-muted font-medium">
            Dashboard
          </div>
          <div className="px-3 py-2 rounded-md hover:bg-muted text-muted-foreground">
            Documents
          </div>
          <div className="px-3 py-2 rounded-md hover:bg-muted text-muted-foreground">
            Chats
          </div>
        </nav>
      </aside>
      <main className="flex-1">
        <header className="border-b p-4 flex items-center justify-between">
          <div></div>
          <UserButton afterSignOutUrl="/" />
        </header>
        <div className="p-6">
          {children}
        </div>
      </main>
    </div>
  )
}
