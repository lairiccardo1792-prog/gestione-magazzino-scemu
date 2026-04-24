import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OrdiniHome } from './ordini-home';

describe('OrdiniHome', () => {
  let component: OrdiniHome;
  let fixture: ComponentFixture<OrdiniHome>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OrdiniHome],
    }).compileComponents();

    fixture = TestBed.createComponent(OrdiniHome);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
