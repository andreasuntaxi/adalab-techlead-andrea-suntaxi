import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Project, ProjectSummary } from './project.models';

@Injectable({ providedIn: 'root' })
export class ProjectsService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl =
  'https://adalab-techlead-andrea-suntaxi.onrender.com';

  list(): Observable<Project[]> {
    return this.http.get<Project[]>(`${this.baseUrl}/projects`);
  }

  summary(projectId: string): Observable<ProjectSummary> {
    return this.http.get<ProjectSummary>(
      `${this.baseUrl}/projects/${encodeURIComponent(projectId)}/summary`
    );
  }
}