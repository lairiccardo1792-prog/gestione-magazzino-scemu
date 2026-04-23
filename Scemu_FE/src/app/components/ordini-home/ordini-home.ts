import { Component, OnInit, ChangeDetectorRef, ViewEncapsulation } from '@angular/core'; // <--- Aggiungi ViewEncapsulation
import { CommonModule } from '@angular/common';
import { OrderService } from '../../services/order';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-home-ordini',
  standalone: true,
  imports: [CommonModule,RouterModule],
  templateUrl: './ordini-home.html',
  styleUrl: './ordini-home.css'
})
export class HomeOrdiniComponent implements OnInit {
  listaOrdini: any[] = [];
  totaleOrdini: number = 0;
  loading: boolean = true; // Inizia come true

  constructor(
    private orderService: OrderService,
    private cd: ChangeDetectorRef // <--- Aggiungi questo
  ) {}

  ngOnInit(): void {
    this.caricaOrdini();
  }

  caricaOrdini(): void {
    this.loading = true;
    this.orderService.getOrdini().subscribe({
      next: (res: any) => {
        console.log('Dati ricevuti dal backend:', res);
        
        // Mappatura sicura: controlliamo se esiste res.ordini
        if (res && res.ordini) {
          this.listaOrdini = res.ordini;
          this.totaleOrdini = res.totale;
        } else if (Array.isArray(res)) {
          // Se il backend mandasse direttamente l'array invece dell'oggetto
          this.listaOrdini = res;
          this.totaleOrdini = res.length;
        }

        // Sblocchiamo la visualizzazione
        this.loading = false;
        
        // Forza Angular a controllare i cambiamenti nel template
        this.cd.detectChanges(); 
      },
      error: (err) => {
        console.error('Errore API:', err);
        this.loading = false;
        this.cd.detectChanges();
      }
    });
  }
}