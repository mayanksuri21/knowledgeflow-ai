"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Upload, Trash2, FileText, Cpu } from "lucide-react"
import { Document } from "@/types"
import { useApi } from "@/hooks/useApi"

function formatFileSize(bytes: number): string {
  if (bytes === 0) return "0 Bytes"
  const k = 1024
  const sizes = ["Bytes", "KB", "MB", "GB"]
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i]
}

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })
}

function getStatusVariant(status: string) {
  switch (status) {
    case "uploaded":
      return "secondary"
    case "processing":
      return "default"
    case "ready":
      return "default"
    case "failed":
      return "destructive"
    default:
      return "outline"
  }
}

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [processingIds, setProcessingIds] = useState<Set<string>>(new Set())
  const { fetchApi } = useApi()

  async function loadDocuments() {
    try {
      setIsLoading(true)
      setError(null)
      const data = await fetchApi<Document[]>("/api/v1/documents")
      setDocuments(data)
    } catch (err) {
      setError("Failed to load documents")
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadDocuments()
  }, [])

  async function handleFileUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return

    try {
      setIsUploading(true)
      setError(null)
      const formData = new FormData()
      formData.append("file", file)
      await fetchApi("/api/v1/documents/upload", {
        method: "POST",
        body: formData,
      })
      await loadDocuments()
    } catch (err) {
      setError("Failed to upload document")
      console.error(err)
    } finally {
      setIsUploading(false)
      e.target.value = ""
    }
  }

  async function handleProcess(documentId: string) {
    try {
      setError(null)
      setProcessingIds((prev) => new Set(prev).add(documentId))
      await fetchApi(`/api/v1/documents/${documentId}/process`, {
        method: "POST",
      })
      await loadDocuments()
    } catch (err) {
      setError("Failed to process document")
      console.error(err)
    } finally {
      setProcessingIds((prev) => {
        const next = new Set(prev)
        next.delete(documentId)
        return next
      })
    }
  }

  async function handleDelete(documentId: string) {
    if (!confirm("Are you sure you want to delete this document?")) return

    try {
      setError(null)
      await fetchApi(`/api/v1/documents/${documentId}`, {
        method: "DELETE",
      })
      await loadDocuments()
    } catch (err) {
      setError("Failed to delete document")
      console.error(err)
    }
  }

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Documents</h1>
          <p className="text-muted-foreground">Manage your uploaded PDFs</p>
        </div>
        <div className="relative">
          <input
            type="file"
            accept="application/pdf"
            onChange={handleFileUpload}
            disabled={isUploading}
            className="absolute inset-0 opacity-0 cursor-pointer"
          />
          <Button disabled={isUploading} className="flex items-center gap-2">
            <Upload className="h-4 w-4" />
            {isUploading ? "Uploading..." : "Upload PDF"}
          </Button>
        </div>
      </div>

      {error && (
        <div className="bg-destructive/10 text-destructive p-3 rounded-md">
          {error}
        </div>
      )}

      {isLoading ? (
        <div className="text-center py-12 text-muted-foreground">
          Loading...
        </div>
      ) : documents.length === 0 ? (
        <div className="text-center py-12 border rounded-lg">
          <FileText className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
          <h3 className="font-medium text-lg">No documents yet</h3>
          <p className="text-muted-foreground mt-2">
            Upload your first PDF to get started
          </p>
        </div>
      ) : (
        <div className="border rounded-lg overflow-hidden">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Filename</TableHead>
                <TableHead>Size</TableHead>
                <TableHead>Pages</TableHead>
                <TableHead>Words</TableHead>
                <TableHead>Characters</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Upload Date</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {documents.map((doc) => (
                <TableRow key={doc.id}>
                  <TableCell className="font-medium">
                    {doc.original_filename}
                  </TableCell>
                  <TableCell>{formatFileSize(doc.file_size)}</TableCell>
                  <TableCell>{doc.page_count ?? "-"}</TableCell>
                  <TableCell>{doc.word_count ?? "-"}</TableCell>
                  <TableCell>{doc.character_count ?? "-"}</TableCell>
                  <TableCell>
                    <Badge variant={getStatusVariant(doc.processing_status)}>
                      {doc.processing_status}
                    </Badge>
                  </TableCell>
                  <TableCell>{formatDate(doc.created_at)}</TableCell>
                  <TableCell className="text-right flex gap-2 justify-end">
                    <Button
                      variant="secondary"
                      size="sm"
                      onClick={() => handleProcess(doc.id)}
                      disabled={
                        doc.processing_status === "processing" ||
                        doc.processing_status === "ready" ||
                        processingIds.has(doc.id)
                      }
                      className="flex items-center gap-1"
                    >
                      <Cpu className="h-3 w-3" />
                      {processingIds.has(doc.id) ? "Processing..." : "Process"}
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => handleDelete(doc.id)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  )
}
