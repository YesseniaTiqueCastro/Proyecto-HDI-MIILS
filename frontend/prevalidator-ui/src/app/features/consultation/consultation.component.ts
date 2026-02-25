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
    this.placa = this.placa?.toUpperCase();
    this.apiService.consultarInspeccionHDI(
      this.placa || undefined,
      this.idInspeccion || undefined
    )
    .subscribe({
      next: (data: any) => {

  console.log('RESPUESTA CONSULTA HDI', data);

  const inspeccion = data?.inspeccion;
  const datos = inspeccion?.datosInspeccionAuto;
  const cliente = datos?.clienteInspeccion;
  const vehiculo = datos?.vehiculo;

  /* ============================
MAPAS DE DESCRIPCIONES
============================ */

const mapaGenero: any = {
  '1': 'Masculino',
  '2': 'Femenino'
};

const mapaTipoPersona: any = {
  '1': 'Natural'
};

const mapaTipoPlaca: any = {
  '12': 'Colombiana',
  '14': 'Diplomática',
  '11': 'Tránsito Libre'
};

/* ============================
TRANSFORMACIONES VISUALES
============================ */

// GENERO
if (cliente?.personaNatural?.genero?.codigo) {
  cliente.personaNatural.genero =
    mapaGenero[cliente.personaNatural.genero.codigo] || '';
}

// TIPO PERSONA
if (cliente?.tipoPersona?.codigo) {
  cliente.tipoPersona =
    mapaTipoPersona[cliente.tipoPersona.codigo] || '';
}

// TIPO PLACA
if (vehiculo?.placa?.tipoPlaca?.codigo) {
  vehiculo.placa.tipoPlaca =
    mapaTipoPlaca[vehiculo.placa.tipoPlaca.codigo] || '';
}

  /* ========= NORMALIZAR ARRAYS ========= */

  if (cliente?.direccion && !Array.isArray(cliente.direccion)) {
    cliente.direccion = [cliente.direccion];
  }

  if (cliente?.contacto && !Array.isArray(cliente.contacto)) {
    cliente.contacto = [cliente.contacto];
  }

  /* ========= FUNCION SEGURA ========= */

  const valorSeguro = (obj: any, ...keys: string[]) => {
    for (const k of keys) {
      if (obj?.[k]) return obj[k];
    }
    return '';
  };

  /* ========= MAPPER DIRECCION ========= */

  const dir = cliente?.direccion?.[0] || {};

  dir.pais = valorSeguro(dir.pais, 'nombre', 'codigo', 'descripcion');
  dir.departamento = valorSeguro(dir.departamento, 'nombre', 'codigo');
  dir.ciudad = valorSeguro(dir.ciudad, 'nombre', 'codigo');
  dir.tipoDireccion = valorSeguro(dir.tipoDireccion, 'nombre', 'codigo');

  /* ========= RESULTADO FINAL ========= */

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