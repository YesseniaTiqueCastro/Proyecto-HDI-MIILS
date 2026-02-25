import { Component, DoCheck } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';

/* IMPORTACIÓN ANGULAR MATERIAL */
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatDividerModule } from '@angular/material/divider';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

/* SERVICE */
import { ApiService } from '../../core/services/api.service';

@Component({
  selector: 'app-consultation-page',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatDividerModule,
    MatButtonModule,
    MatIconModule
  ],
  templateUrl: './consultation-page.html',
  styleUrls: ['./consultation-page.scss'],
})
export class ConsultationPageComponent implements DoCheck {

  placa: string = '';
  idInspeccion: string = '';

  bloquearPlaca = false;
  bloquearId = false;

  cargando = false;
  resultado: any = null;

  form: FormGroup;

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService
  ) {
    this.form = this.fb.group({});
  }

  ngDoCheck() {
    this.bloquearPlaca = !!this.idInspeccion;
    this.bloquearId = !!this.placa;
  }

  limpiarBusqueda() {
    this.placa = '';
    this.idInspeccion = '';
    this.resultado = null;
  }

  limpiarFormulario() {
    this.limpiarBusqueda();
  }

  consultar() {

    if (this.cargando) return;

    const valor = this.idInspeccion || this.placa;

    if (!valor) {
      alert('Debe ingresar placa o id inspección');
      return;
    }

    this.cargando = true;

    this.apiService.consultarInspeccionHDI(
      this.placa || undefined,
      this.idInspeccion || undefined
    )
    .subscribe({
      next: (data: any) => {

  console.log('RESPUESTA CONSULTA HDI', data);

  /* ========= NORMALIZAR RESPUESTA ========= */

  const inspeccion = data?.inspeccion;
  const cliente =
    inspeccion?.datosInspeccionAuto?.clienteInspeccion;

  // SI direccion viene objeto → convertir a array
  if (cliente?.direccion && !Array.isArray(cliente.direccion)) {
    cliente.direccion = [cliente.direccion];
  }

  // SI contacto viene objeto → convertir a array
  if (cliente?.contacto && !Array.isArray(cliente.contacto)) {
    cliente.contacto = [cliente.contacto];
  }

  /* ======================================== */

  this.resultado = data;

  this.cargando = false;
},
      error: () => {
        alert('No se encontraron datos');
        this.cargando = false;
      }
    });
  }
}