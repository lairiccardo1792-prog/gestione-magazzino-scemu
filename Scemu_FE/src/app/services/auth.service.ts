// Injectable significa: questo servizio può essere "iniettato" in altri file
import { Injectable } from '@angular/core';

// HttpClient serve per fare chiamate al backend (GET, POST, ecc.)
import { HttpClient } from '@angular/common/http';

// tap serve per eseguire codice senza modificare la risposta
import { tap } from 'rxjs';

@Injectable({
  providedIn: 'root' // disponibile in tutta l'app senza importarlo manualmente
})
export class AuthService {

  // URL del backend)
  private API_URL = 'http://localhost:8000';

  // injectiamo HttpClient nel costruttore
  constructor(private http: HttpClient) {}

  // FUNZIONE LOGIN
  login(credentials: any) {
    return this.http.post<any>(`${this.API_URL}/login`, credentials)  
    .pipe(
        tap(response => {
          console.log('RISPOSTA SERVER:', response);
          // Se il login va a buon fine, salviamo il token
          if (response && response.token) {
            localStorage.setItem('username', response.username); // nella login
            localStorage.setItem('token', response.token);
            console.log('Token salvato correttamente!');
          } else {
            console.error('ERRORE: Il server non ha inviato un token. Controlla la console.');
          }
        })
      );
  }

  // logout: cancella il token salvato
  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username'); // nella logout

  }

  // controllo semplice: esiste il token?
  isLoggedIn(): boolean {
    return localStorage.getItem('token') !== null;
  }

  // Serve alla navbar per recuperare il nome utente
  getUsername(): string | null {
    return localStorage.getItem('username');
  }
}


