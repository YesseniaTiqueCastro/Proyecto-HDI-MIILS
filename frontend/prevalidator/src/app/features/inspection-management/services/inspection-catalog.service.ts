import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from '../../../core/services/api.service';
import { CatalogItem } from '../../../core/models/catalog.model';

import { core } from '@angular/compiler';


@Injectable({
  providedIn: 'root'
})
export class InspectionCatalogService {

  constructor(private api: ApiService) {}

  getServicios(): Observable<CatalogItem[]> {
    return this.api.get<CatalogItem[]>('/inspection-management/services');
  }

  getTiposCarroceria(): Observable<CatalogItem[]> {
    return this.api.get<CatalogItem[]>('/inspection-management/body-types');
  }

  getAreas(): Observable<CatalogItem[]> {
    return this.api.get<CatalogItem[]>('/inspection-management/areas');
  }

  getPartes(): Observable<CatalogItem[]> {
    return this.api.get<CatalogItem[]>('/inspection-management/parts');
  }

  getCriterios(): Observable<CatalogItem[]> {
    return this.api.get<CatalogItem[]>('/inspection-management/criteria');
  }
}
