import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { Project, ProjectSummary } from './project.models';

@Injectable({ providedIn: 'root' })
export class ProjectsService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = '/api';

  list(): Observable<Project[]> {
    return this.http.get<Project[]>(`${this.baseUrl}/projects`);
  }

  summary(projectId: string): Observable<ProjectSummary> {
    // TODO: consumir el endpoint de resumen implementado en el backend.
    return throwError(() => new Error(`Resumen pendiente: ${projectId}`));
  }
}
