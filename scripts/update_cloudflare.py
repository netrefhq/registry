#!/usr/bin/env python3
"""
Update Cloudflare DNS records from YAML files
This script processes subdomain requests and creates DNS records in Cloudflare
"""

import os
import sys
import yaml
import requests
from pathlib import Path

def get_cloudflare_credentials():
    """Get Cloudflare API credentials from environment variables"""
    api_token = os.environ.get('CLOUDFLARE_API_TOKEN')
    zone_id = os.environ.get('CLOUDFLARE_ZONE_ID')
    
    if not api_token:
        raise ValueError("CLOUDFLARE_API_TOKEN environment variable is required")
    if not zone_id:
        raise ValueError("CLOUDFLARE_ZONE_ID environment variable is required")
    
    return api_token, zone_id

def get_existing_dns_records(api_token, zone_id):
    """Fetch existing DNS records from Cloudflare"""
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }
    
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch DNS records: {response.text}")
    
    records = response.json().get('result', [])
    return {record['name']: record for record in records}

def create_dns_record(api_token, zone_id, subdomain, record_type, record_value, ttl=3600, proxied=False):
    """Create a new DNS record in Cloudflare"""
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }
    
    # Full domain name
    full_domain = f"{subdomain}.netref.link"
    
    data = {
        'type': record_type,
        'name': full_domain,
        'content': record_value,
        'ttl': ttl,
        'proxied': proxied,
    }
    
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code not in (200, 201):
        raise Exception(f"Failed to create DNS record for {full_domain}: {response.text}")
    
    return response.json().get('result')

def update_dns_record(api_token, zone_id, record_id, subdomain, record_type, record_value, ttl=3600, proxied=False):
    """Update an existing DNS record in Cloudflare"""
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }
    
    # Full domain name
    full_domain = f"{subdomain}.netref.link"
    
    data = {
        'type': record_type,
        'name': full_domain,
        'content': record_value,
        'ttl': ttl,
        'proxied': proxied,
    }
    
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}'
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update DNS record for {full_domain}: {response.text}")
    
    return response.json().get('result')

def get_changed_yaml_files():
    """Get list of YAML files that were added or modified in the latest commit"""
    # For GitHub Actions, we can get the list of changed files
    # This is a simplified version - in production, you'd parse git diff
    domains_dir = Path(__file__).parent.parent / 'domains'
    
    # If GITHUB_EVENT_PATH is set, we're in GitHub Actions
    event_path = os.environ.get('GITHUB_EVENT_PATH')
    if event_path and os.path.exists(event_path):
        import json
        with open(event_path, 'r') as f:
            event_data = json.load(f)
        
        # For pull_request events, we'd need to fetch the changed files
        # For now, process all non-example YAML files
        return [f for f in domains_dir.glob('*.yaml') if f.stem != 'example']
    
    # Default: process all YAML files
    return [f for f in domains_dir.glob('*.yaml') if f.stem != 'example']

def process_subdomain_requests(dry_run=False):
    """Process all subdomain requests and update Cloudflare"""
    try:
        api_token, zone_id = get_cloudflare_credentials()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    yaml_files = get_changed_yaml_files()
    
    if not yaml_files:
        print("No subdomain requests to process")
        return
    
    print(f"Processing {len(yaml_files)} subdomain request(s)...")
    
    # Get existing DNS records (skip in dry-run mode)
    if dry_run:
        existing_records = {}
    else:
        try:
            existing_records = get_existing_dns_records(api_token, zone_id)
        except Exception as e:
            print(f"Error fetching existing DNS records: {e}")
            sys.exit(1)
    
    success_count = 0
    error_count = 0
    
    for filepath in yaml_files:
        try:
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)
            
            subdomain = data['subdomain']
            record_type = data['record_type']
            record_value = data['record_value']
            ttl = data.get('ttl', 3600)
            proxied = data.get('proxied', False)
            
            full_domain = f"{subdomain}.netref.link"
            
            if dry_run:
                print(f"[DRY RUN] Would create/update {full_domain} -> {record_type} {record_value}")
                success_count += 1
                continue
            
            # Check if record already exists
            if full_domain in existing_records:
                existing = existing_records[full_domain]
                print(f"Updating existing DNS record for {full_domain}...")
                update_dns_record(api_token, zone_id, existing['id'], subdomain, record_type, record_value, ttl, proxied)
                print(f"✅ Updated {full_domain}")
            else:
                print(f"Creating new DNS record for {full_domain}...")
                create_dns_record(api_token, zone_id, subdomain, record_type, record_value, ttl, proxied)
                print(f"✅ Created {full_domain}")
            
            success_count += 1
            
        except Exception as e:
            print(f"❌ Error processing {filepath.name}: {e}")
            error_count += 1
    
    print(f"\nProcessing complete: {success_count} successful, {error_count} errors")
    
    if error_count > 0:
        sys.exit(1)

def main():
    dry_run = '--dry-run' in sys.argv
    
    if dry_run:
        print("Running in DRY RUN mode - no changes will be made to Cloudflare")
    
    process_subdomain_requests(dry_run=dry_run)

if __name__ == '__main__':
    main()
