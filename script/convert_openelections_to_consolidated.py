"""
Convert existing OpenElections format CSV files to consolidated format
"""
import pandas as pd
import re
from pathlib import Path


def process_openelections_file(file_path):
    """
    Process OpenElections format files (already in standard format)
    These files typically have columns like: county, office, district, party, candidate, votes
    """
    
    print(f"\n  Processing: {file_path.name}")
    
    try:
        # Read the CSV
        df = pd.read_csv(file_path)
        
        # Check columns
        print(f"    Columns ({len(df.columns)} total): {df.columns.tolist()}")
        
        # Standardize column names if needed
        column_mapping = {}
        for col in df.columns:
            col_lower = col.lower()
            # Use elif to prevent matching multiple conditions
            if 'county' in col_lower and col not in column_mapping.values():
                column_mapping[col] = 'county'
            elif 'office' in col_lower and col not in column_mapping.values():
                column_mapping[col] = 'office'
            elif col_lower == 'district' and col not in column_mapping.values():
                column_mapping[col] = 'district'
            elif 'party' in col_lower and col not in column_mapping.values():
                column_mapping[col] = 'party'
            elif 'candidate' in col_lower and col not in column_mapping.values():
                column_mapping[col] = 'candidate'
            elif 'vote' in col_lower and 'registered' not in col_lower and col not in column_mapping.values():
                column_mapping[col] = 'votes'
        
        if column_mapping:
            df = df.rename(columns=column_mapping)
        
        # Ensure required columns exist (party is optional, will be inferred if missing)
        required_cols = ['county', 'office', 'candidate', 'votes']
        missing = [col for col in required_cols if col not in df.columns]
        
        if missing:
            print(f"    ⚠ Missing columns: {missing}")
            return None
        
        # Add district column if missing
        if 'district' not in df.columns:
            df['district'] = ''
        
        # Add party column if missing - we'll infer from known candidates
        if 'party' not in df.columns:
            print(f"    INFO: Party column missing - will infer from candidate names")
            df['party'] = ''
            
            # Known 2010 Ohio candidates
            party_lookup = {
                # Governor
                'Kasich, John': 'REP',
                'Strickland, Ted': 'DEM',
                # U.S. Senate
                'Portman, Rob': 'REP',
                'Fisher, Lee': 'DEM',
                # Attorney General
                'DeWine, Mike': 'REP',
                'Cordray, Richard': 'DEM',
                # Auditor
                'Yost, Dave': 'REP',
                'Pepper, David': 'DEM',
                # Secretary of State
                'Husted, Jon': 'REP',
                "O'Shaughnessy, Maryellen": 'DEM',
                # Treasurer
                'Mandel, Josh': 'REP',
                'Boyce, Kevin': 'DEM',
            }
            
            for candidate, party in party_lookup.items():
                df.loc[df['candidate'] == candidate, 'party'] = party
        
        # Clean up data
        df['county'] = df['county'].astype(str).str.strip()
        df['office'] = df['office'].astype(str).str.strip()
        
        # Handle votes column more carefully - might be object type in some files
        if 'votes' in df.columns:
            votes_col = df['votes']
            # First try to convert, coercing errors to NaN
            df['votes'] = pd.to_numeric(votes_col, errors='coerce')
            # Fill NaN with 0 and convert to int
            df['votes'] = df['votes'].fillna(0).astype(int)
        else:
            print(f"    ERROR: votes column not found. Available: {df.columns.tolist()}")
            return None
        
        # Ensure party is string type
        if 'party' in df.columns:
            df['party'] = df['party'].fillna('').astype(str).str.strip()
        
        # Ensure candidate is string type
        if 'candidate' in df.columns:
            df['candidate'] = df['candidate'].fillna('Unknown').astype(str).str.strip()
        
        # Remove any rows with missing essential data
        df = df[df['county'].notna() & (df['county'] != '') & (df['county'] != 'nan')]
        
        print(f"    OK: Loaded {len(df)} rows")
        return df
        
    except Exception as e:
        print(f"    ERROR: {str(e)[:100]}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Convert all existing OpenElections files to consolidated format"""
    
    base_dir = Path(__file__).parent.parent / "data"
    
    # Find all OpenElections format files (YYYYMMDD__oh__general*.csv)
    openelections_files = list(base_dir.glob("20*__oh__general*.csv"))
    
    print(f"Found {len(openelections_files)} OpenElections files")
    
    # Group by year
    years_data = {}
    
    for file in openelections_files:
        # Extract year from filename (YYYYMMDD format) - case insensitive for state code
        year_match = re.search(r'^(\d{4})\d{4}__[oO][hH]__general', file.name)
        if not year_match:
            print(f"Skipping {file.name} - couldn't extract year")
            continue
        
        year = year_match.group(1)
        
        # Process the file
        df = process_openelections_file(file)
        
        if df is not None:
            if year not in years_data:
                years_data[year] = []
            years_data[year].append(df)
    
    # Combine and save by year
    for year, dfs in years_data.items():
        # Combine all files for this year
        try:
            combined_df = pd.concat(dfs, ignore_index=True)
        except Exception as e:
            print(f"\nERROR combining {year} data: {e}")
            import traceback
            traceback.print_exc()
            continue
        
        # Sort by office, county, votes
        combined_df = combined_df.sort_values(['office', 'county', 'votes'], ascending=[True, True, False])
        
        # Save consolidated file
        output_file = base_dir / f"{year}__oh__general__consolidated.csv"
        combined_df.to_csv(output_file, index=False)
        
        print(f"\nOK: Saved {year} data to: {output_file.name}")
        print(f"  Total rows: {len(combined_df):,}")
        print(f"  Counties: {combined_df['county'].nunique()}")
        print(f"  Offices: {sorted(combined_df['office'].unique())}")
    
    print("\nConversion complete!")


if __name__ == "__main__":
    main()
