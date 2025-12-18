# Contributing to Netref Registry

Thank you for your interest in registering a subdomain with Netref! This guide will walk you through the process.

## How to Request a Subdomain

### Step 1: Fork the Repository

1. Fork this repository to your GitHub account
2. Clone your fork to your local machine

### Step 2: Create Your Subdomain Request

1. Copy the `domains/example.yaml` file
2. Rename it to `<your-subdomain>.yaml` (e.g., `mysite.yaml`)
3. Fill in your information:

```yaml
# Required: The subdomain you want to register
subdomain: mysite

# Required: Your name or organization name
owner: Your Name

# Required: Contact email for administrative purposes
email: your.email@example.com

# Required: Description of how this subdomain will be used
description: My personal website

# Required: DNS record type (A, AAAA, CNAME, TXT)
record_type: CNAME

# Required: DNS record value (IP address for A/AAAA, domain for CNAME, etc.)
record_value: yourusername.github.io

# Optional: TTL (Time To Live) in seconds, defaults to 3600 (1 hour)
ttl: 3600

# Optional: Proxy through Cloudflare (true/false), defaults to false
proxied: false
```

### Step 3: Submit Your Request

1. Commit your changes:
   ```bash
   git add domains/mysite.yaml
   git commit -m "Add subdomain request for mysite"
   git push origin main
   ```

2. Create a Pull Request to this repository
3. Wait for validation - a GitHub Action will automatically validate your request
4. An administrator will review and approve your request

### Step 4: DNS Updates

Once your pull request is approved and merged:
- A GitHub Action will automatically update the Cloudflare DNS
- Your subdomain will be active within a few minutes
- You'll receive a confirmation comment on your PR

## Subdomain Guidelines

### Naming Requirements

- Subdomains must be lowercase
- Can contain letters (a-z), numbers (0-9), and hyphens (-)
- Must be between 1 and 63 characters
- Cannot start or end with a hyphen
- Must be unique (not already registered)

### Allowed Record Types

- **A**: IPv4 address (e.g., `192.0.2.1`)
- **AAAA**: IPv6 address (e.g., `2001:db8::1`)
- **CNAME**: Canonical name pointing to another domain (e.g., `example.github.io`)
- **TXT**: Text record (e.g., for verification)

### Usage Requirements

Your subdomain should be used for:
- Personal websites or blogs
- Open source projects
- Educational content
- Non-commercial community projects

### Prohibited Uses

Subdomains will not be approved for:
- Illegal content or activities
- Spam or phishing
- Malware distribution
- Harassment or hate speech
- Commercial advertising (without prior approval)
- Impersonation

## What Happens Next?

1. **Validation** (automatic): Your YAML file is checked for correct format
2. **Review** (manual): An admin reviews your request for compliance
3. **Approval** (manual): Admin merges your PR
4. **DNS Update** (automatic): Cloudflare DNS is updated via GitHub Actions
5. **Active** (within minutes): Your subdomain is live!

## Need Help?

- Check the `domains/example.yaml` file for a complete example
- Review existing approved requests in the `domains/` directory
- Open an issue if you have questions

## Security Note

Never include API keys, passwords, or other sensitive information in your YAML file. All files in this repository are public.
