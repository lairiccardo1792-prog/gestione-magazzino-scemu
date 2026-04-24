import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CercaOrdine } from './cerca-ordine';

describe('CercaOrdine', () => {
  let component: CercaOrdine;
  let fixture: ComponentFixture<CercaOrdine>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CercaOrdine],
    }).compileComponents();

    fixture = TestBed.createComponent(CercaOrdine);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
