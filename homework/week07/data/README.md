# Week 07 Data

For this assignment I'm looking at white-tailed deer in North Carolina and chronic wasting disease (CWD). CWD is a deadly disease that spreads between deer, and the NC Wildlife Resources Commission (NCWRC) tracks which counties have it. I want to look at where deer are being seen, where they're being hunted, and how public hunting land overlaps with the CWD counties.

Here's what's in the data folder and where each file came from.

## 1. NC County Boundaries

**File:** `nc_counties/nc_counties.shp` (shapefile)

Polygons for all 100 counties in North Carolina. I'm using this as the base layer for most of my maps and joins.

**Source:** NC OneMap, https://www.nconemap.gov

## 2. NCWRC Game Lands

**File:** `gamelands/Game_Lands.shp` (shapefile)

Polygons of the game lands managed by NCWRC. These are public lands used for hunting, trapping, and fishing. This version has the boundaries combined by game land name, so each game land is one shape.

**Source:** NCWRC Game Lands (general), NC OneMap, https://data-nconemap.opendata.arcgis.com/datasets/ncwrc::ncwrc-game-lands-general/about

## 3. White-tailed Deer Observations

**File:** `deer_observations.csv`

Points of white-tailed deer (*Odocoileus virginianus*) sightings in North Carolina. Each row has a latitude and longitude, so I can turn it into a point layer in GeoPandas.

When I downloaded this from GBIF, I filtered it to only include sightings from 2025 in North Carolina that have coordinates. I picked 2025 so it lines up with the deer harvest data. The download had 2,530 sightings, and most of them come from iNaturalist. GBIF gives the file as tab-separated even though it's called a CSV, so I load it with `sep="\t"`.

One thing to know about this data is that it shows where people reported seeing deer, not where all the deer actually are. A lot of the points are probably near cities, parks, and trails because that's where people are.

**Source:** GBIF (Global Biodiversity Information Facility), https://www.gbif.org
GBIF download DOI: https://doi.org/10.15468/dl.hq6c4y

## 4. Deer Harvest by County

**File:** `deer_harvest.csv`

The number of deer hunters reported harvesting in each county during the 2025-26 season. NCWRC only puts this out as a PDF, so I converted the table into a CSV. The PDF breaks the harvest down by weapon type (bow, crossbow, blackpowder, and gun), but I only kept the totals for all weapons combined.

Columns:
- `county`: county name
- `district`: NCWRC wildlife district number
- `antlered_buck`: number of bucks with antlers
- `antlerless_male`: number of males without antlers (like young bucks)
- `antlerless_female`: number of does
- `total_harvest`: total deer harvested in the county

**Source:** NCWRC, 2025-2026 Reported White-tailed Deer Harvest, https://ncwildlife.gov/media/5232/download?attachment=

## 5. CWD Counties

**File:** `cwd_counties.csv`

A small table I made myself with each county that has a CWD designation for the 2026-27 hunting season and what type of area it is. There are two types:

- **CWD Management Area:** Cumberland, Forsyth, Sampson, Stokes, Surry, Wilkes, and Yadkin
- **CWD Surveillance Area:** Edgecombe, Halifax, Martin, and Pitt

**Source:** NCWRC, CWD Surveillance Areas and Special Regulations, https://www.ncwildlife.gov/connect/have-wildlife-problem/preventing-wildlife-conflicts/common-wildlife-diseases/deer-diseases/chronic-wasting-disease/cwd-surveillance-areas-and-special-regulations

All data was downloaded in October 2026.