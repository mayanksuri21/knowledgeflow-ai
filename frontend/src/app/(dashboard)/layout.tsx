"use client"

import { UserButton } from "@clerk/nextjs"
import { ReactNode } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"

export default function DashboardLayout({
  children,
}: {
  children: ReactNode
}) {
  const pathname = usePathname()

  const navItems = [
    { name: "Dashboard", href: "/dashboard" },
    { name: "Documents", href: "/documents" },
    { name: "Chats", href: "/chat" },
  ]

  return (
    <div className="min-h-screen flex bg-background text-foreground">
      <aside className="w-64 border-r bg-card">
        <div className="p-6 border-b">
          <h2 className="text-xl font-bold tracking-tight">KnowledgeFlow</h2>
        </div>
        <nav className="p-4 space-y-2">
          {navItems.map((item) => {
            const isActive = pathname.startsWith(item.href)
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`block px-3 py-2 rounded-md font-medium transition-colors ${
                  isActive
                    ? "bg-primary text-primary-foreground shadow-sm"
                    : "hover:bg-muted text-muted-foreground hover:text-foreground"
                }`}
              >
                {item.name}
              </Link>
            )
          })}
        </nav>
      </aside>
      <main className="flex-1 flex flex-col">
        <header className="border-b p-4 flex items-center justify-between bg-card">
          <div></div>
          <UserButton afterSignOutUrl="/" />
        </header>
        <div className="p-6 flex-1 overflow-y-auto">
          {children}
        </div>
      </main>
    </div>
  )
}
