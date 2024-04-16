# Install via conda
```
conda env create -n postgresql postgis
```

# Create new cluster
```shell
initdb -D /path/to/db_home
```

# (Optional) Allow connections from outside
* Edit `postgresql.conf`
```
listen_addresses = '*'
```
* Edit `pg_hba.conf` and add allowed IP address

# Activate postgis and raster extensions on new DB
```sql
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_raster;
```

# Sample import of NetCDF
Options from:
https://postgis.net/docs/using_raster_dataman.html
`I` -> Create index
`l` -> Overviews

```
raster2pgsql -I -C -e -Y -l 2 -s 4269 -F -t 32x32 NETCDF:"4km_SWE_Depth_WY1982_v01.nc":SWE wy_1982 | psql -h honduras -d swannData
```

# Sample import of Shapefile
https://postgis.net/docs/using_postgis_dbmanagement.html#shp2pgsql_usage
```
shp2pgsql -c -s 4269 -i -I CBRFC_Zones_UC.shp CBRFC_Zones_UC | psql -h honduras -d swannData
```

# Reads
https://www.crunchydata.com/blog/postgres-raster-query-basics