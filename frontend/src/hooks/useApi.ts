import { useAuth } from "@clerk/nextjs"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export function useApi() {
  const { getToken } = useAuth()

  async function fetchApi<T>(
    endpoint: string,
    options: RequestInit = {},
  ): Promise<T> {
    const token = await getToken()

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

  return { fetchApi }
}
