import { Component, OnInit , ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProductService } from '../../services/product'; 
import { ProdottoResponse } from '../../models/product.model';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-prodotti-home',
  standalone: true,
  imports: [CommonModule ,RouterLink],
  templateUrl: './prodotti-home.html',
  styleUrl: './prodotti-home.css'
})
export class ProdottiHome implements OnInit {
  listaProdotti: any[] = []; /*PRONTA A RICEVERE QUALSIASI TIPO DI DATO */
  totaleProdotti: number = 0;
  loading: boolean = true;

  constructor(private productService: ProductService,
  private cd: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    console.log("Inizializzazione caricamento magazzino...");
    
    this.productService.getProdotti(0, 50).subscribe({
      next: (res: any) => {
        console.log("DATI RICEVUTI:", res);

        // Gestione flessibile della risposta (Oggetto vs Array)
        if (res && res.prodotti) {
          // Caso standard del tuo backend (dict con chiave prodotti)
          this.listaProdotti = res.prodotti;
          this.totaleProdotti = res.totale || res.prodotti.length;
        } else if (Array.isArray(res)) {
          // Caso emergenza: il backend manda l'array nudo
          this.listaProdotti = res;
          this.totaleProdotti = res.length;
        }

        // SPEGNI IL CARICAMENTO
        this.loading = false;
        this.cd.detectChanges()  /**aggiunto per non dare problemi all aggiornamentO  */
      },
      error: (err) => {
        console.error("Errore critico durante la chiamata API:", err);
        this.loading = false;
      }
    });
  }
}
