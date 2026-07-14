import { auth } from "@clerk/nextjs/server"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {},
): Promise<T> {
  const { getToken } = auth()
  const token = await getToken({
    template: "backend",
  })

  const headers = new Headers(options.headers || {})
  if (token) {
    headers.set("Authorization", `Bearer ${token}`)
  }
  if (!headers.has("Content-Type") && !(options.body instanceof FormData)) {
    headers.set("Content-Type", "application/json")
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`)
  }

  if (response.status === 204) return {} as T
  return response.json()
}

export async function getDocuments(): Promise<any[]> {
  return fetchApi("/api/v1/documents")
}

export async function uploadDocument(file: File): Promise<any> {
  const formData = new FormData()
  formData.append("file", file)

  return fetchApi("/api/v1/documents/upload", {
    method: "POST",
    body: formData,
  })
}

export async function deleteDocument(documentId: string): Promise<void> {
  return fetchApi(`/api/v1/documents/${documentId}`, {
    method: "DELETE",
  })
}
