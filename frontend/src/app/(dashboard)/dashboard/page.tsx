import { currentUser } from "@clerk/nextjs/server"
import { redirect } from "next/navigation"
import { ArrowUpToLine, MessageSquare } from "lucide-react"

export default async function DashboardPage() {
  const user = await currentUser()
  if (!user) redirect("/sign-in")

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Welcome back, {user.firstName || "User"}!</h1>
          <p className="text-muted-foreground mt-1">
            Manage your documents and start chatting with AI
          </p>
        </div>
        <button className="flex items-center gap-2 bg-primary text-primary-foreground px-4 py-2 rounded-md opacity-50 cursor-not-allowed">
          <ArrowUpToLine className="h-4 w-4" />
          Upload Document
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="border rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center">
              <ArrowUpToLine className="h-5 w-5 text-blue-600 dark:text-blue-400" />
            </div>
            <h2 className="text-lg font-semibold">Recent Documents</h2>
          </div>
          <div className="text-center py-12 text-muted-foreground">
            <p>No documents yet</p>
            <p className="text-sm mt-1">Upload your first document to get started</p>
          </div>
        </div>

        <div className="border rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-purple-100 dark:bg-purple-900 rounded-full flex items-center justify-center">
              <MessageSquare className="h-5 w-5 text-purple-600 dark:text-purple-400" />
            </div>
            <h2 className="text-lg font-semibold">Recent Chats</h2>
          </div>
          <div className="text-center py-12 text-muted-foreground">
            <p>No chats yet</p>
            <p className="text-sm mt-1">Start a new chat with your documents</p>
          </div>
        </div>
      </div>

      <div className="border rounded-lg p-6">
        <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="border rounded-md p-4 opacity-50 cursor-not-allowed">
            <h3 className="font-medium">Upload PDF</h3>
            <p className="text-sm text-muted-foreground mt-1">
              Add a new document to your library
            </p>
          </div>
          <div className="border rounded-md p-4 opacity-50 cursor-not-allowed">
            <h3 className="font-medium">New Chat</h3>
            <p className="text-sm text-muted-foreground mt-1">
              Start a conversation with AI
            </p>
          </div>
          <div className="border rounded-md p-4 opacity-50 cursor-not-allowed">
            <h3 className="font-medium">View History</h3>
            <p className="text-sm text-muted-foreground mt-1">
              See all your past conversations
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
