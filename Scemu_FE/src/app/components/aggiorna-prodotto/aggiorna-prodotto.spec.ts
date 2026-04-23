import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AggiornaProdotto } from './aggiorna-prodotto';

describe('AggiornaProdotto', () => {
  let component: AggiornaProdotto;
  let fixture: ComponentFixture<AggiornaProdotto>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AggiornaProdotto],
    }).compileComponents();

    fixture = TestBed.createComponent(AggiornaProdotto);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
