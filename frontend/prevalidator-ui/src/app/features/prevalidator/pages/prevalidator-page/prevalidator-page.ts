import { Component, DoCheck } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';

/* MATERIAL */
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatDividerModule } from '@angular/material/divider';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

/* SERVICE */
import { ApiService } from '../../../../core/services/api.service';

/* CATALOGOS */
import {
  SERVICIOS,
  TIPOS_CAJA,
  TIPOS_CARROCERIA,
  TIPOS_VEHICULO,
  COLORES,
  TIPOS_PINTURA
} from '../../../../core/catalogos_hdi';

@Component({
  selector: 'app-prevalidator-page',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatDividerModule,
    MatButtonModule,
    MatIconModule
  ],
  templateUrl: './prevalidator-page.html',
  styleUrls: ['./prevalidator-page.scss'],
})
export class PrevalidatorPageComponent implements DoCheck {

  placaBusqueda = '';
  idBusqueda = '';

  bloquearPlaca = false;
  bloquearId = false;
  cargando = false;

  /* ===== CATÁLOGOS ===== */
  servicios = SERVICIOS;
  tiposCaja = TIPOS_CAJA;
  tiposCarroceria = TIPOS_CARROCERIA;
  tiposVehiculo = TIPOS_VEHICULO;
  colores = COLORES;
  tiposPintura = TIPOS_PINTURA;

  form: FormGroup;

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService
  ) {

    this.form = this.fb.group({
      fechaHoraInspeccion: [''],
      fechaHoraSalidaInspeccion: [''],
      tipo: [''],
      codigoFasecolda: [''],
      servicio: [''],
      chasis: [''],
      serial: [''],
      motor: [''],
      modelo: [''],
      color: [''],
      tipoPintura: [''],
      tipoCarroceria: [''],
      tipoVehiculo: [''],
      kilometraje: [''],
      caja: [''],
    });
  }

  ngDoCheck() {
    this.bloquearPlaca = !!this.idBusqueda;
    this.bloquearId = !!this.placaBusqueda;
  }

  limpiarBusqueda() {
    this.placaBusqueda = '';
    this.idBusqueda = '';
  }

  limpiarFormulario() {
    this.form.reset();
    this.limpiarBusqueda();
  }

  consultar() {

    if (this.cargando) return;

    const valor = this.idBusqueda || this.placaBusqueda;

    if (!valor) {
      alert('Debe ingresar placa o id inspección');
      return;
    }

    this.cargando = true;

    this.apiService.consultarPrevalidador(
      this.placaBusqueda || undefined,
      this.idBusqueda || undefined
    )
    .subscribe({
      next: (data: any) => {

        console.log('DATA HDI:', data);

        this.form.patchValue({
          fechaHoraInspeccion: data.inspeccion?.fechaHoraInspeccion,
          fechaHoraSalidaInspeccion: data.inspeccion?.fechaHoraSalidaInspeccion,
          tipo: data.vehiculo?.tipo,
          codigoFasecolda: data.vehiculo?.codigoFasecolda,
          servicio: data.vehiculo?.servicio,
          chasis: data.vehiculo?.chasis,
          serial: data.vehiculo?.serial,
          motor: data.vehiculo?.motor,
          modelo: data.vehiculo?.modelo,
          color: data.vehiculo?.color,
          tipoPintura: data.vehiculo?.tipoPintura,
          tipoCarroceria: data.vehiculo?.carroceria,
          tipoVehiculo: data.vehiculo?.tipoVehiculo,
          kilometraje: data.vehiculo?.kilometraje,
          caja: data.vehiculo?.tipoCaja,
        });

        this.cargando = false;
      },
      error: () => {
        alert('No se encontraron datos');
        this.cargando = false;
      }
    });
  }
}