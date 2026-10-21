#!/usr/bin/env python3
"""
OSDR Data Fetcher CLI Tool for Spaceflight Plant Microbiome Analysis.

Queries the NASA Open Science Data Repository (OSDR) REST API for plant spaceflight
dataset metadata and associated data files (meta-transcriptomics, RNA-seq, microarrays).

Supported Datasets:
  - OSD-37:  Spaceflight effects on seedling microbiome (BRIC-19)
  - OSD-38:  Spaceflight seedling root & shoot microbiome (BRIC-20)
  - OSD-120: Arabidopsis seedlings spaceflight vs ground control
  - OSD-217: Spaceflight transcriptome & microbiome (APEX-03-2 / BRIC-16)
  - OSD-321: Meta-transcriptomic spaceflight profile
  - OSD-522: Arabidopsis spaceflight microbiome profile

Usage:
  python3 fetch_osdr_data.py --studies 37,38,120,217,321,522 --list-files
  python3 fetch_osdr_data.py --study 37 --filter "MetaPhlAn"
"""

import sys
import os
import argparse
import json
import urllib.request

import ssl

OSDR_API_BASE = "https://osdr.nasa.gov/genelab/data/glds/files"

DEFAULT_STUDIES = [37, 38, 69, 120, 193, 217, 218, 223, 281, 321, 417, 522]


def fetch_study_metadata(study_ids):
    """Query OSDR REST API for specific study IDs."""
    ids_str = ",".join(str(s) for s in study_ids)
    url = f"{OSDR_API_BASE}/{ids_str}"
    print(f"[*] Querying OSDR API: {url}")
    
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "MicrobiomeSpaceflightAnalyzer/1.0"}
    )
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                return data
            else:
                print(f"[!] HTTP Error {response.status}")
                return None
    except Exception as e:
        print(f"[!] Error fetching OSDR data: {e}")
        return None


def print_study_summary(api_response, filter_keyword=None):
    """Print file details for queried studies."""
    if not api_response or 'studies' not in api_response:
        print("[!] No valid studies returned from API.")
        return

    studies_dict = api_response['studies']
    sep = "=" * 70
    print(f"\n{sep}")
    print(f"  NASA OSDR STUDY FILE METADATA SUMMARY ({len(studies_dict)} Studies Found)")
    print(f"{sep}")

    total_files = 0
    for study_id, study_data in studies_dict.items():
        title = study_data.get('title', 'N/A')
        files = study_data.get('study_files', [])
        
        if filter_keyword:
            filtered_files = [
                f for f in files if filter_keyword.lower() in f.get('file_name', '').lower()
            ]
        else:
            filtered_files = files

        total_files += len(filtered_files)
        print(f"\n📌 {study_id}: Total Files Available = {len(files)} (Showing {len(filtered_files)})")
        
        for f in filtered_files[:15]:
            fname = f.get('file_name', 'N/A')
            try:
                fsize = int(f.get('file_size', 0) or 0)
            except (ValueError, TypeError):
                fsize = 0
            furl = f.get('remote_url', '')
            if furl and not furl.startswith('http'):
                furl = f"https://osdr.nasa.gov{furl}"
            print(f"   • {fname[:50]:<50} | {fsize} bytes | {furl}")
        
        if len(filtered_files) > 15:
            print(f"   ... and {len(filtered_files) - 15} more files.")

    print(f"\n{sep}")
    print(f" Total files listed across all requested studies: {total_files:,}")
    print(f"{sep}\n")


def main():
    parser = argparse.ArgumentParser(
        description="NASA OSDR REST API Client for Plant Microbiome Data."
    )
    parser.add_argument(
        "--studies", "-s",
        type=str,
        default="37,38,120,217,321,522",
        help="Comma-separated OSD study IDs (default: 37,38,120,217,321,522)"
    )
    parser.add_argument(
        "--filter", "-f",
        type=str,
        default=None,
        help="Filter file names by keyword (e.g., 'fastq', 'MetaPhlAn', 'counts')"
    )
    parser.add_argument(
        "--output-json", "-o",
        type=str,
        default=None,
        help="Save raw API JSON response to specified output file path"
    )

    args = parser.parse_args()

    try:
        study_ids = [int(x.strip()) for x in args.studies.split(",") if x.strip()]
    except ValueError:
        print("[!] Invalid study ID format. Provide integers separated by commas.")
        sys.exit(1)

    data = fetch_study_metadata(study_ids)

    if data:
        print_study_summary(data, filter_keyword=args.filter)
        if args.output_json:
            with open(args.output_json, 'w', encoding='utf-8') as fp:
                json.dump(data, fp, indent=2)
            print(f"[+] Saved API metadata to {args.output_json}")


if __name__ == "__main__":
    main()
