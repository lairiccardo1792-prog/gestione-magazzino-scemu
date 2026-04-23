import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, FormArray, Validators, ReactiveFormsModule } from '@angular/forms';
import { OrderService } from '../../services/order';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-crea-ordine',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './crea-ordine.html',
  styleUrl: './crea-ordine.css'
})
export class CreaOrdineComponent implements OnInit {
  ordineForm!: FormGroup;
  loading = false;
  successo = false;
  errore = false;
  messaggio = '';

  constructor(
    private fb: FormBuilder, 
    private orderService: OrderService,
    private cdr: ChangeDetectorRef
  ) {
    this.initForm();
  }

  ngOnInit(): void {
    console.log("Componente caricato e Form pronto!");
  }

  initForm() {
    this.ordineForm = this.fb.group({
      cliente_nome: ['', [Validators.required, Validators.minLength(3)]],
      cliente_email: ['', [Validators.required, Validators.email]],
      note: [''],
      righe: this.fb.array([this.creaRiga()])
    });
  }

  creaRiga(): FormGroup {
    return this.fb.group({
      prodotto_id: [null, [Validators.required, Validators.min(1)]],
      quantita: [1, [Validators.required, Validators.min(1),Validators.max(9999)]]
    });
  }

  get righe() {
    return this.ordineForm.get('righe') as FormArray;
  }

  aggiungiProdotto() {
    this.righe.push(this.creaRiga());
    this.cdr.detectChanges();
  }

  rimuoviProdotto(index: number) {
    if (this.righe.length > 1) {
      this.righe.removeAt(index);
      this.cdr.detectChanges();
    }
  }

  onReset() {
    this.initForm();
    this.successo = false;
    this.errore = false;
    this.messaggio = '';
    this.cdr.detectChanges();
  }

  onSubmit() {
    if (this.ordineForm.invalid) return;
    this.loading = true;
    
    this.orderService.creaOrdine(this.ordineForm.value).subscribe({
      next: (res) => {
        this.loading = false;
        this.successo = true;
        this.messaggio = `Ordine creato con successo! ID: #${res.id}`;
        this.ordineForm.reset();
        this.initForm();
        this.cdr.detectChanges();
      },
      error: (err) => {
  this.loading = false;
  this.errore = true;
  
  console.error("Dettaglio tecnico errore:", err);

  // LOGICA PER ESTRARRE IL TESTO
  if (err.error && typeof err.error.message === 'string') {
    this.messaggio = err.error.message;
  } else if (err.error && typeof err.error.detail === 'string') {
    this.messaggio = err.error.detail;
  } else if (typeof err.error === 'string') {
    this.messaggio = err.error;
  } else {
    this.messaggio = "Errore: quantità non disponibile o dati non validi.";
  }

  this.cdr.detectChanges();
}
    });
  }
}