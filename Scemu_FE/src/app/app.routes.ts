import { Routes } from '@angular/router';
import { HomeOrdiniComponent } from './components/ordini-home/ordini-home';
import { Component } from '@angular/core';
import { ProdottiHome } from './components/prodotti-home/prodotti-home';
import{LoginLandingPage} from './components/login-landing-page/login-landing-page'
import { Login } from './components/login/login';
import { Errore } from './components/errore/errore';
import { CercaOrdine } from './components/cerca-ordine/cerca-ordine';
import { AggiornaStatoOrdine } from './components/aggiorna-stato-ordine/aggiorna-stato-ordine';
import { CreaOrdineComponent } from './components/crea-ordine/crea-ordine';
import { AuthGuard } from './guards/auth.guard';
import { CercaProdotto } from './components/cerca-prodotto/cerca-prodotto';
import { EliminaProdotto } from './components/elimina-prodotto/elimina-prodotto';
import { AggiornaProdotto } from './components/aggiorna-prodotto/aggiorna-prodotto';
import { StatisticheComponent } from './components/statistiche/statistiche';



export const routes: Routes = [
    {path : "home" , component : LoginLandingPage},
    {path : "login",component : Login},


/* ELEMENTI PROTETTI */ 

    {path : "ordini" , component : HomeOrdiniComponent , canActivate: [AuthGuard]},
    {path : "prodotti" ,component : ProdottiHome , canActivate: [AuthGuard] },
    {path :"cerca-ordine",component : CercaOrdine , canActivate: [AuthGuard]},
    {path : "aggiorna-stato-ordine", component :AggiornaStatoOrdine},
    {path : "crea-ordine",component :CreaOrdineComponent , canActivate: [AuthGuard]},
    {path :"cerca-prodotto" ,component:CercaProdotto,canActivate: [AuthGuard]},
    {path :"elimina-prodotto",component: EliminaProdotto,canActivate: [AuthGuard]},
    {path : "aggiorna-prodotto" , component : AggiornaProdotto,canActivate: [AuthGuard]},
    {path : "statistiche",component : StatisticheComponent,canActivate: [AuthGuard]},

    


    /* ERRORE : */ 
    {path : "**",component: Errore}



];
