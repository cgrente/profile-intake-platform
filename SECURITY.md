# Security Policy

## Supported Versions

This project is maintained as a portfolio-quality reference implementation.
Security fixes are provided for the latest version on the default branch.

| Version | Supported |
|--------:|:---------:|
| latest  | ✅        |
| older   | ❌        |

---

## Reporting a Vulnerability

If you discover a security vulnerability, please **do not** open a public GitHub issue.

Instead, use one of the following private reporting methods:

 **GitHub Security Advisories (preferred)**  
   - If this repository has Security Advisories enabled, please create a **private security advisory**.

---

## What to Include

When reporting a vulnerability, please include:

- A clear description of the issue and impact
- Steps to reproduce (proof-of-concept if possible)
- Affected endpoint(s) or component(s)
- Environment details (OS, Python version, Docker, etc.)
- Any relevant logs, stack traces, or screenshots

If you have a suggested fix, feel free to include it.

---

## Response Expectations

This project is maintained on a best-effort basis.  
If a report is confirmed, we will aim to:

- acknowledge the report
- provide a fix or mitigation guidance
- document the resolution in a release note or changelog (if applicable)

---

## Security Notes

This service uses a simplified authentication model (static Bearer token) for
demonstration and local development purposes.

If you deploy this project publicly, you should:
- use strong, rotated secrets
- restrict CORS origins
- use HTTPS (reverse proxy / ingress)
- consider OAuth/JWT or an identity provider
- run dependency scanning (Dependabot, osv-scanner, etc.)
