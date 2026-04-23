import { Component, OnInit, ChangeDetectorRef } from '@angular/core'; // Aggiunto ChangeDetectorRef
import { StatisticheService } from '../../services/api.service';
import { CommonModule } from '@angular/common'; 
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-statistiche',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './statistiche.html',
  styleUrls: ['./statistiche.css']
})
export class StatisticheComponent implements OnInit {
  stats: any = null;
  loading: boolean = true;
  errore: string | null = null;

  // Iniettiamo il cdr per forzare l'aggiornamento della grafica
  constructor(
    private statsService: StatisticheService,
    private cdr: ChangeDetectorRef 
  ) { }

  ngOnInit(): void {
    this.caricaDati();
  }

  caricaDati() {
    this.loading = true;
    this.errore = null;
    
    console.log("STATISTICHE: Avvio chiamata al service...");

    this.statsService.getTutte().subscribe({
      next: (data) => {
        console.log("%c STATISTICHE: Dati ricevuti con successo! ", "background: #222; color: #bada55", data);
        
        // Salviamo i dati
        this.stats = data;
        
        // Spegniamo il loading con un micro-ritardo per sicurezza
        setTimeout(() => {
          this.loading = false;
          this.cdr.detectChanges(); // <--- SVEGLIA ANGULAR
          console.log("STATISTICHE: Loading impostato a FALSE e grafica aggiornata.");
        }, 50);
      },
      error: (err) => {
        console.error("STATISTICHE: Errore durante la chiamata!", err);
        this.errore = "Impossibile caricare i dati dal server.";
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }
}