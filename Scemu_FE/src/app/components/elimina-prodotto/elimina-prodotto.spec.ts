import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EliminaProdotto } from './elimina-prodotto';

describe('EliminaProdotto', () => {
  let component: EliminaProdotto;
  let fixture: ComponentFixture<EliminaProdotto>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EliminaProdotto],
    }).compileComponents();

    fixture = TestBed.createComponent(EliminaProdotto);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
