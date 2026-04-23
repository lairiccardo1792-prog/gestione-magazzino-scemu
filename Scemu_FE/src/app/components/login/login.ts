// ===== COMPONENTE LOGIN: Form di login che raccoglie user/password e chiama il backend =====
// Flusso: Utente digita username/password → premi invio → componente manda richiesta al backend
// → backend controlla le credenziali → manda back il token → componente salva token in localStorage

// 1. IMPORTIAMO GLI STRUMENTI
import { Component ,OnInit, ChangeDetectorRef } from '@angular/core';  // Component e OnInit (lifecycle hook)
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';  // Per i form reattivi
import { RouterLink , Router} from '@angular/router';  // Router = per navigare tra pagine
import { HttpErrorResponse } from '@angular/common/http';  // Tipo per errori HTTP (non usato qui)
import { AuthService } from '../../services/auth.service';  // AuthService = il servizio che fa la chiamata al backend
import { CommonModule } from '@angular/common';  // CommonModule = *ngIf, *ngFor, ecc
import { LoginDialog } from '../login-dialog/login-dialog';  // LoginDialog = componente di dialogo (OK/ERRORE)

// 2. DEFINIAMO IL COMPONENTE
@Component({  // @Component = decoratore che dice "questo è un componente Angular"
  selector: 'app-login',  // <app-login></app-login> = come usare questo componente nell'HTML
  imports: [RouterLink,ReactiveFormsModule,CommonModule,LoginDialog],  // Importa questi moduli nel componente
  templateUrl: './login.html',  // File HTML del template
  styleUrl: './login.css',  // File CSS degli stili
  standalone: true  // standalone = questo componente non ha bisogno di un modulo wrapper
})
export class Login {  // La classe del nostro componente

  // ===== PROPRIETÀ DEL COMPONENTE =====
  // Queste variabili controllano cosa vede l'utente e cosa succede quando cliccano

  loginForm: FormGroup;  // Il form di login (username + password)
  loading = false;  // true = "sto caricando la risposta dal server", false = "sono libero"
  hidePassword = true;  // true = mostra puntini, false = mostra il testo della password

  showDialog = false;  // true = mostra il dialogo (OK o ERRORE)
  dialogSuccess = false;  // true = login riuscito (mostra OK), false = errore
  dialogMessage = '';  // Il messaggio nel dialogo (es: "Benvenuto mario!" o "Credenziali errate")

  // ===== COSTRUTTORE: Inizializza il componente =====
  // Constructor di cosaè iniettato automaticamente da Angular
  constructor(
    private fb: FormBuilder,  // FormBuilder = strumento per creare form reattivi
    private servizio: AuthService,  // AuthService = il servizio che chiama il backend
    private router: Router,  // Router = per navigare a /ordini dopo login
    private cdr: ChangeDetectorRef  // ChangeDetectorRef = per aggiornare la view (il template HTML)
  ) {
    // CREIAMO IL FORM DI LOGIN
    this.loginForm = this.fb.group({  // fb.group = crea un form con questi campi
      user: ['', [Validators.required, Validators.minLength(3)]],  // Campo username: obbligatorio, minimo 3 caratteri
      password: ['', [Validators.required, Validators.minLength(4)]],  // Campo password: obbligatorio, minimo 4 caratteri
    });  // Questo crea un oggetto { user: '', password: '' }
  }

  // ===== GETTER PER ACCEDERE AI CONTROLLI DEL FORM =====
  // Scorciatoia per accedere ai controlli: non usata qui, ma può servire nell'HTML
  get f() {  // Nel template HTML puoi usare f.user, f.password, ecc
    return this.loginForm.controls;
  }

  // ===== LIFECYCLE HOOK: Eseguito quando il componente si carica =====
  ngOnInit(): void {  // ngOnInit = Angular chiama questo automaticamente all'avvio
    setTimeout(() => {  // Aspetta 150ms prima di eseguire
      this.onReset();  // Resetta il form (svuota i campi)
      console.log("Eseguito automaticamente all'avvio!");  // Log per debug
    }, 150);
  }

  // ===== FUNZIONE: Resetta il form =====
  onReset(): void {  // Pulisce il form
    this.loginForm.reset();  // Svuota tutti i campi
    this.loginForm.markAsPristine();  // Ricorda che non è "sporco" (l'utente non ha digitato nulla)
    this.loginForm.markAsUntouched();  // Ricorda che nessun campo è stato "toccato"
  }

  // ===== FUNZIONE: Quando l'utente clicca il pulsante "Login" =====
  onSubmit(): void {  // onSubmit = il form lo chiama quando clicchi il pulsante submit
    // ===== STEP 1: CONTROLLA SE IL FORM È VALIDO =====
    console.log('1. Pulsante premuto');  // Log: debug
    if (this.loginForm.invalid || this.loading) return;  // Se il form non è valido O stiamo già caricando → STOP
    // (Esempio form non valido: username < 3 caratteri oppure password < 4)

    console.log('2. Form non valido:', this.loginForm.errors);  // Log: mostra errori (se ce ne sono)
    this.loading = true;  // Imposta loading = true (mostrerà un "caricamento..." all'utente)

    // ===== STEP 2: MANDA I DATI AL BACKEND =====
    console.log('3. Invio dati al servizio:', this.loginForm.value);  // Log: i dati che mandiamo
    // loginForm.value = { user: "mario", password: "1234" }
    // servizio.login() chiama il backend con POST /login + questi dati
    this.servizio.login(this.loginForm.value).subscribe({  // .subscribe = "ascolta la risposta del server"
      // next = se la richiesta ha successo
      next: (res: any) => {
        console.log('4. Risposta ricevuta dal server:', res);  // Log: la risposta dal backend
        // res = { success: true, message: "Benvenuto mario!", username: "mario", token: "xxx" }
        this.loading = false;  // Finito il caricamento

        // ===== STEP 3: CONTROLLA SE IL LOGIN HA AVUTO SUCCESSO =====
        // Alcuni server mandano success:true, altri solo il token (controlla entrambi)
        this.dialogSuccess = !!(res?.success || res?.token);  // true solo se success=true O token esiste
        this.dialogMessage = res?.message ?? 'Accesso effettuato';  // Il messaggio della risposta (o di default)
        this.showDialog = true;  // Mostra il dialogo (OK o ERRORE)
        this.cdr.detectChanges();  // Aggiorna la view subito (senza aspettare il tick)
      },
      // error = se la richiesta ha fallito (server offline, 500, ecc)
      error: (err) => {
        console.error('4. ERRORE NELLA CHIAMATA:', err);  // Log: l'errore nello console
        this.loading = false;  // Finito il caricamento
        this.dialogSuccess = false;  // Mostra un messaggio di ERRORE
        this.dialogMessage = 'Errore: credenziali non valide o server offline';  // Messaggio di errore
        this.showDialog = true;  // Mostra il dialogo
        this.cdr.detectChanges();  // Aggiorna la view
      }
    });
  }

  // ===== FUNZIONE: Quando l'utente chiude il dialogo =====
  onDialogClosed(): void {  // Chiamata quando clicchi OK o ANNULLA nel dialogo
    this.showDialog = false;  // Nascondi il dialogo

    // Se il login è riuscito → vai alla pagina /ordini
    if (this.dialogSuccess) {  // Se dialogSuccess = true (login OK)
      this.router.navigate(['/ordini']);  // Usa il Router per andare a /ordini
    }
    // Se il login è fallito → rimani sulla pagina e l'utente può riprovare
  }
}