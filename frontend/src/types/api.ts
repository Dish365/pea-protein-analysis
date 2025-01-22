import { ProcessAnalysis } from './process';
import { AnalysisResult } from './analysis';

// API Response Types
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  details?: Record<string, string[]>;
  status?: string;
  message?: string;
}

// API Error Response
export interface ApiError {
  status: number;
  message: string;
  errors?: Record<string, string[]>;
}

// Pagination Response Type
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

export interface ProcessCreateResponse {
  process_id: number;
  status: string;
  message?: string;
  summary?: AnalysisResult['summary'];
}

export interface ProcessStatusResponse {
  status: ProcessAnalysis['status'];
  progress: number;
  message?: string;
}

export interface ProcessListResponse extends Array<ProcessAnalysis> {}

export interface ProcessDetailResponse extends ProcessAnalysis {
  results?: AnalysisResult;
}

export interface ErrorResponse {
  error: string;
  details?: Record<string, string[]>;
}
