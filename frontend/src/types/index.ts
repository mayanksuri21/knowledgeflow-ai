export type ProcessingStatus = "uploaded" | "processing" | "ready" | "failed"

export interface Document {
  id: string
  user_id: string
  filename: string
  original_filename: string
  file_size: number
  mime_type: string
  storage_path: string
  processing_status: ProcessingStatus
  created_at: string
  updated_at?: string
}
