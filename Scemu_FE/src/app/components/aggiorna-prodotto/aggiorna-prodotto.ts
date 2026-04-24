
import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ProductService } from '../../services/product';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-aggiorna-prodotto',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './aggiorna-prodotto.html',
  styleUrl: './aggiorna-prodotto.css',
})
export class AggiornaProdotto implements OnInit {
  prodottoForm: FormGroup;
  idProdotto!: number;
  prodotti: any[] = [];
  selectedProductId: number | null = null;
  erroreMessaggio: string | null = null;

  categorie = ['Elettronica', 'Abbigliamento', 'Alimentari', 'Libri', 'Sport', 'Altro'];

  constructor(
    private route: ActivatedRoute,
    private fb: FormBuilder,
    private productService: ProductService,
    private router: Router,
    private cdr: ChangeDetectorRef,
  ) {
    this.prodottoForm = this.fb.group({
      id: ['', Validators.required],
      nome: ['', Validators.required],
      // AGGIUNTO: Minimo 0.01 e Massimo 99999 per il prezzo
      prezzo: [0, [Validators.required, Validators.min(0.01), Validators.max(99999)]],
      stock: [0, [Validators.required, Validators.min(1), Validators.max(9999)]],
      categoria: ['', Validators.required],
      attivo: [true],
    });
  }

  ngOnInit(): void {
    this.loadProdotti();
  }
  getErrorMessage(controlName: string): string {
    const control = this.prodottoForm.get(controlName);
    if (!control || !control.errors) return '';

    if (control.errors['required']) {
      return 'Campo obbligatorio';
    }
    if (control.errors['min']) {
      return `Valore minimo: ${control.errors['min'].min}`;
    }
    if (control.errors['max']) {
      return `Valore massimo: ${control.errors['max'].max}`;
    }
    if (control.errors['email']) {
      return 'Email non valida';
    }

    return 'Valore non valido';
  }
  loadProdotti() {
    this.productService.getProdotti().subscribe({
      next: (res: any) => {
        let datiEstratti: any[] = [];
        if (Array.isArray(res)) {
          datiEstratti = res;
        } else if (res && typeof res === 'object') {
          datiEstratti = res.prodotti || res.data || res.items || [res];
        }
        this.prodotti = datiEstratti;
        this.cdr.detectChanges();
      },
      error: (err) => console.error('Errore caricamento prodotti', err),
    });
  }

  onProdottoChange(event: any) {
    const idPulito = parseInt(event.target.value, 10);
    if (!isNaN(idPulito)) {
      this.selectedProductId = idPulito;
      this.productService.getProdottoById(idPulito).subscribe({
        next: (p) => {
          this.prodottoForm.patchValue({
            id: p.id,
            nome: p.nome,
            prezzo: p.prezzo,
            stock: p.stock,
            categoria: p.categoria,
          });
        },
        error: (err) => console.error('Errore nel recupero dettaglio', err),
      });
    }
  }

  onCategoriaChange(event: any){
    const newCategoria = event.target.value;
    if(newCategoria){
      this.prodottoForm.patchValue({ categoria: newCategoria });
    }
  }

  onSubmit() {
    this.erroreMessaggio = null;

    if (this.prodottoForm.valid && this.selectedProductId) {
      const datiAggiornati = this.prodottoForm.value;

      this.productService.aggiornaProdotto(this.selectedProductId, datiAggiornati).subscribe({
        next: (res) => {
          alert('Prodotto aggiornato con successo!');
          this.router.navigate(['/prodotti']);
        },
        error: (err) => {
          console.error("Errore:", err);
          this.erroreMessaggio = err.error?.message || err.error || "Errore durante l'aggiornamento. Controlla i dati inseriti.";
        },
      });
    }
  }
}