import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginLandingPage } from './login-landing-page';

describe('LoginLandingPage', () => {
  let component: LoginLandingPage;
  let fixture: ComponentFixture<LoginLandingPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoginLandingPage],
    }).compileComponents();

    fixture = TestBed.createComponent(LoginLandingPage);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
