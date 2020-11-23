CREATE TABLE IF NOT EXISTS megabikecrm.vers_all(
	kdnr INT NOT NULL,
    fahrrad VARCHAR(50) NOT NULL,
    rahmennr VARCHAR(30) NOT NULL,
    versicherung VARCHAR(30) NOT NULL,
    PRIMARY KEY (rahmennr)
    );

CREATE TABLE IF NOT EXISTS megabikecrm.vers_assona (
    vertragsnr VARCHAR(20) NOT NULL,
	rahmennr VARCHAR(30) NOT NULL,
    beginn DATE NOT NULL,
    PRIMARY KEY (vertragsnr),
    FOREIGN KEY (rahmennr) REFERENCES vers_all(rahmennr)
    );
    
CREATE TABLE IF NOT EXISTS megabikecrm.vers_businessbike (
    rahmennr VARCHAR(30) NOT NULL,
    nutzer VARCHAR(30) NOT NULL,
    beginn DATE NOT NULL,
    ende DATE NOT NULL,
    policenr VARCHAR(30) NOT NULL,
    paket VARCHAR(30) NOT NULL,
    PRIMARY KEY (policenr),
    FOREIGN KEY (rahmennr) REFERENCES vers_all(rahmennr)
    );
    
CREATE TABLE IF NOT EXISTS megabikecrm.vers_bikeleasing (
    rahmennr VARCHAR(30) NOT NULL,
    nutzer_id VARCHAR(30) NOT NULL,
    paket VARCHAR(30) NOT NULL,
    leasingbank VARCHAR(30) NOT NULL,
    PRIMARY KEY (nutzer_id),
    FOREIGN KEY (rahmennr) REFERENCES vers_all(rahmennr)
    );

CREATE TABLE IF NOT EXISTS megabikecrm.vers_enra (
    nutzer VARCHAR(30) NOT NULL,
    rahmennr VARCHAR(30) NOT NULL,
    beginn DATE NOT NULL,
    policenr VARCHAR(30) NOT NULL,
    PRIMARY KEY (policenr),
    FOREIGN KEY (rahmennr) REFERENCES vers_all(rahmennr)
    );
    
CREATE TABLE IF NOT EXISTS megabikecrm.vers_eurorad (
    vertragsnr INT NOT NULL,
    rahmennr VARCHAR(30) NOT NULL,
	beginn DATE NOT NULL,
    PRIMARY KEY (vertragsnr),
    FOREIGN KEY (rahmennr) REFERENCES vers_all(rahmennr)
    );
    
    
    
    
	