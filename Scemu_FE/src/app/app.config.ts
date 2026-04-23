import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptorsFromDi } from '@angular/common/http'; // Aggiungi withInterceptorsFromDi
import { HTTP_INTERCEPTORS } from '@angular/common/http'; // Importa il token per gli interceptor
import { AuthInterceptor } from './interceptors/auth.interceptor'; 
import { StatisticheComponent } from './components/statistiche/statistiche';

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),

    // 1. Configura il client HTTP per accettare gli interceptor "class-based"
    provideHttpClient(
      withInterceptorsFromDi()
    ),

    // 2. Registra il tuo AuthInterceptor nel sistema di Dependency Injection
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }
  ]
};