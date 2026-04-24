import { Injectable } from '@angular/core';
import { CanActivate, Router, UrlTree } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  canActivate(): boolean | UrlTree {
    // Se l'utente è loggato (ovvero se c'è il token nel localStorage)
    if (this.authService.isLoggedIn()) {
      return true; // Accesso consentito
    }

    // Se non è loggato, lo reindirizziamo alla pagina di login
    console.warn('Accesso negato: Token non trovato. Reindirizzamento al login...');
    return this.router.parseUrl('/login');
  }
}