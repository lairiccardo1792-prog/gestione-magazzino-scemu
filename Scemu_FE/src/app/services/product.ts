import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ProdottoResponse, ProdottoCreate, ProdottoUpdate } from '../models/product.model';

@Injectable({
  providedIn: 'root'
})

export class ProductService {
  private apiUrl = 'http://localhost:8000/prodotti';

  constructor(private http: HttpClient) {}

  getProdotti(skip: number = 0, limit: number = 10): Observable<{
    totale: number, 
    skip: number, 
    limit: number, 
    prodotti: ProdottoResponse[]
  }> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    
    return this.http.get<{
      totale: number, 
      skip: number, 
      limit: number, 
      prodotti: ProdottoResponse[]
    }>(this.apiUrl, { params });
  }

  
  getProdottoById(id: number): Observable<ProdottoResponse> {
    return this.http.get<ProdottoResponse>(`${this.apiUrl}/${id}`);
  }

  creaProdotto(prodotto: ProdottoCreate): Observable<ProdottoResponse> {
    return this.http.post<ProdottoResponse>(this.apiUrl, prodotto);
  }

  aggiornaProdotto(prd: number, dati: ProdottoUpdate): Observable<ProdottoResponse> {
    return this.http.patch<ProdottoResponse>(`${this.apiUrl}/${prd}`, dati);
  }

  eliminaProdotto(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}