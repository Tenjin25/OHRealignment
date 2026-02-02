"""
Transform Ohio election data from OpenElections format into nested JSON format
"""
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import re


def get_competitiveness(margin_pct):
    """Determine competitiveness category based on margin percentage"""
    abs_margin = abs(margin_pct)
    
    # Match exact thresholds from visualization
    if abs_margin >= 40:
        category = "Annihilation"
        code_suffix = "ANNIHILATION"
        r_color = "#67000d"
        d_color = "#08306b"
    elif abs_margin >= 30:
        category = "Dominant"
        code_suffix = "DOMINANT"
        r_color = "#a50f15"
        d_color = "#08519c"
    elif abs_margin >= 20:
        category = "Stronghold"
        code_suffix = "STRONGHOLD"
        r_color = "#cb181d"
        d_color = "#3182bd"
    elif abs_margin >= 10:
        category = "Safe"
        code_suffix = "SAFE"
        r_color = "#ef3b2c"
        d_color = "#6baed6"
    elif abs_margin >= 5.5:
        category = "Likely"
        code_suffix = "LIKELY"
        r_color = "#fb6a4a"
        d_color = "#9ecae1"
    elif abs_margin >= 1.0:
        category = "Lean"
        code_suffix = "LEAN"
        r_color = "#fcae91"
        d_color = "#c6dbef"
    elif abs_margin >= 0.5:
        category = "Tilt"
        code_suffix = "TILT"
        r_color = "#fee8c8"
        d_color = "#e1f5fe"
    else:
        category = "Tossup"
        code_suffix = "TOSSUP"
        r_color = "#f7f7f7"
        d_color = "#f7f7f7"
    
    if margin_pct > 0:
        party = "Republican"
        code = f"R_{code_suffix}"
        color = r_color
    elif margin_pct < 0:
        party = "Democratic"
        code = f"D_{code_suffix}"
        color = d_color
    else:
        party = "Even"
        code = "TOSSUP"
        color = "#f7f7f7"
    
    return {
        "category": f"{category} {party}" if party != "Even" else "Tossup",
        "party": party,
        "code": code,
        "color": color
    }


def process_openelections_csv(file_path, year):
    """
    Process OpenElections format CSV
    Columns: county, office, district, party, candidate, votes
    Filter to keep only every other statewide office (except US House/Senate which are always kept)
    """
    
    print(f"Processing: {file_path.name}")
    
    df = pd.read_csv(file_path)
    
    # Standardize party codes
    party_mapping = {
        'R': 'REP',
        'D': 'DEM',
        'Republican': 'REP',
        'Democratic': 'DEM',
        'Democrat': 'DEM',
        'DEM': 'DEM',
        'REP': 'REP'
    }
    df['party'] = df['party'].map(party_mapping).fillna(df['party'])
    
    # Filter out only district-based races (State House, State Senate, US House)
    # Keep all statewide offices: Governor, Attorney General, Secretary of State, Treasurer, Auditor, U.S. Senate, President, Supreme Court
    district_races = [
        'State House', 'State Senate', 'State Senator',
        'State Representative', 
        'US Representative', 'U.S. House', 'U.S. Representative', 
        'Representative to Congress',
        'US House of Representatives'
    ]
    df = df[~df['office'].isin(district_races)]
    
    # Group by office and county to get contest results
    contests = {}
    
    for office in df['office'].unique():
        if office == 'Unknown' or str(office).isdigit():
            continue
            
        office_df = df[df['office'] == office]
        
        # For each unique contest (office + district combination)
        for district in office_df['district'].unique():
            if pd.isna(district):
                district = ''
            
            district_df = office_df[office_df['district'] == district] if district else office_df[office_df['district'].isna() | (office_df['district'] == '')]
            
            # Create contest key
            if district and str(district).strip():
                contest_key = f"{office} - District {district}"
            else:
                contest_key = office
            
            # Get results by county
            county_results = {}
            
            for county in district_df['county'].unique():
                county_df = district_df[district_df['county'] == county]
                
                # Group by candidate and party to handle precinct-level data
                # This aggregates all precincts for each candidate in the county
                candidate_totals = county_df.groupby(['candidate', 'party'], as_index=False)['votes'].sum()
                
                # Get candidate names
                dem_candidates = candidate_totals[candidate_totals['party'] == 'DEM']['candidate'].tolist()
                rep_candidates = candidate_totals[candidate_totals['party'] == 'REP']['candidate'].tolist()
                
                # Clean candidate names (convert "Last, First" to "First Last")
                def clean_name(name):
                    if ',' in name:
                        parts = name.split(',')
                        return f"{parts[1].strip()} {parts[0].strip()}"
                    return name
                
                dem_candidate = clean_name(dem_candidates[0]) if dem_candidates else "Unknown"
                rep_candidate = clean_name(rep_candidates[0]) if rep_candidates else "Unknown"
                
                # Get top 2 candidates by votes
                top_candidates = candidate_totals.nlargest(2, 'votes')
                
                if len(top_candidates) >= 2:
                    # Sum by party (handles multiple candidates per party or standardized codes)
                    dem_votes = candidate_totals[candidate_totals['party'] == 'DEM']['votes'].sum()
                    rep_votes = candidate_totals[candidate_totals['party'] == 'REP']['votes'].sum()
                    other_votes = candidate_totals[~candidate_totals['party'].isin(['DEM', 'REP'])]['votes'].sum()
                    
                    total_votes = candidate_totals['votes'].sum()
                    two_party_total = dem_votes + rep_votes
                    
                    if total_votes > 0:
                        # Calculate percentages based on total votes (including third parties) to match official results
                        dem_pct = (dem_votes / total_votes) * 100
                        rep_pct = (rep_votes / total_votes) * 100
                        margin_pct = rep_pct - dem_pct
                        margin = rep_votes - dem_votes
                        
                        competitiveness = get_competitiveness(margin_pct)
                        
                        county_results[county] = {
                            'county': county,
                            'contest': contest_key,
                            'year': year,
                            'dem_candidate': dem_candidate,
                            'rep_candidate': rep_candidate,
                            'dem_votes': int(dem_votes),
                            'rep_votes': int(rep_votes),
                            'other_votes': int(other_votes),
                            'total_votes': int(total_votes),
                            'two_party_total': int(two_party_total),
                            'margin': int(margin),
                            'margin_pct': round(margin_pct, 2),
                            'winner': 'REP' if rep_votes > dem_votes else 'DEM',
                            'competitiveness': {
                                'category': competitiveness['category'],
                                'party': competitiveness['party'],
                                'code': competitiveness['code'],
                                'color': competitiveness['color']
                            }
                        }
            
            if county_results:
                contests[contest_key] = {
                    'contest_name': contest_key,
                    'office': office,
                    'district': str(district) if district else '',
                    'results': county_results
                }
    
    print(f"  ✓ Processed {len(contests)} contest(s)")
    return contests


def transform_all_data():
    """Transform all Ohio election data into nested JSON format"""
    
    base_dir = Path(__file__).parent.parent / "data"
    output_file = base_dir / "ohio_election_results.json"
    
    # Look for consolidated OpenElections format files
    consolidated_files = list(base_dir.glob("*__oh__general__consolidated.csv"))
    
    if not consolidated_files:
        print("No consolidated files found. Please run convert_to_openelections.py first.")
        return
    
    # Extract years from filenames
    years = []
    year_file_map = {}
    for csv_file in consolidated_files:
        year_match = re.search(r'(\d{4})__oh__general__consolidated', csv_file.name)
        if year_match:
            year = year_match.group(1)
            years.append(int(year))
            year_file_map[year] = csv_file
    
    years = sorted(years)
    
    print(f"\nFound {len(years)} years of data: {years}")
    
    # Create metadata
    metadata = {
        "state": "Ohio",
        "state_code": "OH",
        "total_counties": 88,
        "years_covered": [int(y) for y in years],
        "data_source": "Ohio Secretary of State / OpenElections",
        "generated_date": datetime.now().strftime("%Y-%m-%d")
    }
    
    # Initialize results structure
    results_by_year = {}
    
    # Process each year's data
    for year in years:
        year_str = str(year)
        file_path = year_file_map[year_str]
        
        # Process the OpenElections format file
        contests = process_openelections_csv(file_path, year_str)
        
        # Organize by office type
        office_groups = {}
        for contest_key, contest_data in contests.items():
            office = contest_data['office']
            
            if office not in office_groups:
                office_groups[office] = {}
            
            office_groups[office][contest_key] = contest_data
        
        results_by_year[year_str] = office_groups
    
    # Combine into final structure
    final_output = {
        "metadata": metadata,
        "results_by_year": results_by_year
    }
    
    # Write to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)
    
    print(f"\nTransformation complete!")
    print(f"Output saved to: {output_file}")
    print(f"Years processed: {years}")


if __name__ == "__main__":
    transform_all_data()
