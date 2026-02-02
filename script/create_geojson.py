"""
Convert Ohio county shapefile to GeoJSON format
"""
import geopandas as gpd
import json
from pathlib import Path

def create_geojson():
    """Convert the Ohio county shapefile to GeoJSON"""
    
    # Define paths
    base_dir = Path(__file__).parent.parent
    shapefile_path = base_dir / "data" / "tl_2020_39_county20" / "tl_2020_39_county20.shp"
    output_path = base_dir / "data" / "ohio_counties.geojson"
    
    print(f"Reading shapefile from: {shapefile_path}")
    
    # Read the shapefile
    gdf = gpd.read_file(shapefile_path)
    
    # Convert to GeoJSON (WGS84 - EPSG:4326)
    gdf = gdf.to_crs(epsg=4326)
    
    # Save as GeoJSON
    gdf.to_file(output_path, driver='GeoJSON')
    
    print(f"GeoJSON created successfully at: {output_path}")
    print(f"Total counties: {len(gdf)}")
    print(f"\nAvailable columns: {gdf.columns.tolist()}")
    
    # Find the county name column
    name_col = None
    for col in ['NAME', 'NAMELSAD', 'NAME20', 'NAMELSAD20']:
        if col in gdf.columns:
            name_col = col
            break
    
    if name_col:
        print(f"\nCounty names:")
        for idx, row in gdf.iterrows():
            print(f"  - {row[name_col]}")

if __name__ == "__main__":
    create_geojson()
