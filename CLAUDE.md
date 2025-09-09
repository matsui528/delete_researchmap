# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python tool for retrieving ResearchMap data and generating CSV files for bulk deletion. The main script `delete_researchmap.py` fetches academic publication and profile data from the ResearchMap API and creates CSV files formatted for ResearchMap's bulk deletion feature.

## Architecture

The codebase consists of a single Python script with the following key functions:

- `fetch_researchmap_data()`: Handles API requests with multiple retry strategies for different pagination parameters
- `extract_all_types_data()`: Parses the JSON-LD `@graph` structure and organizes data by `@type`  
- `create_csv_files()`: Generates deletion CSV files in ResearchMap format (type header, action column, ID column)
- `display_publications()`: Debug utility for examining retrieved data structure

## Usage

Run the tool with a ResearchMap permalink:
```bash
python delete_researchmap.py --permalink <permalink>
```

The script generates:
- `delete_{type}.csv` files for each data type found
- `researchmap_{permalink}_debug.json` for debugging raw API responses

## Data Flow

1. API calls to `https://api.researchmap.jp/{permalink}` with fallback pagination parameters
2. JSON-LD parsing to extract items from `@graph` sections
3. CSV generation with format: `@type` header, `アクション名,ID` columns, `delete,{rm:id}` rows

## Dependencies

- `requests`: HTTP client for API calls
- `json`, `csv`, `os`, `sys`: Standard library modules
- Type hints using `typing.Dict`, `typing.Any`, `typing.List`