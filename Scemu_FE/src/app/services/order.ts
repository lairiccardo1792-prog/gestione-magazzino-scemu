// src\app\services\order.ts


import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { OrdineResponse, OrdineCreate, StatoOrdine } from '../models/order.model';

@Injectable({
  providedIn: 'root',
})
export class OrderService {
  private apiUrl = 'http://localhost:8000/ordini';

  constructor(private http: HttpClient) {}

  /**
   * GET /ordini
   * Combacia con il return del tuo CRUD (totale + lista ordini)
   */
  getOrdini(
    stato?: StatoOrdine,
    email?: string,
    skip: number = 0,
    limit: number = 10
  ): Observable<{ totale: number; ordini: OrdineResponse[] }> {
    let params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());

    if (stato) params = params.set('stato', stato);
    if (email) params = params.set('email', email);

    return this.http.get<{ totale: number; ordini: OrdineResponse[] }>(this.apiUrl, { params });
  }

  /**
   * GET /ordini/{ordine_id}
   * Usa i backticks per iniettare l'ID correttamente
   */
  getOrdineById(id: number): Observable<OrdineResponse> {
    // CORRETTO: aggiunto ` ` invece di ' '
    return this.http.get<OrdineResponse>(`${this.apiUrl}/${id}`);
  }

  /**
   * POST /ordini
   * Combacia con OrdineCreate (cliente + array di righe semplificate)
   */
  creaOrdine(ordine: OrdineCreate): Observable<OrdineResponse> {
    return this.http.post<OrdineResponse>(this.apiUrl, ordine);
  }

  /**
   * PATCH /ordini/{ordine_id}/stato
   * Combacia con aggiorna_stato_ordine nel CRUD
   */
  aggiornaStato(id: number, nuovoStato: StatoOrdine): Observable<OrdineResponse> {
    const params = new HttpParams().set('nuovo_stato', nuovoStato);
    // CORRETTO: aggiunto ` ` e l'oggetto vuoto {} come body
    return this.http.patch<OrdineResponse>(`${this.apiUrl}/${id}/stato`, {}, { params });
  }
}