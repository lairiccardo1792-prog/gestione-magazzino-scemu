import { Component } from '@angular/core';
import { Router, NavigationEnd, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { filter } from 'rxjs';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterModule, CommonModule],
  templateUrl: './navbar.html',
  styleUrls: ['./navbar.css'],
})
export class NavbarComponent {

  showNavbar = true;

  // 🔥 DROPDOWN STATE UNICO (FIX DEFINITIVO)
  activeDropdown: 'ordini' | 'prodotti' | null = null;

  constructor(
    private router: Router,
    private authService: AuthService
  ) {
    this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe((event: NavigationEnd) => {
        this.showNavbar = !event.urlAfterRedirects.includes('/login');

        // opzionale ma consigliato: chiude dropdown al cambio pagina
        this.activeDropdown = null;
      });
  }

  // 🔽 DROPDOWN TOGGLE (UNICO PER TUTTI)
  toggleDropdown(menu: 'ordini' | 'prodotti') {
    this.activeDropdown =
      this.activeDropdown === menu ? null : menu;
  }

  // 🔐 LOGIN
  login() {
    this.router.navigate(['/login']);
  }

  // 🚪 LOGOUT
  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);

    // chiude dropdown al logout
    this.activeDropdown = null;
  }

  // 👤 USER
  get username(): string {
    return this.authService.getUsername() ?? 'Utente';
  }

  get isLoggedIn(): boolean {
    return this.authService.isLoggedIn();
  }
}