import { Routes } from '@angular/router';
import { PrevalidatorPageComponent } from './features/prevalidator/pages/prevalidator-page/prevalidator-page';

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
];
