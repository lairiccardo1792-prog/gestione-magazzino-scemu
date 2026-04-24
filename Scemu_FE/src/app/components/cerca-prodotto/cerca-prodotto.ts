
import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { ProductService } from '../../services/product'; // Assicurati che il percorso sia corretto
import { ProdottoResponse } from '../../models/product.model'; // Assicurati che il percorso sia corretto

@Component({
  selector: 'app-cerca-prodotto',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './cerca-prodotto.html',
  styleUrl: './cerca-prodotto.css'
})
export class CercaProdotto implements OnInit {
  searchForm: FormGroup;
  loading = false;
  prodottoTrovato: ProdottoResponse | null = null;
  
  messaggioErrore = '';
  errore = false;

  constructor(
    private fb: FormBuilder, 
    private productService: ProductService,
    private cdr: ChangeDetectorRef
  ) {
    this.searchForm = this.fb.group({
      idProdotto: ['', [Validators.required, Validators.min(1)]]
    });
  }

  get f() { return this.searchForm.controls; }

  ngOnInit(): void {
    this.onReset();
  }

  onReset(): void {
    this.searchForm.reset();
    this.prodottoTrovato = null;
    this.messaggioErrore = '';
    this.errore = false;
    this.loading = false;
  }

  onSubmit(): void {
    this.searchForm.markAllAsTouched();
    if (this.searchForm.invalid || this.loading) return;

    this.loading = true;
    this.errore = false;
    this.messaggioErrore = '';
    this.prodottoTrovato = null;

    const id = this.searchForm.value.idProdotto;

    this.productService.getProdottoById(id).subscribe({
      next: (res) => {
        console.log(res)
        this.loading = false;
        if (res) {
          this.prodottoTrovato = res;
        } else {
          this.errore = true;
          this.messaggioErrore = "Prodotto non trovato.";
        }
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.loading = false;
        this.prodottoTrovato = null;
        this.errore = true;

        if (err.status === 404) {
          this.messaggioErrore = `Il prodotto con ID ${id} non esiste a database.`;
        } else {
          this.messaggioErrore = "Errore di comunicazione con il server.";
        }
        this.cdr.detectChanges();
      }
    });
  }
}