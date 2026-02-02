"""
Convert Ohio Secretary of State aligned CSV files to OpenElections format
"""
import pandas as pd
import csv
import re
from pathlib import Path
from io import StringIO


def parse_candidate_column(col_name):
    """Extract candidate name and party from column header"""
    candidate_name = col_name.strip()
    party = ''
    
    if ' (D)' in candidate_name:
        party = 'DEM'
        candidate_name = candidate_name.replace(' (D)', '')
    elif ' (R)' in candidate_name:
        party = 'REP'
        candidate_name = candidate_name.replace(' (R)', '')
    elif ' (L)' in candidate_name:
        party = 'LIB'
        candidate_name = candidate_name.replace(' (L)', '')
    elif ' (G)' in candidate_name or ' (GRP)' in candidate_name:
        party = 'GRN'
        candidate_name = candidate_name.replace(' (G)', '').replace(' (GRP)', '')
    elif '(WI)' in candidate_name:
        party = ''
        candidate_name = candidate_name.replace(' (WI)*', '').replace(' (WI)', '').replace('(WI)', '')
    
    # Clean up candidate name
    candidate_name = candidate_name.replace(' and ', ' / ').strip()
    
    return candidate_name, party


def infer_office_from_candidate(candidate_name, filename, year):
    """Infer office from candidate name and filename context"""
    
    # Known candidates for 2022-2024 (full names to avoid partial matches)
    governor_candidates_2022 = ['Mike DeWine and Jon Husted', 'Nan Whaley and Cheryl L. Stephens', 'Timothy Grady and Dayna Bickley', 
                                 'Craig Patton and Collin Cook', 'Renea Turner and Adina Pelletier', 'Marshall Usher and Shannon  Walker']
    ag_candidates_2022 = ['Jeffrey A. Crossman', 'Dave Yost']
    auditor_candidates_2022 = ['Keith Faber', 'Taylor Sappington']
    sos_candidates_2022 = ['Chelsea Clark', 'Frank LaRose', 'Terpsehore Tore Maras']
    treasurer_candidates_2022 = ['Scott Schertzer', 'Robert Sprague']
    
    senate_candidates = {
        '2022': ['JD Vance', 'Tim Ryan'],
        '2024': ['Sherrod Brown', 'Bernie Moreno']
    }
    
    president_candidates_2024 = ['Donald J. Trump and JD Vance', 'Kamala D. Harris and Tim Walz', 
                                  'Robert F. Kennedy Jr. and Nicole Shanahan', 'Jill Stein and Rudolph Ware',
                                  'Chase Oliver and Mike ter Maat', 'Cornel West and Melina Abdullah']
    
    supreme_court_candidates = {
        '2022': ['Pat Fischer', 'Sharon L. Kennedy', 'Terri Jamison', 'Jennifer Brunner'],
        '2024': ['Melody J. Stewart', 'Michael P. Donnelly', 'Megan E. Shanahan', 'Joseph T. Deters', 'Dan Hawkins']
    }
    
    # US House candidates - comprehensive list
    house_candidates = ['Brad Wenstrup', 'Steve Chabot', 'Jim Jordan', 'Bob Latta', 'David P. Joyce', 
                       'Mike Carey', 'Troy Balderson', 'Madison Gesiotto Gilbert', 'Bill Johnson', 'Emilia Sykes',
                       'Max Miller', 'Shontel Brown', 'Greg Landsman', 'Warren Davidson', 'Mike Turner',
                       'Joyce Beatty', 'Samantha Meadows', 'Matt Diemer', 'Derek Merrin', 'Marcy Kaptur']
    
    # Check filename hints first (most reliable)
    if 'Supreme' in filename or 'Justice' in filename:
        return 'State Supreme Court', ''
    if 'President' in filename:
        return 'President', ''
    
    # For Congress files, default to checking both Senate and House
    if 'Congress' in filename:
        # Check Senate first (exact match)
        year_senate = senate_candidates.get(year, [])
        for sen in year_senate:
            if sen in candidate_name:  # Exact match
                return 'U.S. Senate', ''
        
        # Then check House candidates
        for house in house_candidates:
            if house in candidate_name:  # Exact match
                return 'U.S. House', ''
        
        # Default to U.S. House for Congress files if no match
        return 'U.S. House', ''
    
    # Match state offices only for midterm years (2022, 2026, etc.)
    if year == '2022':
        # Full name matching for ticket races
        for gov in governor_candidates_2022:
            if 'DeWine' in candidate_name and 'Husted' in candidate_name:
                return 'Governor', ''
            elif 'Whaley' in candidate_name and 'Stephens' in candidate_name:
                return 'Governor', ''
            elif gov in candidate_name:
                return 'Governor', ''
        
        for ag in ag_candidates_2022:
            if ag in candidate_name:  # Exact match
                return 'Attorney General', ''
        
        for aud in auditor_candidates_2022:
            if aud in candidate_name:  # Exact match
                return 'State Auditor', ''
        
        for sec in sos_candidates_2022:
            if sec in candidate_name:  # Exact match
                return 'Secretary of State', ''
        
        for tres in treasurer_candidates_2022:
            if tres in candidate_name:  # Exact match
                return 'State Treasurer', ''
    
    # Check presidential race for 2024
    if year == '2024':
        for pres in president_candidates_2024:
            if 'Trump' in candidate_name or 'Harris' in candidate_name or 'Kennedy' in candidate_name or 'Stein' in candidate_name or 'Oliver' in candidate_name or 'West' in candidate_name:
                return 'President', ''
    
    # Check Supreme Court by year
    year_sc = supreme_court_candidates.get(year, [])
    for sc in year_sc:
        if sc in candidate_name:  # Exact match
            return 'State Supreme Court', ''
    
    return 'Unknown', ''


def convert_ohio_sos_to_openelections(input_file, year):
    """
    Convert Ohio SOS CSV format to OpenElections format
    
    Returns list of dicts with: county, office, district, party, candidate, votes
    """
    
    print(f"\n  Processing: {input_file.name}")
    
    try:
        # Read the file
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # Find header row
        header_row_idx = None
        for idx, line in enumerate(lines):
            if 'County Name' in line and 'Precinct Name' in line:
                header_row_idx = idx
                break
        
        if header_row_idx is None:
            print(f"    ⚠ Could not find header row")
            return []
        
        # Parse the office row (line before header) to get column-to-office mapping
        column_to_office = {}
        if header_row_idx > 0:
            office_line = lines[header_row_idx - 1]
            office_reader = csv.reader(StringIO(office_line))
            office_cells = next(office_reader)
            
            current_office = None
            for col_idx, cell in enumerate(office_cells):
                cell_text = cell.strip()
                
                # Check for office names
                if 'Governor and Lieutenant Governor' in cell_text:
                    current_office = 'Governor'
                elif 'Attorney General' in cell_text:
                    current_office = 'Attorney General'
                elif 'Auditor of State' in cell_text:
                    current_office = 'State Auditor'
                elif 'Secretary of State' in cell_text:
                    current_office = 'Secretary of State'
                elif 'Treasurer of State' in cell_text:
                    current_office = 'State Treasurer'
                elif 'Justice of the Supreme Court' in cell_text:
                    current_office = 'State Supreme Court'
                elif 'President and Vice President' in cell_text:
                    current_office = 'President'
                elif 'U.S. Senator' in cell_text or '"U.S. Senator' in cell_text:
                    current_office = 'U.S. Senate'
                elif 'Representative to Congress' in cell_text:
                    # Extract district number
                    match = re.search(r'District (\d+)', cell_text)
                    if match:
                        current_office = f'U.S. House|{match.group(1)}'
                
                # Map column to current office
                if current_office:
                    column_to_office[col_idx] = current_office
        
        # Parse header
        header_line = lines[header_row_idx]
        header_reader = csv.reader(StringIO(header_line))
        headers = next(header_reader)
        
        # Read data rows and aggregate by county
        data_lines = lines[header_row_idx + 1:]
        csv_reader = csv.reader(StringIO('\n'.join(data_lines)))
        
        county_data = {}
        for row in csv_reader:
            if len(row) < len(headers):
                continue
            
            county_name = row[0].strip() if len(row) > 0 else ''
            
            # Skip summary rows
            if not county_name or county_name in ['Total', 'Percentage']:
                continue
            
            if county_name not in county_data:
                county_data[county_name] = []
            
            county_data[county_name].append(row)
        
        # Convert to OpenElections format
        openelections_rows = []
        
        # Debug: Check Adams county
        if 'Adams' in county_data:
            print(f"    DEBUG: Adams county has {len(county_data['Adams'])} precinct rows")
        
        for county_name, rows in county_data.items():
            # Process each candidate column
            for col_idx, col_name in enumerate(headers):
                # Skip metadata columns
                if col_idx < 2 or not col_name or col_name.strip() in [
                    'Precinct Code', 'Region Name', 'Media Market',
                    'Registered Voters', 'Ballots Counted', 'Official Voter Turnout',
                    '']:
                    continue
                
                # Sum votes across precincts for this county
                total_votes = 0
                for row in rows:
                    if col_idx < len(row):
                        val = row[col_idx]
                        try:
                            num_val = int(str(val).replace(',', '').replace('"', '').strip())
                            total_votes += num_val
                        except:
                            pass
                
                if total_votes == 0:
                    continue
                
                # Parse candidate and party
                candidate_name, party = parse_candidate_column(col_name)
                
                # Infer office from candidate name and context
                office, district = infer_office_from_candidate(candidate_name, input_file.name, year)
                
                # Try column mapping first if available
                if col_idx in column_to_office:
                    office_info = column_to_office[col_idx]
                    if '|' in office_info:
                        # US House with district
                        office, district = office_info.split('|')
                    else:
                        office = office_info
                
                openelections_rows.append({
                    'county': county_name,
                    'office': office,
                    'district': district,
                    'party': party,
                    'candidate': candidate_name,
                    'votes': total_votes
                })
        
        print(f"    ✓ Extracted {len(openelections_rows)} rows ({len(county_data)} counties)")
        return openelections_rows
    
    except Exception as e:
        print(f"    ⚠ Error: {str(e)[:100]}")
        return []


def main():
    """Convert all Ohio SOS aligned files to OpenElections format"""
    
    base_dir = Path(__file__).parent.parent / "data"
    
    # Files to process - USE NON-ALIGNED VERSIONS for complete data
    files_to_process = [
        ('2022 Statewide Offices.csv', '2022'),
        ('2022 Supreme Court.csv', '2022'),
        ('2022 U.S. Congress.csv', '2022'),
        ('2024 President and Vice President.csv', '2024'),
        ('2024 Justice of the Supreme Court.csv', '2024'),
        ('2024 U.S. Congress.csv', '2024'),
    ]
    
    all_results = {}
    
    for filename, year in files_to_process:
        input_file = base_dir / filename
        if not input_file.exists():
            print(f"Skipping {filename} - file not found")
            continue
        
        rows = convert_ohio_sos_to_openelections(input_file, year)
        
        if year not in all_results:
            all_results[year] = []
        all_results[year].extend(rows)
    
    # Save consolidated files by year
    for year, rows in all_results.items():
        if not rows:
            continue
        
        df = pd.DataFrame(rows)
        df = df.sort_values(['office', 'county', 'votes'], ascending=[True, True, False])
        
        output_file = base_dir / f"{year}__oh__general__consolidated.csv"
        df.to_csv(output_file, index=False)
        
        print(f"\n✓ Saved {year} data to: {output_file.name}")
        print(f"  Total rows: {len(df):,}")
        print(f"  Counties: {df['county'].nunique()}")
        print(f"  Offices: {sorted(df['office'].unique())}")
    
    print("\nConversion complete!")


if __name__ == "__main__":
    main()
