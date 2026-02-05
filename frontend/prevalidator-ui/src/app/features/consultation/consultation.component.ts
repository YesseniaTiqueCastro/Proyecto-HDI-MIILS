import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { environment } from '../../../environments/environment.development';

@Component({
  selector: 'app-consultation',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './consultation.component.html',
})
export class ConsultationComponent {

  loading = false;
  response: any = null;
  error: string | null = null;

  constructor(private http: HttpClient) {}

  consultar(idInspeccion: string) {
    this.loading = true;
    this.response = null;
    this.error = null;

    const url = `${environment.apiUrl}/consultation/inspection/consultar?id_inspeccion=${idInspeccion}`;

    console.log('Llamando a:', url);

    this.http.get(url).subscribe({
      next: (data) => {
        console.log('Response backend:', data);
        this.response = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error backend:', err);
        this.error = 'Error consultando inspección';
        this.loading = false;
      }
    });
  }
}
