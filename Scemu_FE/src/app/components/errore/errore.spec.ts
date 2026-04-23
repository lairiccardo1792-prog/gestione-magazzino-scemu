import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Errore } from './errore';

describe('Errore', () => {
  let component: Errore;
  let fixture: ComponentFixture<Errore>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Errore],
    }).compileComponents();

    fixture = TestBed.createComponent(Errore);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
