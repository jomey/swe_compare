CREATE TYPE cbrfc_region AS enum ('UC', 'LC', 'GSL');

ALTER TABLE CBRFC_ZONES_LC RENAME TO cbrfc_zones;

ALTER TABLE cbrfc_zones ADD COLUMN region cbrfc_region;

Update cbrfc_zones SET region = 'LC'; 

INSERT INTO cbrfc_zones (ch5_id, segment, zone, descriptio, fgid, area_mi, area_km, x_centroid, y_centroid, z50_ft, z50_m, zonenum, geom) 
SELECT ch5_id, segment, zone, descriptio, fgid, area_mi, area_km, x_centroid, y_centroid, z50_ft, z50_m, zonenum, geom
FROM cbrfc_zones_uc;

Update cbrfc_zones SET region = 'UC' WHERE region IS NULL; 

INSERT INTO cbrfc_zones (ch5_id, segment, zone, descriptio, fgid, area_mi, area_km, x_centroid, y_centroid, z50_ft, z50_m, zonenum, geom) 
SELECT ch5_id, segment, zone, descriptio, fgid, area_mi, area_km, x_centroid, y_centroid, z50_ft, z50_m, zonenum, geom
FROM cbrfc_zones_GSL;

Update cbrfc_zones SET region = 'GSL' WHERE region IS NULL; 

ALTER TABLE cbrfc_zones ALTER COLUMN region SET NOT NULL;

DROP TABLE cbrfc_zones_uc;
DROP TABLE cbrfc_zones_gsl;
