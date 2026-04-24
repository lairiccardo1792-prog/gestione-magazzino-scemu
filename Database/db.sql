-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versione server:              11.8.6-MariaDB - MariaDB Server
-- S.O. server:                  Win64
-- HeidiSQL Versione:            12.14.0.7165
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dump della struttura del database ordini_base
CREATE DATABASE IF NOT EXISTS `ordini_base` /*!40100 DEFAULT CHARACTER SET utf16 COLLATE utf16_general_ci */;
USE `ordini_base`;

-- Dump della struttura di tabella ordini_base.ordini
CREATE TABLE IF NOT EXISTS `ordini` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `utente_id` int(11) NOT NULL,
  `cliente_nome` varchar(500) NOT NULL,
  `cliente_email` varchar(500) NOT NULL,
  `totale` decimal(10,2) NOT NULL DEFAULT 0.00,
  `stato` varchar(50) NOT NULL,
  `note` text DEFAULT NULL,
  `creato_il` datetime NOT NULL DEFAULT current_timestamp(),
  `aggiornato_il` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_ordini_utenti` (`utente_id`),
  CONSTRAINT `FK_ordini_utenti` FOREIGN KEY (`utente_id`) REFERENCES `utenti` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1014 DEFAULT CHARSET=utf16 COLLATE=utf16_general_ci;

-- Dump dei dati della tabella ordini_base.ordini: ~13 rows (circa)
INSERT INTO `ordini` (`id`, `utente_id`, `cliente_nome`, `cliente_email`, `totale`, `stato`, `note`, `creato_il`, `aggiornato_il`) VALUES
	(1, 1, 'Mario Rossi', 'mario.rossi@email.it', 1259.90, 'spedito', 'Consegnare al mattino', '2026-04-17 17:42:51', NULL),
	(2, 2, 'Luca Bianchi', 'l.bianchi@provider.com', 850.00, 'confermato', NULL, '2026-04-17 17:42:51', NULL),
	(3, 3, 'Elena Verdi', 'elena.v@servizio.it', 475.50, 'consegnato', 'Lasciare in portineria', '2026-04-17 17:42:51', NULL),
	(4, 4, 'Giulia Neri', 'giulia.neri@web.com', 125.50, 'confermato', NULL, '2026-04-17 17:42:51', '2026-04-22 12:05:23'),
	(5, 4, 'Roberto Bruno', 'roberto.b@mail.it', 308.90, 'confermato', 'Urgente', '2026-04-17 17:42:51', NULL),
	(6, 2, 'Alice Gialli', 'alice.g@test.it', 249.00, 'spedito', NULL, '2026-04-17 17:42:51', NULL),
	(7, 5, 'Marco Viola', 'm.viola@company.it', 185.00, 'consegnato', NULL, '2026-04-17 17:42:51', NULL),
	(8, 5, 'Sofia Rosa', 'sofia.r@agency.com', 214.00, 'in_attesa', NULL, '2026-04-17 17:42:51', NULL),
	(9, 5, 'Francesco Blu', 'f.blu@internet.it', 99.00, 'annullato', 'Ordine annullato dal cliente', '2026-04-17 17:42:51', NULL),
	(10, 5, 'Anna Arancio', 'anna.a@shop.it', 215.00, 'in_attesa', NULL, '2026-04-17 17:42:51', NULL),
	(11, 1, 'Elviro', 'elviro@gmail.com', 29.90, 'in_attesa', 'Prova', '2026-04-22 12:29:10', NULL),
	(12, 4, 'Lukino', 'lukino@gmail.com', 18.00, 'in_attesa', 'test', '2026-04-22 12:30:22', NULL),
	(13, 3, 'Federico', 'fede1@gmail.com', 29.90, 'in_attesa', 'prova 3', '2026-04-22 12:33:16', NULL);

-- Dump della struttura di tabella ordini_base.prodotti
CREATE TABLE IF NOT EXISTS `prodotti` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(500) NOT NULL,
  `descrizione` varchar(500) DEFAULT NULL,
  `prezzo` decimal(10,2) NOT NULL,
  `categoria` varchar(250) NOT NULL DEFAULT '',
  `stock` int(11) NOT NULL DEFAULT 0,
  `attivo` int(1) NOT NULL DEFAULT 0,
  `creato_il` datetime NOT NULL,
  `aggiornato_il` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nome` (`nome`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf16 COLLATE=utf16_general_ci;

-- Dump dei dati della tabella ordini_base.prodotti: ~10 rows (circa)
INSERT INTO `prodotti` (`id`, `nome`, `descrizione`, `prezzo`, `categoria`, `stock`, `attivo`, `creato_il`, `aggiornato_il`) VALUES
	(1, 'Laptop Pro 15', 'Laptop alte prestazioni', 1200.00, 'Elettronica', 10, 1, '2026-04-17 17:42:51', NULL),
	(2, 'Smartphone X', 'Display OLED 128GB', 850.00, 'Elettronica', 25, 1, '2026-04-17 17:42:51', NULL),
	(3, 'T-Shirt Sport', 'Tessuto traspirante', 29.90, 'Abbigliamento', 48, 1, '2026-04-17 17:42:51', '2026-04-22 11:33:16'),
	(4, 'Manubri 10kg', 'Coppia manubri gommati', 45.00, 'Sport', 15, 1, '2026-04-17 17:42:51', NULL),
	(5, 'Pasta Integrale 500g', 'Grano 100% italiano', 1.50, 'Alimentari', 100, 1, '2026-04-17 17:42:51', NULL),
	(6, 'Il Nome della Rosa', 'Romanzo di Umberto Eco', 18.00, 'Libri', 29, 1, '2026-04-17 17:42:51', '2026-04-22 11:30:22'),
	(7, 'Monitor 27 QHD', 'Monitor gaming 144Hz', 350.00, 'Elettronica', 12, 1, '2026-04-17 17:42:51', NULL),
	(8, 'Zaino Trekking', 'Capacità 40 litri', 85.00, 'Sport', 8, 1, '2026-04-17 17:42:51', NULL),
	(9, 'Caffè Arabica 250g', 'Torrefazione artigianale', 4.50, 'Libri', 60, 1, '2026-04-17 17:42:51', '2026-04-22 16:37:44'),
	(10, 'Lampada LED', 'Luce calda regolabile', 35.00, 'Altro', 20, 1, '2026-04-17 17:42:51', NULL);

-- Dump della struttura di tabella ordini_base.righe_ordini
CREATE TABLE IF NOT EXISTS `righe_ordini` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ordini_id` int(11) NOT NULL DEFAULT 0,
  `prodotti_id` int(11) NOT NULL DEFAULT 0,
  `nome_prodotto` varchar(50) NOT NULL DEFAULT '0',
  `prezzo_unitario` decimal(10,2) NOT NULL DEFAULT 0.00,
  `quantita` int(6) NOT NULL DEFAULT 0,
  `sub_totale` decimal(10,2) NOT NULL DEFAULT 0.00,
  PRIMARY KEY (`id`),
  KEY `FK_righe_ordini_prodotti` (`prodotti_id`),
  KEY `FK_righe_ordini_ordini` (`ordini_id`),
  CONSTRAINT `FK_righe_ordini_ordini` FOREIGN KEY (`ordini_id`) REFERENCES `ordini` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `FK_righe_ordini_prodotti` FOREIGN KEY (`prodotti_id`) REFERENCES `prodotti` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf16 COLLATE=utf16_general_ci;

-- Dump dei dati della tabella ordini_base.righe_ordini: ~13 rows (circa)
INSERT INTO `righe_ordini` (`id`, `ordini_id`, `prodotti_id`, `nome_prodotto`, `prezzo_unitario`, `quantita`, `sub_totale`) VALUES
	(1, 1, 1, 'Laptop Pro 15', 1200.00, 1, 1200.00),
	(2, 1, 5, 'Mouse Wireless', 59.90, 1, 59.90),
	(3, 2, 2, 'Smartphone X', 850.00, 1, 850.00),
	(4, 3, 3, 'Monitor 27 QHD', 350.00, 1, 350.00),
	(5, 3, 4, 'Tastiera Meccanica', 125.50, 1, 125.50),
	(6, 4, 4, 'Tastiera Meccanica', 125.50, 1, 125.50),
	(7, 5, 5, 'Mouse Wireless', 59.90, 1, 59.90),
	(8, 5, 6, 'Cuffie Noise Cancelling', 249.00, 1, 249.00),
	(9, 6, 6, 'Cuffie Noise Cancelling', 249.00, 1, 249.00),
	(10, 7, 7, 'Stampante Laser', 185.00, 1, 185.00),
	(11, 11, 3, 'T-Shirt Sport', 29.90, 1, 29.90),
	(12, 12, 6, 'Il Nome della Rosa', 18.00, 1, 18.00),
	(13, 13, 3, 'T-Shirt Sport', 29.90, 1, 29.90);

-- Dump della struttura di tabella ordini_base.utenti
CREATE TABLE IF NOT EXISTS `utenti` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf16 COLLATE=utf16_general_ci;

-- Dump dei dati della tabella ordini_base.utenti: ~5 rows (circa)
INSERT INTO `utenti` (`id`, `user`, `password`) VALUES
	(1, 'riccardo', '1234'),
	(2, 'alessio', '1234'),
	(3, 'federico', '1234'),
	(4, 'gianmarco', '1234'),
	(5, 'luca', '1234');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
