// ===== INTERCEPTOR: Intercetta TUTTE le richieste HTTP e aggiunge il token =====
// Questo significa: "Ogni volta che fai una richiesta HTTP (GET, POST, ecc),
// prima di inviarla, aggiungi il token nel header Authorization"

// 1. IMPORTIAMO GLI STRUMENTI
import { Injectable } from '@angular/core';  // @Injectable = rende questo servizio iniettabile (usabile ovunque)

// Strumenti per intercettare richieste HTTP
import { HttpInterceptor, HttpRequest, HttpHandler } from '@angular/common/http';
// HttpInterceptor = l'interfaccia che definisce un interceptor
// HttpRequest = la richiesta HTTP che vogliamo modificare
// HttpHandler = l'oggetto che invia la richiesta

// 2. DEFINIAMO L'INTERCEPTOR
@Injectable()  // @Injectable = questo servizio può essere iniettato in altri componenti/servizi
export class AuthInterceptor implements HttpInterceptor {  // Implementiamo l'interfaccia HttpInterceptor

  // ===== FUNZIONE CHE INTERCETTA TUTTE LE RICHIESTE HTTP =====
  // Questa funzione si chiama AUTOMATICAMENTE ogni volta che fai una richiesta HTTP
  intercept(req: HttpRequest<any>, next: HttpHandler) {
    // req = la richiesta HTTP originale (es: GET /api/ordini)
    // next = il "next handler" (la cosa che invia la richiesta al server)

    // STEP 1: PRENDIAMO IL TOKEN SALVATO NEL BROWSER
    const token = localStorage.getItem('token');  // localStorage è il browser che salva dati
    // token sarà qualcosa come: "dXNlcjEyMzoxNzEzNjEyMzQ1" (la stringa codificata dal backend)

    // STEP 2: SE ABBIAMO IL TOKEN → AGGIUNGIAMOLO ALLA RICHIESTA
    if (token) {  // Se token esiste (cioè sei loggato)

      // Creiamo una COPIA della richiesta originale (non la modifichiamo, ne facciamo una copia)
      const clonedRequest = req.clone({  // .clone() = copia la richiesta

        // Aggiungiamo il header Authorization (es: "Authorization: Bearer token123")
        setHeaders: {  // setHeaders = aggiungi questi header
          Authorization: `Bearer ${token}` // "Bearer token123" è il formato standard per i token
        }
      });

      // STEP 3: INVIAMO LA RICHIESTA MODIFICATA (CON IL TOKEN)
      return next.handle(clonedRequest);  // next.handle() = invia la richiesta al server
    }

    // STEP 4: SE NON ABBIAMO TOKEN → INVIAMO LA RICHIESTA NORMALE (SENZA MODIFICHE)
    // Questo succede se l'utente non è loggato
    return next.handle(req);  // Invia la richiesta così come è
  }
}