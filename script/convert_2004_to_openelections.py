"""
Convert 2004 Ohio election data to OpenElections format
Merges the Candidate Name List with Election Results
"""
import pandas as pd
from pathlib import Path

def convert_2004_to_openelections():
    """
    Convert 2004 Ohio data to OpenElections format
    """
    
    base_dir = Path(__file__).parent.parent / "data"
    
    # Read candidate mapping
    candidates_file = base_dir / "2004 Candidate Name List.csv"
    results_file = base_dir / "2004 Election Results.csv"
    
    print(f"Reading {candidates_file.name}...")
    candidates_df = pd.read_csv(candidates_file)
    
    print(f"Reading {results_file.name}...")
    # Read with skiprows to skip the first header line
    results_df = pd.read_csv(results_file, skiprows=1)
    
    # Create mapping of column names to candidate info
    column_mapping = {}
    for _, row in candidates_df.iterrows():
        col_name = row['Data Column Name']
        
        # Skip if missing required fields
        if pd.isna(col_name) or pd.isna(row['Candidate Name']):
            continue
        
        office = row['Office '].strip()
        district = row['District'] if pd.notna(row['District']) else None
        party_code = row['Party']
        candidate = str(row['Candidate Name']).strip()
        
        # Map party codes
        party = 'DEM' if party_code == 'D' else 'REP' if party_code == 'R' else 'IND'
        
        # Standardize office names
        if office == 'President/Vice President':
            office_name = 'President'
        elif office == 'U.S. Senate':
            office_name = 'U.S. Senate'
        elif office == 'U.S. Representative':
            office_name = 'U.S. House'
        elif office == 'State Senator':
            office_name = 'State Senate'
        elif office == 'State Representative':
            office_name = 'State House'
        elif office == 'Board of Education':
            office_name = 'State Board of Education'
        elif 'Justice of the Supreme Court' in office or 'Chief Justice' in office:
            office_name = 'State Supreme Court'
        elif 'Court of Appeals' in office:
            office_name = 'Court of Appeals'
        else:
            office_name = office
        
        column_mapping[col_name] = {
            'office': office_name,
            'district': str(int(district)) if pd.notna(district) else '',
            'party': party,
            'candidate': candidate
        }
    
    # Process results
    openelections_rows = []
    
    print("\nProcessing results...")
    for _, row in results_df.iterrows():
        county_name = row['COUNTY NAME']
        
        # Skip total/summary rows
        if pd.isna(county_name) or not county_name.strip():
            continue
        
        county_name = county_name.strip().title()
        
        # Fix Van Wert county name (appears as VANWERT in source)
        if county_name == 'Vanwert':
            county_name = 'Van Wert'
        
        # Process each candidate column
        for col_name, candidate_info in column_mapping.items():
            if col_name not in results_df.columns:
                continue
            
            votes = row[col_name]
            
            # Skip if no votes or invalid value
            if pd.isna(votes) or votes == '':
                votes = 0
            else:
                try:
                    votes = int(str(votes).replace(',', '').strip())
                except:
                    votes = 0
            
            openelections_rows.append({
                'county': county_name,
                'office': candidate_info['office'],
                'district': candidate_info['district'],
                'party': candidate_info['party'],
                'candidate': candidate_info['candidate'],
                'votes': votes
            })
    
    # Aggregate by county (sum votes across precincts)
    print("\nAggregating by county...")
    df = pd.DataFrame(openelections_rows)
    
    grouped = df.groupby(['county', 'office', 'district', 'party', 'candidate'], as_index=False)['votes'].sum()
    
    # Sort by office, county, votes
    grouped = grouped.sort_values(['office', 'county', 'votes'], ascending=[True, True, False])
    
    # Save consolidated file
    output_file = base_dir / "2004__oh__general__consolidated.csv"
    grouped.to_csv(output_file, index=False)
    
    print(f"\n✓ Saved consolidated 2004 data to: {output_file.name}")
    print(f"  Total rows: {len(grouped):,}")
    print(f"  Counties: {grouped['county'].nunique()}")
    print(f"  Offices: {grouped['office'].nunique()}")
    print(f"\nOffices included:")
    for office in sorted(grouped['office'].unique()):
        count = grouped[grouped['office'] == office]['candidate'].nunique()
        print(f"  - {office}: {count} candidates")
    
    return grouped

if __name__ == "__main__":
    convert_2004_to_openelections()
