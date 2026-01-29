import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-pending-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './pending-list.component.html',
})
export class PendingListComponent {
  loading = false;

  pendingInspections = [
    {
      orderNumber: 'ORD-001',
      chassis: 'CH-123',
      inspectionId: 1,
    },
    {
      orderNumber: 'ORD-002',
      chassis: 'CH-456',
      inspectionId: 2,
    },
  ];

  openInspection(id: number) {
    console.log('Abrir inspección', id);
  }
}

