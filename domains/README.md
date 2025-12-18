# Subdomain Requests

This directory contains all approved subdomain requests for `netref.link`.

## How to Add Your Subdomain

1. Copy `example.yaml` to a new file named `<your-subdomain>.yaml`
2. Fill in your details
3. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed instructions.

## Active Subdomains

Each YAML file in this directory represents an active subdomain:

- `example.yaml` - Template file (not active)
- `test.yaml` - Test subdomain for validation

## File Format

Each YAML file must contain:

```yaml
subdomain: yourname        # Required: subdomain name (lowercase, alphanumeric, hyphens)
owner: Your Name           # Required: owner name or organization
email: you@example.com     # Required: contact email
description: Purpose       # Required: description of use
record_type: CNAME         # Required: A, AAAA, CNAME, or TXT
record_value: target.com   # Required: DNS target
ttl: 3600                  # Optional: TTL in seconds (default: 3600)
proxied: false             # Optional: Cloudflare proxy (default: false)
```

## Validation

All files are automatically validated when you submit a pull request. The validation checks:

- ✅ Required fields are present
- ✅ Subdomain name is valid (lowercase, alphanumeric, hyphens only)
- ✅ Email format is valid
- ✅ Record type is supported
- ✅ No duplicate subdomains
- ✅ Filename matches subdomain name
