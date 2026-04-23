import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CercaPtrodotto } from './cerca-ptrodotto';

describe('CercaPtrodotto', () => {
  let component: CercaPtrodotto;
  let fixture: ComponentFixture<CercaPtrodotto>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CercaPtrodotto],
    }).compileComponents();

    fixture = TestBed.createComponent(CercaPtrodotto);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
