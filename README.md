# IssueScope

> AI-powered research and question-answering platform for SEBI IPO prospectuses.

## Problem

Every month, around 20–40 new Draft Red Herring Prospectuses (DRHPs) are filed with SEBI, with each document often containing 300–600 pages. Investor-education content teams need to analyze sections such as risk factors, objects of the issue, financial information, promoter details, and outstanding litigation before an IPO opens. Manually reading these documents is time-consuming, causing research notes to be late or incomplete. IssueScope processes SEBI prospectuses and allows users to ask questions across them while receiving answers backed by citations to the original documents.

## Who it is for

Investor-education content leads and financial research analysts at Indian retail stockbrokers who prepare plain-language IPO research for retail investors.

## Signature feature

A daily **New Filing Digest** that automatically identifies newly filed DRHPs and summarizes the issue size, promoter selling information, and top three risk factors with citations to the original prospectus.

## Hardest problem (my interview story)

The hardest engineering problem is reliably ingesting more than **30,000 pages of large and sometimes scanned prospectus PDFs**. IssueScope uses resumable background workers with a Redis-backed job queue, document-level progress tracking, retries for failed downloads and processing jobs, and OCR fallback for scanned documents. The ingestion pipeline is designed so that if a worker crashes midway through processing, completed work is preserved and the failed job can resume or retry without losing documents. It also periodically checks SEBI filings so newly published prospectuses can automatically enter the processing pipeline.

## Dataset

| Source | Link | Documents | Pages | Licence / terms |
|---|---|---:|---:|---|
| SEBI Public Issues – Draft Offer Documents | https://www.sebi.gov.in/filings/public-issues.html | 100+ | 30,000+ | Publicly available regulatory filings; use subject to SEBI website terms |

The initial dataset consists of Draft Red Herring Prospectuses (DRHPs), Red Herring Prospectuses (RHPs), and addenda filed with SEBI over approximately the last two years. The project targets a minimum of **100 prospectuses and 30,000+ pages**.

## 10 real questions

See [docs/QUESTIONS.md](docs/QUESTIONS.md).

Example questions IssueScope is designed to answer include:

1. How much of Sambcorp Green Infra's issue is fresh issue versus offer for sale?
2. List the top five risk factors in the latest DRHP filed by a pharmaceutical company.
3. Which DRHPs filed this quarter disclose pending tax cases above ₹100 crore?
4. What are the objects of the issue for a selected IPO?
5. What outstanding litigation has been disclosed by the company?
6. What are the major risks associated with the company's business?
7. How will the company use the proceeds from the fresh issue?
8. Who are the promoters and how much are they selling through the offer for sale?
9. How have the company's revenue and profit changed over the last three financial years?
10. How does the company's valuation compare with its listed industry peers?

## Run it

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env                               # Windows: copy .env.example .env
uvicorn app.main:app --reload
curl localhost:8000/health
```

## Live link

<Added in Week 2>