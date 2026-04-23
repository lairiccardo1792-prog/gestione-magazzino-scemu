export enum Categoria {
  ELETTRONICA = 'Elettronica',
  ABBIGLIAMENTO = 'Abbigliamento',
  ALIMENTARI = 'Alimentari',
  LIBRI = 'Libri',
  SPORT = 'Sport',
  ALTRO = 'Altro'
}

export interface ProdottoBase {
  nome: string;
  descrizione: string;
  prezzo: number;
  categoria: Categoria;
  stock: number;
  attivo: boolean;
}

export interface ProdottoCreate extends ProdottoBase {}


export interface ProdottoUpdate {
  nome?: string;
  descrizione?: string;
  prezzo?: number;
  categoria?: Categoria;
  stock?: number;
  attivo?: boolean;
}

export interface ProdottoResponse extends ProdottoBase {
  id: number;
  creato_il: string;     
  aggiornato_il?: string; 
}