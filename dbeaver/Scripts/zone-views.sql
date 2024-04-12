DO $$
DECLARE
    cbrfc_zone record;
BEGIN
    FOR cbrfc_zone IN 
        SELECT czu.zone AS name 
        FROM cbrfc_zones_uc czu 
        WHERE czu.zone LIKE 'ALEC2%'
    LOOP 
        RAISE NOTICE 'Creating view for zone %', cbrfc_zone.name;
        EXECUTE FORMAT(
            'Create or replace view public.%I AS SELECT * FROM mask_for_zone(%L)',
            cbrfc_zone.name, cbrfc_zone.name
        );
    END LOOP;
END; 
$$
