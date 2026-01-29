import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from '../../../core/services/api.service';
import { PrevalidatorData } from '../models/prevalidator.model';

@Injectable({
  providedIn: 'root'
})
export class PrevalidatorService {

  constructor(private api: ApiService) {}

  getPendingInspections(): Observable<PrevalidatorData[]> {
    return this.api.get<PrevalidatorData[]>('/prevalidator/pending');
  }

  getInspectionDetail(id: string): Observable<PrevalidatorData> {
    return this.api.get<PrevalidatorData>(`/prevalidator/${id}`);
  }
}
