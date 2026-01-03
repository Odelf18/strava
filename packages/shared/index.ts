// Shared types between frontend and backend

export type VisualizationType = 
  | "facets" 
  | "map" 
  | "elevations" 
  | "landscape" 
  | "calendar" 
  | "dumbbell"

export type PackType = "single" | "all" | "premium"

export type JobStatus = "pending" | "processing" | "completed" | "failed" | "expired"

export interface BoundingBox {
  lon_min: number
  lon_max: number
  lat_min: number
  lat_max: number
}

export interface Filters {
  sport_types?: string[]
  date_from?: string
  date_to?: string
  bbox?: BoundingBox
  activity_ids?: number[]
}

export interface PaymentIntentCreate {
  job_id: number
  pack_type: PackType
  visualization_type?: string
  visualizations: VisualizationType[]
  has_filters: boolean
  filters?: Filters
  success_url: string
  cancel_url: string
}

export interface Job {
  id: number
  status: JobStatus
  visualizations: string | null
  has_filters: boolean
  created_at: string
  completed_at: string | null
  error_message: string | null
}

