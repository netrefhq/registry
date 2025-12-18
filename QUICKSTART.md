# Quick Reference Guide

## For Users

### Request a Subdomain (3 Steps)

1. **Copy the template**
   ```bash
   cp domains/example.yaml domains/mysubdomain.yaml
   ```

2. **Fill in your details**
   ```yaml
   subdomain: mysubdomain
   owner: Your Name
   email: you@example.com
   description: What you'll use it for
   record_type: CNAME
   record_value: your-site.github.io
   ```

3. **Submit Pull Request**
   - Fork repo, commit changes, create PR
   - Wait for validation (automatic)
   - Admin reviews and merges
   - DNS updates automatically!

### Your subdomain will be: `mysubdomain.netref.link`

## Workflow Summary

```
User Submits PR
    ↓
[Automatic] Validate YAML
    ↓
Admin Reviews
    ↓
Admin Merges PR
    ↓
[Automatic] Update Cloudflare DNS
    ↓
Subdomain Active! 🎉
```

## Files Overview

```
.github/workflows/
  ├── validate.yml          # Validates PRs
  └── update-dns.yml        # Updates Cloudflare

domains/
  ├── README.md             # Domains directory info
  ├── example.yaml          # Template
  └── *.yaml                # Subdomain requests

scripts/
  ├── validate.py           # Validation logic
  └── update_cloudflare.py  # Cloudflare API integration

README.md                   # Project overview
CONTRIBUTING.md             # User guide
```

## Supported DNS Record Types

- **A**: IPv4 address
- **AAAA**: IPv6 address
- **CNAME**: Point to another domain
- **TXT**: Text records

## Common Use Cases

| Use Case | Record Type | Example Value |
|----------|-------------|---------------|
| GitHub Pages | CNAME | `username.github.io` |
| Static IP | A | `192.0.2.1` |
| Vercel/Netlify | CNAME | `app.vercel.app` |
| IPv6 Server | AAAA | `2001:db8::1` |
| Domain Verification | TXT | `verification-code` |

## Getting Help

- 📖 Read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions
- 💬 Open an issue for questions
- 🌟 Star the repo to show support!
