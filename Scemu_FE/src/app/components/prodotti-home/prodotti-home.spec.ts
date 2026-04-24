import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProdottiHome } from './prodotti-home';

describe('ProdottiHome', () => {
  let component: ProdottiHome;
  let fixture: ComponentFixture<ProdottiHome>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProdottiHome],
    }).compileComponents();

    fixture = TestBed.createComponent(ProdottiHome);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
