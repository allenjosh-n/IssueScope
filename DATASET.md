# Dataset

| File | Source URL | Pages | Licence / terms | Downloaded on |
|---|---|---|---|---|
| Sambcorp_Green_Infra_DRHP.pdf | https://www.sebi.gov.in/filings/public-issues.html | 408 | Publicly available regulatory filing; use subject to SEBI website terms | 2024-10-21 |
| Blackbuck_RHP.pdf | https://www.sebi.gov.in/filings/public-issues.html | 512 | Publicly available regulatory filing; use subject to SEBI website terms | 2024-10-21 |
| Afcons_Infrastructure_DRHP.pdf | https://www.sebi.gov.in/filings/public-issues.html | 634 | Publicly available regulatory filing; use subject to SEBI website terms | 2024-10-21 |

Full data lives in `data/raw/` (not committed). A 2–3 file sample is in `data/sample/`.

## Coverage

The initial dataset targets **100+ prospectuses** and **30,000+ pages** sourced from SEBI's public-issues filing portal.
Document types: Draft Red Herring Prospectuses (DRHPs), Red Herring Prospectuses (RHPs), and addenda filed over approximately the last two years.

## Download tool

```bash
python app/tools/download.py app/tools/urls.txt
```

Downloads to `data/raw/`, respects `robots.txt`, enforces a 2-second delay between requests,
and logs each file to `data/manifest.csv` (path, source URL, date, bytes, SHA-256 prefix).
