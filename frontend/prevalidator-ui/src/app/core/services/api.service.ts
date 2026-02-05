import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment.development';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private readonly baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  consultarInspeccion(idInspeccion: string): Observable<any> {
    return this.http.get(
      `${this.baseUrl}/consultation/inspection/consultar`,
      {
        params: { id_inspeccion: idInspeccion }
      }
    );
  }
}
