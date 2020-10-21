CREATE DATABASE IF NOT EXISTS megabike_crm;

CREATE TABLE IF NOT EXISTS megabike_crm.rekla(
	auftrag INT PRIMARY KEY,
    angenommen VARCHAR(20),
    ansprechpartner VARCHAR(20),
    kunde VARCHAR(50),
    kd_nr INT,
    hersteller VARCHAR(20),
    gemeldet VARCHAR(20),
    vorgangsnr VARCHAR(30));
    
CREATE TABLE IF NOT EXISTS megabike_crm.rekla_status(
	status_id INT AUTO_increment PRIMARY KEY,
    mitarbeiter VARCHAR(20),
    auftrag INT,
    stand VARCHAR(50),
    anmerkung MEDIUMTEXT,
    datum TIMESTAMP);
    
CREATE OR REPLACE VIEW megabike_crm.rekla_vw
AS SELECT r.auftrag, b.stand, r.angenommen, r.ansprechpartner, r.kunde,
			r.kd_nr, r.hersteller, r.gemeldet, r.vorgangsnr, b.datum
FROM rekla AS r
JOIN (
	SELECT rs.auftrag, rs.stand, rs.datum
	FROM rekla_status AS rs
    WHERE rs.datum = (SELECT max(t2.datum)
						FROM rekla_status AS t2
                        WHERE rs.auftrag = t2.auftrag) 
	GROUP BY rs.auftrag) AS b
ON (b.auftrag = r.auftrag)
ORDER BY auftrag ASC;
    
    