CREATE OR REPLACE FUNCTION public.mask_for_zone(zone_name text)
 RETURNS TABLE(id integer, val double precision, geom geometry)
 LANGUAGE sql
AS $function$
    WITH cbrfc_zone AS (
        select geom from cbrfc_zones czu where zone = zone_name
    ),
    zone_buffer AS (
        SELECT st_buffer(st_envelope(cbrfc_zone.geom), 0.05) AS geom FROM cbrfc_zone
    ),
    swann_pixels AS (
        SELECT generate_series(0,1000) AS ID, 
            (ST_PixelAsPolygons(
                ST_CLIP(
                    ssm.rast,
                    zone_buffer.geom
                )
            )).*
        FROM swann_swe_mask ssm, zone_buffer
    )
    SELECT swann_pixels.id, swann_pixels.val, swann_pixels.geom
    FROM cbrfc_zone, swann_pixels
    WHERE ST_Intersects(swann_pixels.geom, cbrfc_zone.geom); 
$function$
;
