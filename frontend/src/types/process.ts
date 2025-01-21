export interface Process {
  id: string;
  name: string;
  status: ProcessStatus;
  createdAt: Date;
  updatedAt: Date;
}

export enum ProcessStatus {
  PENDING = "PENDING",
  RUNNING = "RUNNING",
  COMPLETED = "COMPLETED",
  FAILED = "FAILED",
}

export interface ProcessMetadata {
  startTime?: Date;
  endTime?: Date;
  progress?: number;
  error?: string;
}
