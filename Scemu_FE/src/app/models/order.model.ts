export enum StatoOrdine {
  IN_ATTESA = 'in_attesa',
  CONFERMATO = 'confermato',
  SPEDITO = 'spedito',
  CONSEGNATO = 'consegnato',
  ANNULLATO = 'annullato'
}

export interface RigaOrdineCreate {
  prodotto_id: number;
  quantita: number;
}

export interface OrdineCreate {
  cliente_nome: string;
  cliente_email: string;
  righe: RigaOrdineCreate[]; 
}


export interface RigaOrdineResponse {
  id: number;
  prodotto_id: number;
  nome_prodotto: string;
  prezzo_unitario: number;
  quantita: number;
  subtotale: number;
}

export interface OrdineResponse {
  id: number;
  cliente_nome: string;
  cliente_email: string;
  totale: number;
  stato: StatoOrdine;
  note: string | null;
  righe: RigaOrdineResponse[]; 
  creato_il: string;
  aggiornato_il?: string | null;
}


