import { Component, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import {FormsModule,FormBuilder,FormGroup,ReactiveFormsModule,Validators} from '@angular/forms';

import { finalize } from 'rxjs/operators';

/* MATERIAL */
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatDividerModule } from '@angular/material/divider';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule, MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';

/* SERVICE */
import { ApiService } from '../../../../core/services/api.service';
import { buildHdiPayload } from '../../mappers/hdi-payload.mapper';

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
    MatIconModule,
    MatTableModule,
    MatPaginatorModule
  ],
  templateUrl: './prevalidator-page.html',
  styleUrls: ['./prevalidator-page.scss'],
})
export class PrevalidatorPageComponent {

  idBusqueda: string = '';
  idInspeccion: number | null = null;
  cargando: boolean = false;

  servicios = SERVICIOS;
  tiposCaja = TIPOS_CAJA;
  tiposCarroceria = TIPOS_CARROCERIA;
  tiposVehiculo = TIPOS_VEHICULO;
  colores = COLORES;
  tiposPintura = TIPOS_PINTURA;

  form: FormGroup;

  /* ================= CALIFICACIONES ================= */

  displayedColumnsCalificaciones: string[] = [
    'id_service',
    'area',
    'parte',
    'criterio'
  ];

  dataSourceCalificaciones = new MatTableDataSource<any>([]);

  @ViewChild('paginatorCalificaciones')
  paginatorCalificaciones!: MatPaginator;

  /* ================= ACCESORIOS ================= */

  displayedColumnsAccesorios: string[] = [
    'id_service',
    'valor',
    'nombre',
    'existencia',
    'id_accesorio',
    'asegurable',
    'original',
    'cantidad',
    'id_hdi'
  ];

  dataSourceAccesorios = new MatTableDataSource<any>([]);

  @ViewChild('paginatorAccesorios')
  paginatorAccesorios!: MatPaginator;

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService
  ) {

    this.form = this.fb.group({
      fechaHoraInspeccion: [''],
      fechaHoraSalidaInspeccion: [''],
      tipo: [''],
      codigoFasecolda: [''],
      servicio: ['', Validators.required],
      chasis: [''],
      serial: [''],
      motor: [''],
      modelo: [''],
      color: ['', Validators.required],
      tipoPintura: ['', Validators.required],
      tipoCarroceria: ['', Validators.required],
      tipoVehiculo: ['', Validators.required],
      kilometraje: [''],
      caja: ['', Validators.required],
    });
  }

  limpiarBusqueda() {
    this.idBusqueda = '';
    this.idInspeccion = null;
  }

  limpiarFormulario() {
    this.form.reset();
    this.limpiarBusqueda();
    this.dataSourceCalificaciones.data = [];
    this.dataSourceAccesorios.data = [];
  }

  consultar() {

    if (this.cargando) return;

    const id = this.idBusqueda?.trim();

    if (!id) {
      alert('Debe ingresar id inspección');
      return;
    }

    this.cargando = true;
    this.apiService.consultarPrevalidador(id)
      .pipe(finalize(() => this.cargando = false))
      .subscribe({
        next: (data: any) => {

          console.log('DATA PREVALIDADOR:', data);

          this.idInspeccion = Number(id);

          /* ===== INSPECCIÓN ===== */
          this.form.patchValue({
            fechaHoraInspeccion: data.inspeccion?.fechaHoraInspeccion,
            fechaHoraSalidaInspeccion: data.inspeccion?.fechaHoraSalidaInspeccion,
            tipo: data.inspeccion?.tipo,
            codigoFasecolda: data.inspeccion?.codigoFasecolda,
            servicio: data.inspeccion?.servicio,
            chasis: data.inspeccion?.chasis,
            serial: data.inspeccion?.serial,
            motor: data.inspeccion?.motor,
            modelo: data.inspeccion?.modelo,
            color: data.inspeccion?.color,
            tipoPintura: data.inspeccion?.tipoPintura,
            tipoCarroceria: data.inspeccion?.tipoCarroceria,
            tipoVehiculo: data.inspeccion?.tipoVehiculo,
            kilometraje: data.inspeccion?.kilometraje,
            caja: data.inspeccion?.caja,
          });

          /* ===== CALIFICACIONES ===== */
          this.dataSourceCalificaciones.data = data.calificaciones || [];
          setTimeout(() => {
            this.dataSourceCalificaciones.paginator = this.paginatorCalificaciones;
          });

          /* ===== ACCESORIOS ===== */
          this.dataSourceAccesorios.data = data.accesorios || [];
          setTimeout(() => {
            this.dataSourceAccesorios.paginator = this.paginatorAccesorios;
          });

        },
        error: () => {
          alert('No se encontraron datos');
        }
      });
  }

  guardar() {

    if (!this.idInspeccion) {
      alert('Debe consultar una inspección primero');
      return;
    }

    if (this.form.invalid) {
      alert('Debe completar los campos obligatorios');
      return;
    }

    const payload = buildHdiPayload(
      this.form.value,
      this.idInspeccion
    );

    this.apiService
      .guardarPrevalidacion(this.idInspeccion, payload)
      .subscribe({
        next: () => {
          alert('Inspección gestionada correctamente');
        },
        error: () => {
          alert('Error enviando a HDI');
        }
      });
  }
}