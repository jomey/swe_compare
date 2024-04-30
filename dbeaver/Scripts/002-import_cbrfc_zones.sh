#!/usr/bin/env bash

shp2pgsql -c -s 4269 -i -I CBRFC_Zones_UC.shp CBRFC_Zones_UC | psql -h honduras -d swannData
shp2pgsql -c -s 4269 -i -I CBRFC_Zones_LC.shp CBRFC_Zones_LC | psql -h honduras -d swannData
shp2pgsql -c -s 4269 -i -I CBRFC_Zones_GSL.shp CBRFC_Zones_GSL | psql -h honduras -d swannData
