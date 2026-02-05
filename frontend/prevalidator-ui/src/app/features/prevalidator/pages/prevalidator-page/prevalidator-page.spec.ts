import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PrevalidatorPage } from './prevalidator-page';

describe('PrevalidatorPage', () => {
  let component: PrevalidatorPage;
  let fixture: ComponentFixture<PrevalidatorPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PrevalidatorPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PrevalidatorPage);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
