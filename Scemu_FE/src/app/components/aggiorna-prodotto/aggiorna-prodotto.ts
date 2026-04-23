import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ProductService } from '../../services/product'; // Controlla il percorso
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

  categorie = [
    'Elettronica',
    'Abbigliamento',
    'Alimentari',
    'Libri',
    'Sport',
    'Altro'
  ]

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
      prezzo: [0, [Validators.required, Validators.min(0.01)]],
      stock: [0, [Validators.required, Validators.min(1)]],
      categoria: ['', Validators.required],
      attivo: [true],
    });
  }

  ngOnInit(): void {
    this.loadProdotti();
  }

  loadProdotti() {
    this.productService.getProdotti().subscribe({
      next: (res: any) => {
        console.log('Dati ricevuti:', res);
        // Usiamo una variabile di supporto per analizzare la risposta
        let datiEstratti: any[] = [];

        if (Array.isArray(res)) {
          // Se è già un array, lo prendiamo così com'è
          datiEstratti = res;
        } else if (res && typeof res === 'object') {
          // Se è un oggetto, cerchiamo l'array al suo interno.
          // Controlliamo le proprietà più comuni che i backend restituiscono
          datiEstratti = res.prodotti || res.data || res.items || [res];
        }

        // Ora assegniamo il risultato finale al nostro array del componente
        this.prodotti = datiEstratti;

        // 3. Forza Angular a rinfrescare l'interfaccia
        this.cdr.detectChanges();

        console.log('Array prodotti finale:', this.prodotti);
      },
      error: (err) => {
        console.error('Errore caricamento prodotti', err);
      },
    });
  }

  onProdottoChange(event: any) {
    // Recuperiamo il valore e assicuriamoci che sia pulito
    const idGrezzo = event.target.value;

    // Se l'ID è numerico, convertiamolo in numero per eliminare spazi o caratteri extra
    const idPulito = parseInt(idGrezzo, 10);

    if (!isNaN(idPulito)) {
      this.selectedProductId = idPulito; // <---- SALVIAMO L'ID QUI

      this.productService.getProdottoById(idPulito).subscribe({
        next: (p) => {
          this.prodottoForm.patchValue({
            id: p.id,
            nome: p.nome, // Se il tuo form ha anche il campo nome
            prezzo: p.prezzo,
            stock: p.stock,
            categoria: p.categoria,
          });
        },
        error: (err) => {
          console.error('Errore nel recupero del dettaglio prodotto', err);
        },
      });
    } else {
      console.warn('ID non valido rilevato:', idGrezzo);
    }
  }

  onCategoriaChange(event: any){
    const newCategoria = event.target.value
    if(newCategoria){
      this.prodottoForm.patchValue({
        categoria: newCategoria
      });

      console.log('Categoria Aggiornata: ', newCategoria);
    }

  }

  onSubmit() {
    if (this.prodottoForm.valid && this.selectedProductId) {
      const datiAggiornati = this.prodottoForm.value;

      // Passiamo l'ID salvato separatamente al servizio
      this.productService.aggiornaProdotto(this.selectedProductId, datiAggiornati).subscribe({
        next: (res) => {
          alert('Prodotto aggiornato con successo!');
          console.log('Aggiornamento riuscito!', res);
          this.router.navigate(['/prodotti']); // Torna alla lista
        },
        error: (err) => console.error("Errore durante l'aggiornamento:", err),
      });
    }
  }
}