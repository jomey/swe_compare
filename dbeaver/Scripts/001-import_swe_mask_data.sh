#!/usr/bin/env bash

raster2pgsql -I -C -e -Y -s 4629 -F -t 32x32 SWE_Mask_v01.nc swann_swe_mask | psql -h honduras -d swannData