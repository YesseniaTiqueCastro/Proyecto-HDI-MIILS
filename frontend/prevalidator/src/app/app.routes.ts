import { Routes } from '@angular/router';
import { PendingListComponent } from './features/prevalidator/pages/pending-list/pending-list.component';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'prevalidator',
    pathMatch: 'full',
  },
  {
    path: 'prevalidator',
    component: PendingListComponent,
  },
];
