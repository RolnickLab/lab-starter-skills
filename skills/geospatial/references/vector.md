# Vector Processing

## Formats
- **Preferred:** GeoParquet. Write with `gdf.to_parquet(..., write_covering_bbox=True)` for spatial filter pushdown.
- **Acceptable:** GeoPackage (desktop GIS interchange), GeoJSON (small web interchange), FlatGeobuf (streaming).
- **Avoid:** Shapefile: 2GB limit, 10-char field names, no real nulls, sidecar files.

## Geometry Validity
- Check `gdf.is_valid.all()` right after loading.
- Fix with `gdf.make_valid()`. Avoid `buffer(0)`: it silently drops parts of self-intersecting (bowtie) polygons. `make_valid` can return GeometryCollections; filter or explode to the expected type.
- Pixel-traced geometries have redundant vertices: `simplify()` (in a projected CRS) or `set_precision()`.

## Spatial Operations
- **Vectorize:** Never `iterrows()` (orders of magnitude slower).
  - *Bad:* `[row.geometry.buffer(10) for _, row in gdf.iterrows()]`
  - *Good:* `gdf.buffer(10)`
  - `apply()` is still a Python loop: last resort.
- **Spatial index:** `gdf.sindex` (shapely STRtree) is built lazily and used automatically by `sjoin`, `overlay`, `clip`. Use `sindex.query()` directly for custom candidate searches.
- **Predicates:** Choose deliberately: `intersects` vs `within` vs `contains` vs `touches` change join results.

## Large Data
- Larger than memory: `dask-geopandas` (spatially partitioned) or DuckDB spatial (SQL over GeoParquet).
- Visualizing millions of features: `lonboard` or `datashader`, not matplotlib/folium.
