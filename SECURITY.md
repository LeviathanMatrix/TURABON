# Security

## Reporting a vulnerability

Please report suspected security issues privately to `cc@leviathanmatrix.com`. Do not include live Agent API keys, payment credentials, provider credentials, personal data, or exploitable details in a public GitHub issue.

Include the affected public endpoint, the minimum steps needed to reproduce the issue, the observed result, and the expected result. TURABON may ask for additional evidence through a private channel.

## Exposed credentials

If an Agent API key is exposed:

1. Revoke or rotate it immediately in TURABON Runtime access.
2. Remove it from local files and logs.
3. If committed to Git, treat it as compromised even after deleting the line.
4. Do not reuse it.

This repository never needs a TURABON server secret, provider API key, Stripe key, wallet key, database credential, or GitHub token.
