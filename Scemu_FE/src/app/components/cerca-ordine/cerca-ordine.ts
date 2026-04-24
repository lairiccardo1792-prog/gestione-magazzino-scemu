import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router'; // <--- 1. IMPORTA QUESTO
import { OrderService } from '../../services/order';
import { OrdineResponse } from '../../models/order.model';
import { ChangeDetectorRef } from '@angular/core'; // 1. Importa

@Component({
  selector: 'app-cerca-ordine',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink], // <--- 2. AGGIUNGI QUI
  templateUrl: './cerca-ordine.html',
  styleUrl: './cerca-ordine.css',
})
export class CercaOrdine implements OnInit {
  searchForm: FormGroup;
  loading = false;
  ordineTrovato: OrdineResponse | null = null;
  
  // 3. CAMBIA NOME DA 'messaggio' A 'messaggioErrore' PER L'HTML
  messaggioErrore = ''; 
  errore = false;

  constructor(private fb: FormBuilder, private orderService: OrderService,private cdr: ChangeDetectorRef) {
    this.searchForm = this.fb.group({
      idOrdine: ['', [Validators.required, Validators.min(1)]]
    });
  }

  get f() { return this.searchForm.controls; }

  ngOnInit(): void { this.onReset(); }

  onReset(): void {
    this.searchForm.reset();
    this.ordineTrovato = null;
    this.messaggioErrore = '';
    this.errore = false;
    this.loading = false;
  }


onSubmit(): void {
  // 1. Controllo validità form (Istantaneo)
  this.searchForm.markAllAsTouched();
  if (this.searchForm.invalid || this.loading) return;

  // 2. RESET TOTALE (Qui sta la velocità)
  // Spegniamo tutto subito: l'utente vede la pagina pulirsi all'istante
  this.loading = true;
  this.errore = false; 
  this.messaggioErrore = '';
  this.ordineTrovato = null;

  const id = this.searchForm.value.idOrdine;

  this.orderService.getOrdineById(id).subscribe({
    next: (res) => {
      this.loading = false;
      if (res) {
        this.ordineTrovato = res;
        this.errore = false; // Confermiamo che non c'è errore
      } else {
        // Caso in cui il server risponde 200 ma senza dati
        this.errore = true;
        this.messaggioErrore = "Ordine non trovato.";
      }
      this.cdr.detectChanges();
    },
    error: (err) => {
      this.loading = false;
      this.ordineTrovato = null;
      this.errore = true; // ACCENDIAMO l'errore solo qui

      if (err.status === 404) {
        this.messaggioErrore = "ID non esistente.";
      } else {
        this.messaggioErrore = "Errore di connessione al server.";
      }
      
      this.cdr.detectChanges();
    }
  });
}
}