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

  /* ===============================
     CONSULTA PREVALIDADOR HDI
  =============================== */
  consultarPrevalidador(
    placa?: string,
    idInspeccion?: string
  ): Observable<any> {

    const params: any = {};

    if (placa) params.placa = placa;
    if (idInspeccion) params.id_inspeccion = idInspeccion;

    return this.http.get(
      `${this.baseUrl}/consultation/inspection/consultar`,
      { params }
    );
  }

  /* ===============================
     GESTIONAR INSPECCION HDI
  =============================== */
  guardarPrevalidacion(
    idInspeccion: number,
    payload: any
  ) {
    return this.http.post(
      `${this.baseUrl}/inspection/${idInspeccion}`,
      payload
    );
  }
}