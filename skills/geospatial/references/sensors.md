# Remote Sensing Sensors

Constellation status changes; check SentiWiki or USGS before quoting revisit times. Status below as of 2026.

## Optical

### Landsat 8-9 (OLI/TIRS, USGS/NASA)
- 30m (VNIR, SWIR), 15m pan, 100m thermal (delivered at 30m). 12-bit (L8) / 14-bit (L9).
- Revisit 16 days per satellite, 8 days combined. Archive back to 1972 (MSS) for long-term change.
- Landsat 7 ETM+: SLC failure since 2003 causes striped data gaps.

### Sentinel-2 (MSI, ESA)
- 10m (B2, B3, B4, B8), 20m (Red Edge B5-B7, B8A, SWIR B11-B12), 60m (atmospheric B1, B9, B10).
- Revisit 5 days with two satellites (2B and 2C operational since 2025).
- Red Edge bands are key for chlorophyll and vegetation stress.

### Harmonized Landsat Sentinel-2 (HLS, NASA)
- Landsat 8/9 + Sentinel-2 surface reflectance on a common 30m grid with BRDF and bandpass adjustment. Default for dense multi-sensor time series.

### High-Resolution Commercial
- **PlanetScope:** 3m, near-daily. Lower radiometric consistency than Sentinel/Landsat.
- **Maxar WorldView / Legion:** 30-50cm. Tasking, costly.
- **Pléiades Neo:** 30cm.

## SAR

### Sentinel-1 (C-band, ESA)
- Flood mapping, sea ice, InSAR deformation. Works through clouds and at night.
- IW mode is the land default; dual-pol VV+VH over land, HH+HV over polar regions.
- 6-day revisit with 1C and 1D (since mid-2026). 1B lost in 2021, so 2022-2025 archives are mostly 12-day.

### L-band (NISAR, ALOS-2/4)
- Penetrates canopy: biomass, forest structure, deformation in vegetated areas.
- NISAR (NASA-ISRO, L+S band): public L-band data via ASF DAAC since July 2026.

### P-band (ESA BIOMASS, launched 2025)
- Longest wavelength in orbit; designed for forest biomass and height.

## LiDAR & Elevation
- **ICESat-2 (ATLAS):** Photon-counting; ice sheets, canopy height, shallow bathymetry.
- **GEDI (ISS):** Full-waveform; canopy height and structure, ~25m footprints.
- **Airborne/UAV:** 10-100+ pts/m²; bare-earth DTMs, precision forestry, flood modeling.

## Hyperspectral
- **PRISMA, EnMAP, EMIT:** Hundreds of narrow bands (~30-60m); mineral mapping, species discrimination, methane plumes (EMIT).
