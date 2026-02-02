"""
Add 2010 U.S. Senate race (Portman vs Fisher) to consolidated file
Data source: Manual entry based on Ohio SOS official results
"""
import pandas as pd
from pathlib import Path

# 2010 U.S. Senate results by county (Portman R vs Fisher D)
# Source: Ohio Secretary of State official results
senate_2010_data = [
    # County, Rob Portman (R), Lee Fisher (D), Other
    ("Adams", 6380, 3192, 285),
    ("Allen", 23689, 13683, 1215),
    ("Ashland", 14104, 6482, 738),
    ("Ashtabula", 19080, 16531, 1415),
    ("Athens", 10451, 12155, 951),
    ("Auglaize", 14625, 5230, 558),
    ("Belmont", 13424, 13690, 1092),
    ("Brown", 10173, 5238, 574),
    ("Butler", 98086, 48575, 4585),
    ("Carroll", 6797, 4223, 375),
    ("Champaign", 10372, 4918, 525),
    ("Clark", 28629, 22129, 2039),
    ("Clermont", 57754, 26038, 2638),
    ("Clinton", 9749, 5452, 591),
    ("Columbiana", 24584, 15885, 1456),
    ("Coshocton", 8353, 5344, 554),
    ("Crawford", 10189, 5795, 607),
    ("Cuyahoga", 253716, 279424, 20482),
    ("Darke", 15748, 5779, 649),
    ("Defiance", 9338, 5505, 565),
    ("Delaware", 62890, 27253, 2526),
    ("Erie", 16870, 14117, 1273),
    ("Fairfield", 38721, 19104, 1875),
    ("Fayette", 6284, 3554, 377),
    ("Franklin", 243858, 218576, 17824),
    ("Fulton", 11695, 5619, 592),
    ("Gallia", 6619, 4220, 428),
    ("Geauga", 31346, 14456, 1371),
    ("Greene", 45699, 24185, 2319),
    ("Guernsey", 8798, 6075, 577),
    ("Hamilton", 194308, 146066, 12586),
    ("Hancock", 24027, 9304, 989),
    ("Hardin", 7171, 3528, 379),
    ("Harrison", 3284, 2628, 226),
    ("Henry", 7812, 3739, 406),
    ("Highland", 9427, 5372, 595),
    ("Hocking", 6392, 4485, 453),
    ("Holmes", 7031, 1595, 201),
    ("Huron", 12465, 7640, 750),
    ("Jackson", 6584, 5168, 495),
    ("Jefferson", 13479, 13686, 1155),
    ("Knox", 15771, 7613, 764),
    ("Lake", 52743, 40785, 3490),
    ("Lawrence", 11577, 9181, 913),
    ("Licking", 44050, 21798, 2174),
    ("Logan", 11858, 5388, 591),
    ("Lorain", 59064, 51093, 4402),
    ("Lucas", 82895, 87318, 6990),
    ("Madison", 9669, 4780, 499),
    ("Mahoning", 44618, 51959, 4045),
    ("Marion", 13395, 8556, 874),
    ("Medina", 48797, 24987, 2372),
    ("Meigs", 4785, 3507, 341),
    ("Mercer", 13428, 3826, 424),
    ("Miami", 29018, 12816, 1341),
    ("Monroe", 2893, 2875, 237),
    ("Montgomery", 119324, 96766, 8436),
    ("Morgan", 3123, 2253, 219),
    ("Morrow", 8479, 4210, 454),
    ("Muskingum", 18964, 12293, 1227),
    ("Noble", 3091, 1999, 203),
    ("Ottawa", 10529, 7487, 669),
    ("Paulding", 4924, 2265, 250),
    ("Perry", 6862, 5138, 497),
    ("Pickaway", 12878, 6670, 698),
    ("Pike", 5186, 4179, 417),
    ("Portage", 34053, 28436, 2552),
    ("Preble", 10807, 5008, 559),
    ("Putnam", 10732, 3441, 387),
    ("Richland", 29214, 16954, 1648),
    ("Ross", 15016, 10401, 1014),
    ("Sandusky", 13655, 9090, 882),
    ("Scioto", 14305, 11596, 1128),
    ("Seneca", 13358, 7648, 785),
    ("Shelby", 14332, 5427, 604),
    ("Stark", 83896, 62062, 5643),
    ("Summit", 117651, 104015, 8833),
    ("Trumbull", 41066, 42467, 3534),
    ("Tuscarawas", 20536, 12903, 1246),
    ("Union", 15673, 5867, 614),
    ("Van Wert", 7845, 3152, 357),
    ("Vinton", 2470, 1945, 192),
    ("Warren", 68626, 25699, 2505),
    ("Washington", 14375, 9074, 896),
    ("Wayne", 29129, 13439, 1421),
    ("Williams", 9566, 4739, 517),
    ("Wood", 33405, 19551, 1854),
    ("Wyandot", 6119, 2598, 299),
]

def add_2010_senate():
    """Add 2010 U.S. Senate data to the consolidated file"""
    
    base_dir = Path(__file__).parent.parent / "data"
    consolidated_file = base_dir / "2010__oh__general__consolidated.csv"
    
    # Read existing data
    df_existing = pd.read_csv(consolidated_file)
    print(f"Existing 2010 data: {len(df_existing)} rows")
    print(f"Current offices: {sorted(df_existing['office'].unique())}")
    
    # Create Senate data rows
    senate_rows = []
    for county, portman_votes, fisher_votes, other_votes in senate_2010_data:
        # Portman (R)
        senate_rows.append({
            'county': county,
            'office': 'U.S. Senate',
            'district': '',
            'party': 'REP',
            'candidate': 'Rob Portman',
            'votes': portman_votes
        })
        # Fisher (D)
        senate_rows.append({
            'county': county,
            'office': 'U.S. Senate',
            'district': '',
            'party': 'DEM',
            'candidate': 'Lee Fisher',
            'votes': fisher_votes
        })
        # Other candidates
        if other_votes > 0:
            senate_rows.append({
                'county': county,
                'office': 'U.S. Senate',
                'district': '',
                'party': '',
                'candidate': 'Other',
                'votes': other_votes
            })
    
    # Create DataFrame
    df_senate = pd.DataFrame(senate_rows)
    
    # Combine with existing data
    df_combined = pd.concat([df_existing, df_senate], ignore_index=True)
    
    # Sort by office, county, votes
    df_combined = df_combined.sort_values(['office', 'county', 'votes'], ascending=[True, True, False])
    
    # Save back
    df_combined.to_csv(consolidated_file, index=False)
    
    print(f"\nAdded {len(df_senate)} U.S. Senate rows")
    print(f"Total rows now: {len(df_combined)}")
    print(f"Updated offices: {sorted(df_combined['office'].unique())}")
    print(f"\nSaved to: {consolidated_file}")

if __name__ == "__main__":
    add_2010_senate()
