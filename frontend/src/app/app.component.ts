import { Component, inject, OnInit, signal } from '@angular/core';
import { DecimalPipe, PercentPipe } from '@angular/common';
import { ProjectsService } from './projects.service';
import { Project, ProjectSummary } from './project.models';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [DecimalPipe, PercentPipe],
  templateUrl: './app.component.html',
})
export class AppComponent implements OnInit {
  private readonly api = inject(ProjectsService);
  readonly projects = signal<Project[]>([]);
  readonly selectedId = signal('');
  readonly summary = signal<ProjectSummary | null>(null);
  readonly message = signal('Seleccione un proyecto para consultar sus indicadores.');

  ngOnInit(): void {
    this.api.list().subscribe({
      next: projects => this.projects.set(projects),
      error: () => this.message.set('No se pudo cargar la lista de proyectos.'),
    });
  }

  selectProject(projectId: string): void {
    this.selectedId.set(projectId);
    // TODO: completar el flujo de carga, resultado y error del resumen.
    // Considerar cambios de selección antes de terminar una petición.
    this.message.set('La consulta del resumen está pendiente de implementación.');
  }
}
