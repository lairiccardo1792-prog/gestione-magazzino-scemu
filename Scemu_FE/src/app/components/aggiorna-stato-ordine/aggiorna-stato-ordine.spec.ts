import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AggiornaStatoOrdine } from './aggiorna-stato-ordine';

describe('AggiornaStatoOrdine', () => {
  let component: AggiornaStatoOrdine;
  let fixture: ComponentFixture<AggiornaStatoOrdine>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AggiornaStatoOrdine],
    }).compileComponents();

    fixture = TestBed.createComponent(AggiornaStatoOrdine);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
