export interface Project {
  id: string;
  name: string;
  budget: number;
  status: 'active' | 'archived';
}

export interface ProjectSummary {
  project_id: string;
  name: string;
  activity_count: number;
  completed_count: number;
  total_hours: number;
  completion_rate: number;
}
