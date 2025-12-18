# Netref Registry

The Netref Registry is a free, neutral, and transparent subdomain reference system. It allows users to request free subdomains for `netref.link` and helps safely delegate DNS records while maintaining trust and auditability.

## 🚀 Quick Start

Want a free subdomain? Here's how:

1. **Fork this repository**
2. **Copy `domains/example.yaml`** and rename it to `yourname.yaml`
3. **Fill in your details** (subdomain, DNS records, contact info)
4. **Submit a Pull Request**
5. **Wait for approval** - your subdomain will be live within minutes!

📚 **Documentation:**
- [Quick Reference Guide](QUICKSTART.md) - Fast overview
- [Contributing Guide](CONTRIBUTING.md) - Detailed instructions

## 📝 Example Subdomain Request

Create a file `domains/mysite.yaml`:

```yaml
subdomain: mysite
owner: John Doe
email: john@example.com
description: My personal website
record_type: CNAME
record_value: johndoe.github.io
ttl: 3600
proxied: false
```

This creates `mysite.netref.link` pointing to your site!

## 🎯 Features

- **Free Subdomains**: Get your own `.netref.link` subdomain
- **Automated Validation**: GitHub Actions automatically validate your request
- **Instant Updates**: DNS updates happen automatically upon approval
- **Transparent**: All requests and approvals are public via Git history
- **Flexible**: Support for A, AAAA, CNAME, and TXT records

## 🔧 How It Works

1. **Submit**: Users submit subdomain requests via YAML files in pull requests
2. **Validate**: GitHub Actions automatically validate the format and uniqueness
3. **Review**: Administrators review and approve requests
4. **Deploy**: Upon merge, GitHub Actions update Cloudflare DNS automatically

## 📚 Documentation

- [Contributing Guide](CONTRIBUTING.md) - How to request a subdomain
- [Example Request](domains/example.yaml) - Template for subdomain requests

## 📜 License

This project is open source and follows the principle of transparent subdomain allocation.

## 🤝 Community

- Open an issue for questions or support
- Star this repository to show your support
- Share with others who might need a free subdomain!
