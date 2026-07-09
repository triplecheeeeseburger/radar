# One-time setup (~10 min)

## 1. Create the repo

- github.com → New repository → name `radar`, Public, no README.
- Upload this folder's contents (or I'll push once you give me a token — step 3).

## 2. Enable GitHub Pages

- Repo → Settings → Pages → Source: **Deploy from a branch** → `main` / `/ (root)` → Save.

## 3. Token so Claude can deploy

- github.com → Settings → Developer settings → **Fine-grained personal access tokens** → Generate.
- Repository access: **Only select repositories → `radar`**.
- Permissions: **Contents → Read and write**. Nothing else.
- Expiration: 90 days. Paste the token to me in chat; it's scoped to this one repo and revocable anytime at the same page.

## 4. DNS for radar.danberte.com

At your DNS provider (Cloudflare, by the look of danberte.com):

| Type  | Name    | Target                  |
|-------|---------|-------------------------|
| CNAME | `radar` | `<your-gh-username>.github.io` |

If Cloudflare: set the record to **DNS only** (grey cloud) initially so GitHub can issue the cert, then Repo → Settings → Pages → Custom domain: `radar.danberte.com` → wait for check → tick **Enforce HTTPS**.

## 5. Weekly automation (optional)

Ask me to schedule a task: every Friday 4 PM I compile the week, cut the archive, and push — plus a note in chat with what shipped.

## Security posture

- No server, no database, no forms, no JS on the published site → effectively no attack surface beyond GitHub Pages itself.
- Write access is a single fine-grained token limited to one repo's contents.
- All content passes through you/me before publish — nothing auto-ingests from the internet.
