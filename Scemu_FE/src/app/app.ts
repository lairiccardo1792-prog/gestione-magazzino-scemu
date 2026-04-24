import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common'; // Opzionale ma consigliato
// Controlla che il percorso porti al file della navbar
import { NavbarComponent } from './components/navbar/navbar'; 

@Component({
  selector: 'app-root',
  standalone: true,
  // QUI devi inserire NavbarComponent
  imports: [CommonModule, RouterOutlet, NavbarComponent], 
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App { // Deve chiamarsi App perché così è scritto nel main.ts
  title = signal('Ordini_base_API_Alchemy_FE');
}