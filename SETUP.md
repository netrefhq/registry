# Administrator Setup Guide

This guide is for repository administrators who need to configure the subdomain registry system.

## Prerequisites

- GitHub repository with admin access
- Cloudflare account with DNS management for `netref.link`
- Cloudflare API token with DNS edit permissions

## Initial Setup

### 1. Cloudflare Configuration

#### Create API Token

1. Log in to Cloudflare Dashboard
2. Go to **My Profile** > **API Tokens**
3. Click **Create Token**
4. Use the **Edit zone DNS** template
5. Configure:
   - **Permissions**: Zone > DNS > Edit
   - **Zone Resources**: Include > Specific zone > `netref.link`
6. Create the token and **copy it immediately** (you won't see it again)

#### Get Zone ID

1. Go to your domain overview in Cloudflare
2. Scroll down to find **Zone ID** in the right sidebar
3. Copy the Zone ID

### 2. GitHub Secrets Configuration

Add these secrets to your GitHub repository:

1. Go to **Settings** > **Secrets and variables** > **Actions**
2. Click **New repository secret**
3. Add the following secrets:

   - `CLOUDFLARE_API_TOKEN`: Your Cloudflare API token
   - `CLOUDFLARE_ZONE_ID`: Your Cloudflare Zone ID

### 3. Repository Configuration

The repository is now configured with two GitHub Actions workflows:

- **validate.yml**: Runs on every pull request to validate subdomain requests
- **update-dns.yml**: Runs when a pull request is merged to update Cloudflare DNS

## Workflow

### For New Subdomain Requests

1. **User submits PR**: User adds a YAML file in `domains/` directory
2. **Automatic validation**: GitHub Actions validate the request
3. **Admin review**: You review the request for:
   - Appropriate use case
   - No malicious content
   - Compliance with guidelines
4. **Approve and merge**: Merge the PR
5. **Automatic DNS update**: GitHub Actions update Cloudflare DNS
6. **Confirmation**: User receives confirmation comment

### Manual DNS Management

If you need to update DNS manually:

```bash
# Install dependencies
pip install -r requirements.txt

# Validate all requests
python scripts/validate.py

# Update Cloudflare DNS (dry-run first)
export CLOUDFLARE_API_TOKEN="your-token"
export CLOUDFLARE_ZONE_ID="your-zone-id"
python scripts/update_cloudflare.py --dry-run

# Update for real
python scripts/update_cloudflare.py
```

## Monitoring

### Check Workflow Status

1. Go to **Actions** tab in GitHub
2. Review recent workflow runs
3. Check for failures

### Common Issues

#### Validation Failures

- User didn't follow YAML format
- Invalid subdomain name
- Duplicate subdomain request
- Missing required fields

**Solution**: Comment on PR with specific errors, user needs to fix

#### DNS Update Failures

- Invalid Cloudflare credentials
- API rate limiting
- Zone ID mismatch

**Solution**: Check GitHub Actions logs, verify secrets, retry if needed

## Security Considerations

1. **Protect secrets**: Never expose API tokens in code or logs
2. **Review requests**: Always review subdomain requests before approving
3. **Monitor usage**: Regularly check for abuse
4. **Rate limiting**: Be aware of Cloudflare API rate limits
5. **Backup**: Keep regular backups of DNS records

## API Rate Limits

Cloudflare API limits:

- **Free plan**: 1,200 requests per 5 minutes
- **Paid plans**: Higher limits

With automatic updates on merge, this is typically sufficient for most use cases.

## Maintenance

### Regular Tasks

- Review and approve subdomain requests
- Monitor for abuse or misuse
- Update documentation as needed
- Check Cloudflare for proper DNS configuration

### Updating Scripts

If you need to modify the validation or update scripts:

1. Test changes locally first
2. Use dry-run mode for Cloudflare updates
3. Update documentation
4. Create a PR for review

## Troubleshooting

### Validation Script Issues

```bash
# Test validation locally
python scripts/validate.py

# Check for YAML syntax errors
python -c "import yaml; yaml.safe_load(open('domains/subdomain.yaml'))"
```

### Cloudflare Update Issues

```bash
# Test API connection
curl -X GET "https://api.cloudflare.com/client/v4/user/tokens/verify" \
  -H "Authorization: Bearer YOUR_API_TOKEN"

# List existing DNS records
curl -X GET "https://api.cloudflare.com/client/v4/zones/YOUR_ZONE_ID/dns_records" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

## Support

For issues or questions:

- Check GitHub Actions logs
- Review Cloudflare audit log
- Open an issue in the repository
- Contact Cloudflare support for API issues

## Best Practices

1. **Review carefully**: Check each request before approval
2. **Document changes**: Use clear commit messages
3. **Communicate**: Add comments to PRs when requesting changes
4. **Monitor**: Regularly check for issues
5. **Backup**: Keep DNS records backed up externally
6. **Test**: Use dry-run mode when testing changes
