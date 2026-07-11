"use client"

import { useState, useEffect, useRef, Suspense } from "react"
import { useSearchParams } from "next/navigation"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { useApi } from "@/hooks/useApi"
import { Document } from "@/types"
import { 
  MessageSquare, 
  Send, 
  Trash2, 
  Loader2, 
  Bot, 
  User, 
  FileText, 
  Sparkles, 
  AlertCircle,
  FolderOpen
} from "lucide-react"

interface Citation {
  page_number: number
  content: string
}

interface Message {
  role: "user" | "model"
  content: string
  citations?: Citation[]
}

function ChatContent() {
  const searchParams = useSearchParams()
  const initialDocumentId = searchParams.get("documentId")

  const { fetchApi } = useApi()
  const [documents, setDocuments] = useState<Document[]>([])
  const [selectedDocId, setSelectedDocId] = useState<string>("")
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoadingDocs, setIsLoadingDocs] = useState(true)
  const [isSending, setIsSending] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Fetch ready documents
  useEffect(() => {
    async function loadDocuments() {
      try {
        setIsLoadingDocs(true)
        const allDocs = await fetchApi<Document[]>("/api/v1/documents")
        const readyDocs = allDocs.filter(doc => doc.processing_status === "ready")
        setDocuments(readyDocs)
        
        // Auto-select document from search query if it is in readyDocs
        if (initialDocumentId && readyDocs.some(d => d.id === initialDocumentId)) {
          setSelectedDocId(initialDocumentId)
        } else if (readyDocs.length > 0) {
          // Fallback to first ready doc if no initial ID
          setSelectedDocId(readyDocs[0].id)
        }
      } catch (err) {
        console.error("Failed to load documents:", err)
        setError("Failed to load your document library.")
      } finally {
        setIsLoadingDocs(false)
      }
    }
    loadDocuments()
  }, [initialDocumentId])

  // Scroll to bottom when messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, isSending])

  const selectedDocument = documents.find(d => d.id === selectedDocId)

  async function handleSendMessage(e: React.FormEvent) {
    e.preventDefault()
    if (!input.trim() || !selectedDocId || isSending) return

    const userMessage = input.trim()
    setInput("")
    setError(null)
    setMessages(prev => [...prev, { role: "user", content: userMessage }])
    setIsSending(true)

    try {
      const response = await fetchApi<{ answer: string; citations?: Citation[] }>(`/api/v1/chat/${selectedDocId}`, {
        method: "POST",
        body: JSON.stringify({ question: userMessage })
      })

      setMessages(prev => [...prev, { role: "model", content: response.answer, citations: response.citations }])
    } catch (err) {
      console.error("Failed to get chat response:", err)
      setError("Failed to get a response from Gemini. Please try again.")
    } finally {
      setIsSending(false)
    }
  }

  const starterPrompts = [
    "Summarize this document.",
    "What are the main key takeaways?",
    "List the critical points mentioned in this file."
  ]

  const handleStarterPrompt = (prompt: string) => {
    setInput(prompt)
  }

  return (
    <div className="max-w-5xl mx-auto flex flex-col h-[calc(100vh-140px)] border rounded-xl overflow-hidden bg-card/45 backdrop-blur-sm shadow-xl">
      {/* Top Header Controls */}
      <div className="p-4 border-b bg-card flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3 w-full md:w-auto">
          <FolderOpen className="h-5 w-5 text-indigo-500 shrink-0" />
          <span className="font-semibold text-sm text-muted-foreground mr-1">Active Document:</span>
          {isLoadingDocs ? (
            <div className="flex items-center gap-2">
              <Loader2 className="h-4 w-4 animate-spin text-indigo-500" />
              <span className="text-sm text-muted-foreground">Loading library...</span>
            </div>
          ) : documents.length === 0 ? (
            <span className="text-sm font-medium text-destructive">No processed documents found</span>
          ) : (
            <select
              value={selectedDocId}
              onChange={(e) => {
                setSelectedDocId(e.target.value)
                setMessages([])
                setError(null)
              }}
              className="bg-background border border-input rounded-md px-3 py-1.5 text-sm font-medium focus:outline-none focus:ring-1 focus:ring-ring"
            >
              {documents.map((doc) => (
                <option key={doc.id} value={doc.id}>
                  {doc.original_filename}
                </option>
              ))}
            </select>
          )}
        </div>

        {selectedDocument && (
          <div className="flex items-center gap-4 text-xs text-muted-foreground w-full md:w-auto justify-between md:justify-end">
            <div className="flex gap-3">
              <span>Pages: <strong className="text-foreground">{selectedDocument.page_count ?? "-"}</strong></span>
              <span>Words: <strong className="text-foreground">{selectedDocument.word_count ?? "-"}</strong></span>
            </div>
            {messages.length > 0 && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setMessages([])}
                className="h-7 px-2 text-muted-foreground hover:text-destructive flex items-center gap-1.5"
              >
                <Trash2 className="h-3.5 w-3.5" />
                Clear Chat
              </Button>
            )}
          </div>
        )}
      </div>

      {/* Main Conversation Stream */}
      <div className="flex-1 p-6 overflow-y-auto bg-gradient-to-b from-transparent to-muted/10 space-y-4">
        {error && (
          <div className="flex items-center gap-2 bg-destructive/10 text-destructive border border-destructive/20 p-3 rounded-lg text-sm">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <p className="font-medium">{error}</p>
          </div>
        )}

        {documents.length === 0 && !isLoadingDocs ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-8">
            <div className="w-16 h-16 rounded-2xl bg-indigo-50 dark:bg-indigo-950/30 flex items-center justify-center text-indigo-500 mb-4 shadow-inner">
              <FileText className="h-8 w-8" />
            </div>
            <h3 className="text-lg font-semibold tracking-tight text-foreground">No Processed PDFs Available</h3>
            <p className="text-sm text-muted-foreground max-w-sm mt-2 mb-6">
              You must upload a PDF document and successfully process it on the Documents page before you can start chatting.
            </p>
            <Link href="/documents">
              <Button>Go to Documents</Button>
            </Link>
          </div>
        ) : !selectedDocId && !isLoadingDocs ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-8">
            <Loader2 className="h-8 w-8 animate-spin text-indigo-500" />
          </div>
        ) : messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center max-w-lg mx-auto py-10 space-y-6">
            <div className="w-16 h-16 rounded-2xl bg-indigo-500/10 flex items-center justify-center text-indigo-500 shadow-md">
              <Sparkles className="h-8 w-8" />
            </div>
            <div className="text-center space-y-2">
              <h3 className="text-xl font-bold tracking-tight">
                Chat with {selectedDocument?.original_filename}
              </h3>
              <p className="text-sm text-muted-foreground">
                Ask any questions about this document. Gemini will scan the document context and provide precise responses.
              </p>
            </div>
            
            <div className="w-full space-y-2.5 pt-4">
              <span className="text-xs font-semibold text-muted-foreground tracking-wider uppercase block text-center">Suggested prompts</span>
              <div className="grid grid-cols-1 gap-2">
                {starterPrompts.map((prompt, i) => (
                  <button
                    key={i}
                    type="button"
                    onClick={() => handleStarterPrompt(prompt)}
                    className="text-left text-sm px-4 py-3 rounded-lg border bg-card hover:bg-muted/30 hover:border-indigo-400/50 transition duration-200 cursor-pointer"
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex gap-3 ${
                  message.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                {message.role === "model" && (
                  <div className="w-8 h-8 rounded-full bg-indigo-100 dark:bg-indigo-950 flex items-center justify-center text-indigo-650 shrink-0 shadow-sm border border-indigo-200/50">
                    <Bot className="h-4 w-4" />
                  </div>
                )}
                
                <div
                  className={`rounded-2xl px-4 py-3 text-sm shadow-sm whitespace-pre-wrap ${
                    message.role === "user"
                      ? "bg-gradient-to-r from-indigo-600 to-indigo-700 text-white rounded-tr-none max-w-[80%]"
                      : "bg-card border text-foreground rounded-tl-none max-w-[80%]"
                  }`}
                >
                  <div>{message.content}</div>
                  {message.role === "model" && message.citations && message.citations.length > 0 && (
                    <div className="mt-3 pt-2.5 border-t border-indigo-100 dark:border-zinc-800 text-xs text-muted-foreground space-y-1.5">
                      <span className="font-semibold text-indigo-600 dark:text-indigo-400 block">Sources & Citations:</span>
                      <div className="space-y-2">
                        {message.citations.map((citation, idx) => (
                          <div key={idx} className="bg-muted/40 p-2 rounded border border-muted-foreground/10">
                            <span className="font-bold text-foreground block mb-0.5">Page {citation.page_number}</span>
                            <p className="italic leading-relaxed">&quot;{citation.content}&quot;</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {message.role === "user" && (
                  <div className="w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center text-white shrink-0 shadow-sm">
                    <User className="h-4 w-4" />
                  </div>
                )}
              </div>
            ))}

            {isSending && (
              <div className="flex gap-3 justify-start">
                <div className="w-8 h-8 rounded-full bg-indigo-100 dark:bg-indigo-950 flex items-center justify-center text-indigo-650 shrink-0 border border-indigo-200/50">
                  <Bot className="h-4 w-4" />
                </div>
                <div className="bg-card border rounded-2xl rounded-tl-none px-4 py-3 max-w-[80%] flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-indigo-500 animate-bounce" style={{ animationDelay: "0ms" }}></span>
                  <span className="w-2 h-2 rounded-full bg-indigo-500 animate-bounce" style={{ animationDelay: "150ms" }}></span>
                  <span className="w-2 h-2 rounded-full bg-indigo-500 animate-bounce" style={{ animationDelay: "300ms" }}></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Message Form */}
      <div className="p-4 border-t bg-card">
        <form onSubmit={handleSendMessage} className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={!selectedDocId || isSending}
            placeholder={
              selectedDocId 
                ? "Ask a question about the document..." 
                : "Select a document to begin chatting"
            }
            className="flex-1 bg-background border border-input rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-ring disabled:opacity-50"
          />
          <Button 
            type="submit" 
            disabled={!selectedDocId || !input.trim() || isSending}
            className="px-4 py-2.5 flex items-center gap-2 shrink-0 bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm"
          >
            {isSending ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <>
                <Send className="h-4 w-4" />
                <span>Send</span>
              </>
            )}
          </Button>
        </form>
        <p className="text-[10px] text-muted-foreground text-center mt-2.5">
          KnowledgeFlow AI. Answers are synthesized directly from your PDF via Google Gemini.
        </p>
      </div>
    </div>
  )
}

export default function ChatPage() {
  return (
    <Suspense fallback={
      <div className="max-w-5xl mx-auto flex items-center justify-center h-[calc(100vh-140px)] border rounded-xl bg-card/45 backdrop-blur-sm shadow-xl">
        <Loader2 className="h-8 w-8 animate-spin text-indigo-500" />
      </div>
    }>
      <ChatContent />
    </Suspense>
  )
}
