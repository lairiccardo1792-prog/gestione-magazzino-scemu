import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; 
import { RouterLink } from '@angular/router';
import { ProductService } from '../../services/product'; 

@Component({
  selector: 'app-elimina-prodotto',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './elimina-prodotto.html',
  styleUrl: './elimina-prodotto.css'
})
export class EliminaProdotto {
  prodottoId: number | null = null;
  loading = false;
  successo = false;
  errore = false;
  messaggioErrore = '';

  constructor(
    private productService: ProductService, 
    private cdr: ChangeDetectorRef
  ) {}

  onElimina(): void {
    if (!this.prodottoId) return;

    const conferma = confirm(`Sei sicuro di voler eliminare il prodotto ID: ${this.prodottoId}?`);
    
    if (conferma) {
      this.loading = true;
      this.successo = false;
      this.errore = false;
      this.messaggioErrore = '';

      this.productService.eliminaProdotto(this.prodottoId).subscribe({
        next: () => {
          // Successo: il backend ha risposto 204
          this.loading = false;
          this.successo = true;
          this.errore = false;
          this.prodottoId = null; 
          this.cdr.detectChanges();
        },
        error: (err) => {
          // Errore: il backend ha risposto 400, 404 o 500
          this.loading = false;
          this.successo = false;
          this.errore = true;

          // LOGICA DI ESTRAZIONE MESSAGGIO DAL BACKEND
          if (err.error && err.error.detail) {
            // Legge il detail della HTTPException di FastAPI
            this.messaggioErrore = err.error.detail;
          } else if (typeof err.error === 'string') {
            this.messaggioErrore = err.error;
          } else {
            // Fallback se il server non risponde o crasha
            this.messaggioErrore = "Impossibile eliminare il prodotto. Verificare ID o ordini attivi.";
          }
          
          console.error("Dettaglio errore ricevuto:", err);
          this.cdr.detectChanges();
        }
      });
    }
  }

  onReset(): void {
    this.prodottoId = null;
    this.successo = false;
    this.errore = false;
    this.messaggioErrore = '';
    this.cdr.detectChanges();
  }
}