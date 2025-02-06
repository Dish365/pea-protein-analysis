import { useQuery } from "@tanstack/react-query";
import type { Query } from "@tanstack/react-query";
import axios from "axios";
import { PROCESS_ENDPOINTS } from "@/config/endpoints";
import { ProcessType, ProcessStatus } from "@/types/process";

export interface Analysis {
  id: string;
  name: string;
  type: "technical" | "economic" | "environmental";
  status: "completed" | "in_progress";
  date: string;
}

export interface ProcessListResponse {
  data: Analysis[];
  total: number;
  page: number;
  pageSize: number;
}

// For now, let's use mock data since we don't have an API yet
const mockAnalyses: Analysis[] = [
  {
    id: "1",
    name: "Protein Extraction Process",
    type: "technical",
    status: "completed",
    date: "2024-01-30",
  },
  {
    id: "2",
    name: "Cost Analysis Q1 2024",
    type: "economic",
    status: "completed",
    date: "2024-01-29",
  },
  {
    id: "3",
    name: "Carbon Footprint Assessment",
    type: "environmental",
    status: "in_progress",
    date: "2024-01-28",
  },
];

export function useRecentAnalyses() {
  return useQuery({
    queryKey: ["recentAnalyses"],
    queryFn: async () => {
      // For development, return mock data
      return mockAnalyses;

      // When API is ready, uncomment this:
      // const response = await axios.get("/api/analyses/recent");
      // return response.data;
    },
  });
}
