# Applications: Data and Method Lookup

| Application | Data | Method / Gotcha |
| :--- | :--- | :--- |
| Mineral mapping | SWIR, hyperspectral (EnMAP, EMIT) | Spectral unmixing, band ratios for clays, carbonates, iron oxides. |
| Faults, lineaments | SAR, DEMs | Hillshade from multiple azimuths; SAR geometry distorts steep terrain. |
| Landslides, erosion | LiDAR DTM, InSAR | Slope/curvature derivatives; InSAR for slow movement. |
| Crop health, nitrogen | Sentinel-2 Red Edge | NDRE over NDVI in dense canopy. |
| Phenology | HLS or Sentinel-2 time series | Smooth noisy series (Savitzky-Golay) before extracting season start/end. |
| Forest biomass | GEDI, L/P-band SAR, airborne LiDAR | Calibrate with field plots; optical saturates at high biomass. |
| Deforestation | Sentinel-1 + Sentinel-2 | SAR fills gaps in cloudy tropics. |
| Flood mapping | Sentinel-1 | Low VV backscatter = open water; urban and vegetated floods need care (double bounce). |
| Water quality | Sentinel-2, Landsat | Chlorophyll-a, TSM; needs water-specific atmospheric correction (ACOLITE, C2RCC). |
| Snow, glaciers | Sentinel-2 (NDSI), SAR | Feature tracking or InSAR for glacier velocity. |
| Land cover | Sentinel-2, Landsat | Spatial CV; check against existing products (ESA WorldCover, Dynamic World). |
| Urban heat | Landsat thermal (ST band) | Land surface temperature, not air temperature. |
| Subsidence | Sentinel-1 InSAR (PSI, SBAS) | Mm-level, needs long stacks; reports line-of-sight motion only. |
