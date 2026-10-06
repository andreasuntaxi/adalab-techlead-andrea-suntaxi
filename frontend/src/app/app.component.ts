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
  readonly message = signal('Cargando proyectos...');

  ngOnInit(): void {
    this.api.list().subscribe({
      next: projects => {
        this.projects.set(projects);
        this.message.set(
          projects.length
            ? 'Seleccione un proyecto para consultar sus indicadores.'
            : 'No hay proyectos disponibles.'
        );
      },
      error: () => {
        this.projects.set([]);
        this.summary.set(null);
        this.message.set('No se pudo cargar la lista de proyectos.');
      },
    });
  }

  selectProject(projectId: string): void {
    this.selectedId.set(projectId);
    this.summary.set(null);

    if (!projectId) {
      this.message.set('Seleccione un proyecto para consultar sus indicadores.');
      return;
    }

    this.message.set('Cargando indicadores...');

    this.api.summary(projectId).subscribe({
      next: value => {
        if (this.selectedId() !== projectId) return;

        this.summary.set(value);
        this.message.set('Indicadores cargados.');
      },
      error: () => {
        if (this.selectedId() !== projectId) return;

        this.summary.set(null);
        this.message.set('No se pudieron cargar los indicadores del proyecto.');
      },
    });
  }
}
