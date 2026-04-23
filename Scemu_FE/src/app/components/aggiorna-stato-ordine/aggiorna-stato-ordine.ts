import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { OrderService } from '../../services/order';
import { StatoOrdine } from '../../models/order.model';
import { RouterLink } from '@angular/router';
import { ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-aggiorna-stato-ordine',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './aggiorna-stato-ordine.html',
  styleUrl: './aggiorna-stato-ordine.css' // Assicurati che il CSS sia collegato
})
export class AggiornaStatoOrdine implements OnInit {
  aggiornaForm: FormGroup;
  loading = false;
  successo = false;
  errore = false;
  messaggio = '';
  
  // Trasformiamo l'Enum in un array per il select HTML
  listaStati = Object.values(StatoOrdine);

  constructor(
    private fb: FormBuilder, 
    private orderService: OrderService,
    private cdr: ChangeDetectorRef
  ) {
    this.aggiornaForm = this.fb.group({
      idOrdine: ['', [Validators.required, Validators.min(1)]],
      nuovoStato: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.onReset(); // Inizia sempre pulito
  }

  onReset(): void {
    this.aggiornaForm.reset({
      idOrdine: '',
      nuovoStato: ''
    });
    this.loading = false;
    this.successo = false;
    this.errore = false;
    this.messaggio = '';
    this.cdr.detectChanges();
  }
onAggiorna(): void {
  if (this.aggiornaForm.invalid || this.loading) return;

  this.loading = true;
  this.successo = false;
  this.errore = false;
  this.messaggio = ''; // Puliamo il messaggio precedente

  const { idOrdine, nuovoStato } = this.aggiornaForm.value;

  this.orderService.aggiornaStato(idOrdine, nuovoStato).subscribe({
    next: (res) => {
      this.loading = false;
      this.successo = true;
      // Caso Successo: Usiamo i dati che tornano dal backend
      this.messaggio = `Ordine #${res.id} passato a ${res.stato.toUpperCase()}`;
      this.cdr.detectChanges();
    },
    error: (err) => {
      this.loading = false;
      this.errore = true;

      // --- QUI GESTIAMO TUTTE LE SITUAZIONI (400, 404, ecc.) ---
      if (err.error && err.error.detail) {
        // Se FastAPI manda un detail (sia per il 404 che per il 400), lo prendiamo!
        this.messaggio = err.error.detail;
      } else {
        // Fallback se il server crasha o non risponde
        this.messaggio = "Errore di comunicazione con il server.";
      }

      console.error("Dettaglio tecnico errore:", err);
      this.cdr.detectChanges();
    }
  });
}
}
