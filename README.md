# Ohio Political Realignment Visualization (2000-2024)

An interactive data visualization project exploring Ohio's dramatic political transformation from swing state to Republican stronghold, featuring 13 years of statewide election data across 88 counties.

![Ohio Election Map](https://img.shields.io/badge/Elections-2000--2024-blue) ![Counties](https://img.shields.io/badge/Counties-88-green) ![Data%20Points](https://img.shields.io/badge/Data%20Points-10%2C000%2B-orange)

## 🎯 Project Overview

This project visualizes Ohio's political realignment from 2000-2024, showing how the state went from deciding the 2004 presidential election to becoming a Safe Republican state with R+11 margins. The interactive map reveals county-level patterns, working-class voter shifts, and the collapse of the New Deal Democratic coalition in industrial America.

**Key Findings:**
- Ohio swung **15.9 points** toward Republicans from 2008 (D+4.6%) to 2024 (R+11.3%)
- Mahoning County (Youngstown) flipped from D+28.37% (2012) to R+9.45% (2024) - a **37.82-point swing**
- Trumbull County shifted **39.88 points** from D+23.00% (2012) to R+16.88% (2024)
- Democrats went from 12 House seats (2008) to 4-5 (2024)

## ✨ Features

### Interactive Map
- **88 Ohio counties** with clickable interactivity
- **Color-coded competitiveness** using 15 categories (Annihilation ≥40% to Tossup <0.5%)
- **County-level details** showing exact vote totals, margins, and percentages
- **Statewide summaries** for each year and office type

### Advanced Controls
- **Year selector**: Browse 13 elections (2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024)
- **Office type filter**: President, U.S. Senate, Governor, and other statewide offices
- **Contest switcher**: View different races within the same year/office
- **View modes**: Map visualization and Research Findings toggle

### Research Findings
- **Data-driven analysis** using exact percentages from the JSON
- **County profiles** for Mahoning, Trumbull, Franklin (Columbus), and Cuyahoga (Cleveland)
- **Historical context** explaining the working-class realignment
- **Demographic analysis** of Ohio's political geography
- **Vice President J.D. Vance** political rise as evidence of Ohio's Republican consolidation

## 📊 Data Sources

### Official Election Results
- **Ohio Secretary of State**: Official certified results (2000-2024)
- **OpenElections Format**: Standardized CSV structure for consistency
- **County-level precision**: Precinct-aggregated data ensuring accuracy

### Geographic Data
- **US Census TIGER/Line**: Official county boundary shapefiles (2020)
- **88 counties**: Complete coverage of Ohio political geography

### Data Coverage
| Year | Presidential | U.S. Senate | Governor | Other Statewide |
|------|-------------|-------------|----------|-----------------|
| 2000 | ✓ | ✓ | | |
| 2002 | | | ✓ | ✓ |
| 2004 | ✓ | | | ✓ |
| 2006 | | ✓ | ✓ | ✓ |
| 2008 | ✓ | | | ✓ |
| 2010 | | ✓ | ✓ | ✓ |
| 2012 | ✓ | ✓ | | |
| 2014 | | | ✓ | ✓ |
| 2016 | ✓ | ✓ | | |
| 2018 | | ✓ | ✓ | ✓ |
| 2020 | ✓ | | | ✓ |
| 2022 | | ✓ | ✓ | ✓ |
| 2024 | ✓ | ✓ | | |

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Web browser (Chrome, Firefox, Safari, Edge)
- Git (for version control)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/OHRealignment.git
cd OHRealignment
```

2. **Create Python virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

3. **Install dependencies**
```bash
pip install pandas geopandas
```

4. **Run local server**
```bash
python -m http.server 8000
```

5. **Open in browser**
```
http://localhost:8000
```

## 🛠️ Project Structure

```
OHRealignment/
├── index.html                          # Main visualization page
├── README.md                           # This file
├── data/
│   ├── ohio_election_results.json     # Transformed election data (nested structure)
│   ├── ohio_counties.geojson          # County boundaries
│   ├── *__oh__general*.csv             # Raw Ohio SOS election results
│   └── tl_2020_39_county20/            # Census TIGER shapefiles
├── script/
│   ├── create_geojson.py               # Convert TIGER shapefile to GeoJSON
│   ├── convert_to_openelections.py    # Convert Ohio SOS CSVs to OpenElections format
│   ├── convert_2004_to_openelections.py # Special handler for 2004 two-file format
│   ├── convert_openelections_to_consolidated.py # Standardize OpenElections CSVs
│   ├── add_2010_senate.py              # Manually add missing 2010 U.S. Senate data
│   ├── transform_election_data.py      # Create nested JSON with competitiveness
│   ├── get_margins.py                  # Extract presidential margins for research
│   └── cleanup_findings.py             # Fix research findings formatting
├── .venv/                              # Python virtual environment
└── .gitignore                          # Git ignore file
```

## 📈 Data Processing Pipeline

### 1. GeoJSON Creation
```bash
python script/create_geojson.py
```
Converts Census TIGER shapefiles to GeoJSON with 88 Ohio counties.

### 2. Election Data Standardization
```bash
# Convert 2004 (special two-file format)
python script/convert_2004_to_openelections.py

# Convert 2022 and 2024
python script/convert_to_openelections.py

# Consolidate all other years
python script/convert_openelections_to_consolidated.py

# Add missing 2010 U.S. Senate
python script/add_2010_senate.py
```

### 3. JSON Transformation
```bash
python script/transform_election_data.py
```
Creates nested JSON with:
- **Vote aggregation** by candidate/party to prevent precinct duplication
- **Margin calculations** using total votes (not just two-party)
- **Competitiveness categories** (15 levels from Annihilation to Tossup)
- **Color coding** matching Minnesota visualization format

### 4. Research Analysis
```bash
python script/get_margins.py
```
Extracts exact presidential margins for key counties (Mahoning, Trumbull, Franklin, Cuyahoga).

## 🎨 Technologies Used

### Frontend
- **HTML5/CSS3**: Responsive design with flexbox layout
- **JavaScript (ES6+)**: Interactive map controls and data filtering
- **Mapbox GL JS**: High-performance vector map rendering
- **Papa Parse**: Client-side CSV parsing (if needed)

### Backend/Processing
- **Python 3.11**: Data processing and transformation
- **Pandas**: Data manipulation and aggregation
- **GeoPandas**: Geographic data processing
- **JSON**: Nested data structure for efficient client-side filtering

### Data Structure
```javascript
{
  "metadata": {
    "generated_date": "2026-02-02",
    "years_covered": ["2000", "2002", ..., "2024"],
    "total_races": 157,
    "counties": 88
  },
  "results_by_year": {
    "2024": {
      "President": {
        "President and Vice President": {
          "results": {
            "Franklin": {
              "total_votes": 823456,
              "dem_votes": 527123,
              "rep_votes": 291234,
              "margin_pct": 28.53,
              "winner": "DEM"
            }
          }
        }
      }
    }
  }
}
```

## 🔍 Key Technical Decisions

### Why Nested JSON?
- **Efficient filtering**: Client-side year/office/contest filtering without reloading
- **Reduced payload**: Single JSON load vs. multiple CSV files
- **Structured data**: Clear hierarchy (year → office → contest → county)

### Vote Aggregation Strategy
Grouped by `(candidate, party)` before summing to prevent precinct-level duplication:
```python
grouped = df.groupby(['county', 'candidate', 'party']).agg({
    'votes': 'sum'
}).reset_index()
```

### Margin Calculation
Uses **total votes** (not two-party total) for accurate percentages:
```python
margin_pct = (winner_votes - runner_up_votes) / total_votes * 100
```

### Competitiveness Categories
15 levels based on margin percentage:
- **Annihilation**: ≥40%
- **Dominant**: 30-40%
- **Stronghold**: 20-30%
- **Safe**: 10-20%
- **Likely**: 5.5-10%
- **Lean**: 1-5.5%
- **Tilt**: 0.5-1%
- **Tossup**: <0.5%

## 📝 Notable Data Challenges Solved

### 1. 2004 Two-File Format
Ohio SOS split 2004 into "Candidate Name List" and "Election Results" files. Solution: Custom merger script with Van Wert county name normalization ("VANWERT" → "Van Wert").

### 2. 2010 Missing U.S. Senate
OpenElections precinct file lacked Senate race. Solution: Manually entered Rob Portman vs. Lee Fisher results for all 88 counties.

### 3. 2020 Party Column Missing
2020 CSV had no party column. Solution: Candidate lookup dictionary with party assignments.

### 4. 2020 President Data Structure
2020 used "President - District 12" instead of "President" key. Solution: Flexible contest key detection in get_margins.py.

### 5. Office Name Variations
Multiple formats (e.g., "Governor/Lieutenant Governor" vs "Governor/LtGovernor"). Solution: Comprehensive office type mapping in flattenElectionJSON().

## 🎓 Research Findings Highlights

### The Great Realignment
Ohio transformed from **D+4.6% (2008)** to **R+11.3% (2024)** - a 15.9-point swing in 16 years.

### Mahoning Valley Case Study
Historic steel union territory (Youngstown) flipped:
- **2012**: D+28.37% (Obama's peak)
- **2016**: D+3.32% (Clinton's collapse)
- **2020**: R+1.90% (THE FLIP)
- **2024**: R+9.45% (Republican consolidation)

### J.D. Vance: Symbol of Ohio's Transformation
From *Hillbilly Elegy* author (2016) → U.S. Senator (2022) → Vice President (2024), showing Ohio's role in national Republican politics.

## 🤝 Contributing

This is an academic project, but suggestions for improvements are welcome:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

## 📜 License

This project is for educational purposes. Election data is public domain from the Ohio Secretary of State. Census TIGER/Line shapefiles are public domain from the U.S. Census Bureau.

## 🙏 Acknowledgments

- **Ohio Secretary of State**: Official election results
- **OpenElections**: Data standardization format
- **U.S. Census Bureau**: TIGER/Line county shapefiles
- **Mapbox**: GL JS mapping library
- **Minnesota Election Visualization**: Design inspiration for nested JSON structure

## 📧 Contact

For questions about this project, please open an issue on GitHub.

---

**Built with data, maps, and Python** | **Visualizing Democracy in Action** 🗳️
