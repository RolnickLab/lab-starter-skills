# Coordinate Reference Systems (CRS)

## Rules
1. **Never assume:** If data lacks a `.prj` or CRS metadata, do not guess. Ask the source.
2. **Common CRS:** Transform all layers to one CRS before spatial operations (intersection, distance, joins).
3. **Axis order:** EPSG:4326 is officially (lat, lon); most software expects (x, y) = (lon, lat). Use `pyproj.Transformer.from_crs(..., always_xy=True)`.

## Common EPSG Codes
| Code | Name | Unit | Usage |
| :--- | :--- | :--- | :--- |
| **4326** | WGS 84 | Degrees | Storage, GPS data. **Bad for analysis.** |
| **3857** | Web Mercator | Meters | Web map tiles only. **Bad for area/distance** (huge distortion at high latitudes). |
| **326xx / 327xx** | UTM zones (N/S) | Meters | Local analysis within one zone. |
| **5070** | NAD83 / Conus Albers | Meters | Equal-area, US. |
| **3035** | ETRS89 / LAEA Europe | Meters | Equal-area, Europe. |

## Area, Distance, Buffers
- **Area:** Equal-area CRS (Albers, LAEA), or geodesic `pyproj.Geod(ellps="WGS84").geometry_area_perimeter()`.
- **Distance:** Local: UTM. Regional/global: geodesic `pyproj.Geod.inv()` (Karney, accurate everywhere). Haversine is spherical (~0.5% error); Vincenty can fail near antipodes.
- **Buffer:** Project to local UTM (`gdf.estimate_utm_crs()`), buffer in meters, project back.
- Data spanning several UTM zones: use a regional equal-area or custom projection, not one zone.
