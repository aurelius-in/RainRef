# Security Notes

This document captures practical guidance to operate RainRef securely in production.

## Secrets Management
- Store secrets (JWT_SECRET, RAINBEACON_SECRET, adapter tokens, DATABASE_URL) in a managed secrets store (e.g., GitHub Encrypted Secrets, AWS SSM/Secrets Manager, Azure Key Vault).
- Never commit secrets to source control. Use .env files only for local development.
- Rotate secrets on a schedule (e.g., 90 days) and on personnel changes.
- For JWT rotation, support overlapping keys during a cutover window or force refresh by shortening token lifetimes temporarily.

## Authentication & Authorization
- Set REQUIRE_JWT_FOR_ADMIN=true in production.
- Limit admin access to SSO-backed users; consider adding an IdP in front of the API gateway.
- Enforce least-privilege roles in tokens (admin, support_lead, support, user).

## Policies (OPA)
- Expand coverage to all action types; add explicit deny reasons for missing parameters and role mismatch.
- Version and test policies alongside code; validate with CI.

## Transport & Headers
- Terminate TLS at an ingress/proxy; enable HSTS by setting ENABLE_HSTS=true.
- Review CSP connect-src for your API/UI/CDN domains.
- COOP/COEP/CORP are enabled by default to reduce cross-origin risks.

## Rate Limiting
- Enable Redis-backed limiter for multi-replica deployments: USE_REDIS_LIMITER=true and configure REDIS_URL.
- Tune rate_limit_window_sec and rate_limit_per_window per environment.

## Backups & Recovery
- Use scripts/pg_backup.sh and scripts/pg_restore.sh for ad-hoc backups. Prefer scheduled snapshots in your cloud provider.
- Test restores regularly.

## Observability
- Configure OTEL_EXPORTER_OTLP_ENDPOINT; collect traces/logs/metrics centrally.
- Add dashboards for request rates, error rates, latency, and policy denies.

## Supply Chain & CI/CD
- Lock base images by digest; run CI on PRs; require status checks for protected branches.
- Use the release workflow to build and publish images on signed tags.

## Data Protection
- Scope database users to least privilege.
- Consider row-level encryption or KMS for sensitive fields where applicable.


