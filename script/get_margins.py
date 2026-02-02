import json

data = json.load(open('data/ohio_election_results.json'))

# Get presidential margins for key counties across years
counties = ['Mahoning', 'Trumbull', 'Franklin', 'Cuyahoga', 'Hamilton', 'Butler']
years = ['2008', '2012', '2016', '2020', '2024']

print("\nChecking for 2020 data specifically:")
if '2020' in data['results_by_year']:
    print(f"2020 offices: {list(data['results_by_year']['2020'].keys())}")

for county in counties:
    print(f"\n{county} County Presidential Margins:")
    for year in years:
        try:
            if year in data['results_by_year'] and 'President' in data['results_by_year'][year]:
                president_data = data['results_by_year'][year]['President']
                
                # Find the presidential contest key
                contest_key = None
                if 'President' in president_data:
                    contest_key = 'President'
                elif 'President and Vice President' in president_data:
                    contest_key = 'President and Vice President'
                else:
                    # For 2020, it might be "President - District X" - just grab any President key
                    president_keys = [k for k in president_data.keys() if 'President' in k]
                    if president_keys:
                        contest_key = president_keys[0]
                
                if contest_key and 'results' in president_data[contest_key]:
                    pres = president_data[contest_key]['results']
                    if county in pres:
                        margin = pres[county]['margin_pct']
                        winner = pres[county]['winner']
                        dem_pct = (pres[county]['dem_votes'] / pres[county]['total_votes']) * 100
                        rep_pct = (pres[county]['rep_votes'] / pres[county]['total_votes']) * 100
                        
                        if winner == 'DEM':
                            print(f"  {year}: D+{margin:.2f}% ({dem_pct:.2f}% D, {rep_pct:.2f}% R)")
                        else:
                            print(f"  {year}: R+{margin:.2f}% ({rep_pct:.2f}% R, {dem_pct:.2f}% D)")
        except Exception as e:
            print(f"  {year}: Error - {e}")
