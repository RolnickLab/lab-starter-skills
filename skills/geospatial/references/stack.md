# Tech Stack

| Category | Library | Purpose |
| :--- | :--- | :--- |
| **Vector** | `geopandas` (>=1.0) | DataFrame API; `pyogrio` is the default I/O engine. |
| | `shapely` (>=2.0) | Vectorized geometry engine. |
| | `duckdb` (spatial ext.) | SQL over large GeoParquet. |
| **Raster** | `rasterio` | GDAL-based I/O. |
| | `rioxarray` + `xarray` | Labeled N-d arrays with CRS. |
| | `exactextract` | Zonal statistics. |
| **Scaling** | `dask`, `dask-geopandas` | Parallel/out-of-core processing. |
| **Cloud** | `pystac-client` | Search STAC APIs. |
| | `odc-stac` (or `stackstac`) | STAC items → lazy xarray. |
| **ML** | `torchgeo` | Geospatial datasets, samplers, pretrained weights. |
| **Viz** | `folium`, `lonboard`, `mapclassify` | Quick maps, large vector viz, choropleth classes. |
| **Point Cloud** | `pdal` | Point cloud pipelines. |

## Forbidden Patterns
- **Hardcoded target CRS:** `dst_crs = 'EPSG:3857'` buried in processing code.
  - *Fix:* Set it in config, or derive it (`gdf.estimate_utm_crs()`).
- **Ignoring transforms:** Reading a raster into numpy without keeping the `transform` loses its location on Earth.
- **Pickling spatial objects:** Persist as GeoParquet/GeoTIFF instead.
