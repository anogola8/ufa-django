# UFA Django Platform — `core` + `accounts`

This is the first slice of the rebuild: foundation (`core`) and auth (`accounts`)
apps, built and verified per the architecture doc. Everything else
(`events`, `news`, `gallery`, `projects`, `communications`, `reports`,
`dashboard`) gets added the same way, one app at a time, in the dependency
order laid out in `UFA_Architecture_and_ERD.md`.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env: set a real SECRET_KEY. Leave DB_NAME blank to use local
# sqlite for development, or fill in DB_NAME/DB_USER/DB_PASSWORD/DB_HOST
# to point at Postgres.

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the public home page,
`/accounts/register/` to create a member account, and `/admin/` for the
Django admin (log in with the superuser you just created).

## What's here

- `config/` — project settings, root URLs. Reads all config from `.env`
  via `python-decouple` — no secrets hardcoded, unlike the original repo.
- `core/` — `County`, `Ward`, `SiteSetting`, `Document`, `AuditLog` models;
  `core/services.py` has `log_action()`, the one function every app should
  use to write audit entries, so logging stays consistent project-wide.
- `accounts/` — custom `User` model (email login, `role` field, MFA-ready
  fields), register/login/logout/profile views + templates.
- `templates/base.html` — expects Bootstrap 5 vendored locally at
  `static/vendor/bootstrap/bootstrap.min.css` (currently an empty
  placeholder file) rather than pulled from a CDN, since the real
  deployment target is the air-gapped internal network mentioned in your
  other project context. Swap in the real Bootstrap 5 CSS/JS before this
  goes further than local dev.

## Verified before hand-off

- `manage.py check` clean
- Migrations generate and apply without conflicts
- `createsuperuser` works through the custom email-based manager
- Full register → login → profile flow tested via Django's test client
  (200/302 responses as expected, `AuditLog` entry written on registration)
- `Ward(county, name)` uniqueness constraint rejects duplicates at the DB
  level, as designed in the ERD
- `User.is_admin` / `is_staff_or_above` helper properties behave correctly
  for superuser vs. ordinary member

## Known gaps / next steps

- `LOGIN_REDIRECT_URL` points at `accounts:profile` — change to
  `dashboard:index` once the `dashboard` app exists (flagged with a TODO
  in `config/settings.py`).
- No tests directory yet (`accounts/tests.py` / `core/tests.py` are the
  default empty stubs) — add real test cases as each app's behavior
  stabilizes, rather than writing tests against code that will still
  change shape.
- MFA fields exist on `User` but there's no TOTP enrollment/verification
  flow yet — data model is ready, the flow isn't built.
- `mfa_secret` should be encrypted at rest once a real
  encryption-at-rest/KMS approach is chosen for the production
  deployment; it's a plain `CharField` for now.
- Seed data migration for Kenya's 47 counties/wards hasn't been written —
  `County`/`Ward` tables are empty until that's added or entered via admin.
