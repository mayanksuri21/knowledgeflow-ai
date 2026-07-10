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
  page_count?: number
  word_count?: number
  character_count?: number
  extracted_text?: string
  processed_at?: string
  created_at: string
  updated_at?: string
}
