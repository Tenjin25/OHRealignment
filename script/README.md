# Data Processing Scripts

This folder contains Python scripts to process Ohio election data.

## Scripts

### 1. create_geojson.py
Converts the Ohio county shapefile to GeoJSON format.

**Usage:**
```bash
python script/create_geojson.py
```

**Output:**
- Creates `data/ohio_counties.geojson`

### 2. transform_election_data.py
Transforms Ohio election CSV files into a nested JSON structure with metadata and results organized by year.

**Usage:**
```bash
python script/transform_election_data.py
```

**Output:**
- Creates `data/ohio_election_results.json`

## Installation

Install required packages:
```bash
pip install -r script/requirements.txt
```

## Data Structure

The transformed JSON follows this structure:
```json
{
  "metadata": {
    "state": "Ohio",
    "state_code": "OH",
    "total_counties": 88,
    "years_covered": [2000, 2002, ...],
    "data_source": "Ohio Secretary of State",
    "generated_date": "2026-02-01"
  },
  "results_by_year": {
    "2024": {
      "president": {
        "president_2024": {
          "contest_name": "PRESIDENT",
          "results": {
            "County Name": {
              "county": "County Name",
              "year": "2024",
              "dem_candidate": "Name",
              "rep_candidate": "Name",
              "dem_votes": 12345,
              "rep_votes": 12345,
              "margin": 123,
              "margin_pct": 1.23,
              "winner": "REP",
              "competitiveness": {
                "category": "Lean Republican",
                "party": "Republican",
                "code": "R_LEAN",
                "color": "#fc9272"
              }
            }
          }
        }
      }
    }
  }
}
```

## Competitiveness Categories

- **Safe** (±20% or more): Deep red/blue
- **Likely** (±10-20%): Moderate red/blue
- **Lean** (±5-10%): Light red/blue
- **Toss-up** (<5%): Very light colors
