import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreaOrdine } from './crea-ordine';

describe('CreaOrdine', () => {
  let component: CreaOrdine;
  let fixture: ComponentFixture<CreaOrdine>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreaOrdine],
    }).compileComponents();

    fixture = TestBed.createComponent(CreaOrdine);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
