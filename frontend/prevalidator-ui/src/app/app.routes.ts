import { Routes } from '@angular/router';
import { PrevalidatorPageComponent } from './features/prevalidator/pages/prevalidator-page/prevalidator-page';
import { ConsultationPageComponent } from './features/consultation/consultation.component';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'prevalidator',
    pathMatch: 'full',
  },
  {
    path: 'prevalidator',
    component: PrevalidatorPageComponent,
  },
  {
    path: 'consulta',
    component: ConsultationPageComponent,
  },
];