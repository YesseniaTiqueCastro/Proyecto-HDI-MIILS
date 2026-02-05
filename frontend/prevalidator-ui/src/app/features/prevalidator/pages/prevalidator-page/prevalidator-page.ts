import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';

/* Angular Material */
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatDividerModule } from '@angular/material/divider';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-prevalidator-page',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatDividerModule,
    MatButtonModule,
  ],
  templateUrl: './prevalidator-page.html',
  styleUrls: ['./prevalidator-page.scss'],
})
export class PrevalidatorPageComponent {
  form: FormGroup;

  constructor(private fb: FormBuilder) {
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
      tipoCarroceria: [''],
      tipoVehiculo: [''],
      kilometraje: [''],
      kilometrajePorAnio: [''],
      tipoPintura: [''],
      caja: [''],
    });
  }
}
