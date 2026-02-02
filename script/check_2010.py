import pandas as pd

df = pd.read_csv('data/2010__oh__general__consolidated.csv')

statewide = ['Attorney General', 'Auditor of State', 'Governor/Lieutenant Governor', 
             'Secretary of State', 'Treasurer of State', 'U.S. Senate']

for office in statewide:
    office_df = df[df['office'] == office]
    print(f'{office}: {len(office_df)} rows, {office_df["county"].nunique()} counties')
    parties = office_df['party'].value_counts().to_dict()
    print(f'  Parties: {parties}')
    if len(office_df) > 0:
        print(f'  Sample candidates: {office_df["candidate"].unique()[:5].tolist()}')
    print()
