"""
ResearchMap API client for retrieving and managing publication data.
Usage: python researchmap_delete.py --permalink <permalink>
"""

import argparse
import requests
import json
import sys
import csv
from typing import Dict, Any, List


def fetch_researchmap_data(permalink: str, limit: int = 1000) -> Dict[str, Any]:
    """
    Fetch ResearchMap data for a given permalink.
    
    Args:
        permalink: ResearchMap permalink (e.g., 'matsui528')
        limit: Number of items to request per page
        
    Returns:
        JSON data from ResearchMap API
    """
    url = f"https://api.researchmap.jp/{permalink}"
    params = {"limit": limit}
    
    try:
        print(f"Fetching data from: {url} with limit: {limit}")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
        
    except requests.RequestException as e:
        print(f"Failed to fetch data: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        sys.exit(1)


def extract_all_types_data(data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Extract all data from the @graph attribute, organized by @type.
    
    Args:
        data: Full JSON data from ResearchMap API
        
    Returns:
        Dictionary with @type as keys and list of items as values
    """
    graph = data.get("@graph", [])
    types_data = {}
    
    for item in graph:
        item_type = item.get("@type", "unknown")
        
        # Initialize list if not exists
        if item_type not in types_data:
            types_data[item_type] = []
        
        # If item has 'items' array, extract those items
        if "items" in item and isinstance(item["items"], list):
            print(f"Found {item_type} section with {item.get('total_items', len(item['items']))} items")
            types_data[item_type].extend(item["items"])
        else:
            # Add the item itself
            types_data[item_type].append(item)
    
    return types_data


def save_debug_data(data: Dict[str, Any], permalink: str) -> None:
    """
    Save raw API response data for debugging purposes.
    
    Args:
        data: Raw JSON data from ResearchMap API
        permalink: ResearchMap permalink for filename
    """
    debug_file = f"researchmap_{permalink}_debug.json"
    with open(debug_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Raw data saved to: {debug_file}")


def create_csv_files(types_data: Dict[str, List[Dict[str, Any]]]) -> None:
    """
    Create CSV files for each @type found in the data in ResearchMap deletion format.
    
    Format:
    - Line 1: @type
    - Line 2: Header "アクション名,ID"
    - Line 3+: "delete,{ID}" for each item
    
    Args:
        types_data: Dictionary with @type as keys and list of items as values
    """
    for data_type, items in types_data.items():
        if not items:
            continue
            
        filename = f"delete_{data_type}.csv"
        print(f"Creating {filename} with {len(items)} records...")
        
        # Write CSV file in ResearchMap deletion format
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                
                # Line 1: @type
                writer.writerow([data_type])
                
                # Line 2: Header
                writer.writerow(["アクション名", "ID"])
                
                # Line 3+: delete entries for each item
                for item in items:
                    item_id = item.get("rm:id", "")
                    if item_id:
                        writer.writerow(["delete", item_id])
                    else:
                        print(f"Warning: No rm:id found for item in {data_type}")
                        # Try to find alternative ID fields
                        alt_id = item.get("@id", "").split("/")[-1] if item.get("@id") else ""
                        if alt_id:
                            writer.writerow(["delete", alt_id])
                        else:
                            print(f"Warning: No ID found for item in {data_type}")
                    
            print(f"Successfully created {filename}")
            
        except Exception as e:
            print(f"Error creating {filename}: {e}")




def main():
    parser = argparse.ArgumentParser(
        description="Retrieve and display ResearchMap publication data"
    )
    parser.add_argument(
        "--permalink",
        required=True,
        help="ResearchMap permalink (e.g., matsui528)"
    )
    
    args = parser.parse_args()
    
    # Fetch data from ResearchMap API
    data = fetch_researchmap_data(args.permalink)
    
    # Extract and process all types from @graph
    if "@graph" not in data:
        print("No @graph attribute found in response")
        save_debug_data(data, args.permalink)
        return
    
    print(f"@graph contains {len(data['@graph'])} items")
    
    # Extract all data organized by type
    types_data = extract_all_types_data(data)
    
    # Display summary of found types
    print(f"\nFound {len(types_data)} different types:")
    for data_type, items in types_data.items():
        print(f"  - {data_type}: {len(items)} items")
    
    # Create CSV files for each type
    print("\nCreating CSV files...")
    create_csv_files(types_data)
    
    # Save raw data for debugging
    save_debug_data(data, args.permalink)


if __name__ == "__main__":
    main()