import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { ProjectsService } from './projects.service';
import { ProjectSummary } from './project.models';

describe('ProjectsService', () => {
  let service: ProjectsService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    });

    service = TestBed.inject(ProjectsService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('consulta el resumen por GET y devuelve sus indicadores', () => {
    const projectId = '64b000000000000000000001';
    const expected: ProjectSummary = {
      project_id: projectId,
      name: 'SAT',
      activity_count: 3,
      completed_count: 2,
      total_hours: 35,
      completion_rate: 2 / 3,
    };
    let received: ProjectSummary | undefined;

    service.summary(projectId).subscribe(value => {
      received = value;
    });

    const request = httpMock.expectOne(
      `https://adalab-techlead-andrea-suntaxi.onrender.com/projects/${projectId}/summary`
    );

    expect(request.request.method).toBe('GET');

    request.flush(expected);

    expect(received).toEqual(expected);
  });
});