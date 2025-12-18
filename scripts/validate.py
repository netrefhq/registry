#!/usr/bin/env python3
"""
Validate subdomain request YAML files
This script checks if YAML files in the domains/ directory are properly formatted
"""

import os
import sys
import yaml
import re
from pathlib import Path

def validate_email(email):
    """Basic email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_subdomain(subdomain):
    """Validate subdomain name"""
    # Must be alphanumeric with hyphens, no starting/ending hyphen
    pattern = r'^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$'
    return re.match(pattern, subdomain) is not None

def validate_record_type(record_type):
    """Validate DNS record type"""
    valid_types = ['A', 'AAAA', 'CNAME', 'TXT']
    return record_type in valid_types

def validate_yaml_file(filepath):
    """Validate a single YAML file"""
    errors = []
    
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"Invalid YAML format: {e}"]
    except Exception as e:
        return [f"Error reading file: {e}"]
    
    if not isinstance(data, dict):
        return ["YAML file must contain a dictionary/object"]
    
    # Check required fields
    required_fields = ['subdomain', 'owner', 'email', 'description', 'record_type', 'record_value']
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Validate subdomain
    if 'subdomain' in data:
        if not validate_subdomain(data['subdomain']):
            errors.append(f"Invalid subdomain: {data['subdomain']}. Must be lowercase alphanumeric with hyphens, 1-63 characters")
        
        # Check if filename matches subdomain
        filename = Path(filepath).stem
        if filename != 'example' and data['subdomain'] != filename:
            errors.append(f"Filename '{filename}.yaml' must match subdomain '{data['subdomain']}'")
    
    # Validate email
    if 'email' in data and not validate_email(data['email']):
        errors.append(f"Invalid email address: {data['email']}")
    
    # Validate record type
    if 'record_type' in data and not validate_record_type(data['record_type']):
        errors.append(f"Invalid record_type: {data['record_type']}. Must be one of: A, AAAA, CNAME, TXT")
    
    # Validate TTL if present
    if 'ttl' in data:
        try:
            ttl = int(data['ttl'])
            if ttl < 60 or ttl > 86400:
                errors.append("TTL must be between 60 and 86400 seconds")
        except (ValueError, TypeError):
            errors.append("TTL must be a number")
    
    # Validate proxied if present
    if 'proxied' in data and not isinstance(data['proxied'], bool):
        errors.append("'proxied' must be true or false")
    
    # Validate record_value is not empty
    if 'record_value' in data and not data['record_value']:
        errors.append("record_value cannot be empty")
    
    return errors

def check_duplicate_subdomains(domains_dir):
    """Check for duplicate subdomain entries"""
    subdomains = {}
    duplicates = []
    
    for filepath in Path(domains_dir).glob('*.yaml'):
        if filepath.stem == 'example':
            continue
            
        try:
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)
                if isinstance(data, dict) and 'subdomain' in data:
                    subdomain = data['subdomain']
                    if subdomain in subdomains:
                        duplicates.append(f"Duplicate subdomain '{subdomain}' in {filepath.name} and {subdomains[subdomain]}")
                    else:
                        subdomains[subdomain] = filepath.name
        except Exception:
            # Skip files that can't be read or parsed
            pass
    
    return duplicates

def main():
    domains_dir = Path(__file__).parent.parent / 'domains'
    
    if not domains_dir.exists():
        print(f"Error: domains directory not found at {domains_dir}")
        sys.exit(1)
    
    yaml_files = list(domains_dir.glob('*.yaml'))
    
    if not yaml_files:
        print("No YAML files found in domains/ directory")
        sys.exit(0)
    
    all_errors = []
    
    # Validate each file
    for filepath in yaml_files:
        if filepath.stem == 'example':
            continue  # Skip example file
            
        print(f"Validating {filepath.name}...")
        errors = validate_yaml_file(filepath)
        
        if errors:
            all_errors.append(f"\n{filepath.name}:")
            for error in errors:
                all_errors.append(f"  - {error}")
    
    # Check for duplicates
    duplicates = check_duplicate_subdomains(domains_dir)
    if duplicates:
        all_errors.append("\nDuplicate subdomain errors:")
        for dup in duplicates:
            all_errors.append(f"  - {dup}")
    
    if all_errors:
        print("\n❌ Validation failed:")
        for error in all_errors:
            print(error)
        sys.exit(1)
    else:
        print("\n✅ All subdomain requests are valid!")
        sys.exit(0)

if __name__ == '__main__':
    main()
