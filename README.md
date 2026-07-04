# Reqlyzer - Requests Analyzer

## Project Goal

Build a working prototype that accepts an exported HAR file from a browser, analyzes every backend request, identifies security-relevant information, and generates an AI-powered explanation using the "What, Who, Why, Where, and How" framework.

---

# Recommended Technology Stack

## Backend

* Python 3.12+
* FastAPI
* Uvicorn

## Frontend

* HTML
* Bootstrap 5
* JavaScript

## AI

* Ollama (Llama 3.2 3B or Mistral 7B)
* LangChain (optional, only if time permits)

## Data Processing

* JSON
* pandas
* haralyzer (or manual HAR parsing)

## Database (Optional)

* SQLite

---

# Day 1 (Today – 4–5 Hours)

## Goal

Create the project skeleton.

### Tasks

* Create Git repository
* Create FastAPI project
* Create frontend
* Create upload page
* Upload HAR file
* Read HAR JSON successfully
* Display request count

### Deliverable

```
HAR uploaded successfully

Total Requests:
126
```

---

# Day 2 (Tomorrow – 4–5 Hours)

## Goal

Parse every request.

Extract

* Method
* URL
* Host
* Headers
* Cookies
* Query Parameters
* Body
* Status Code
* Response Headers
* Response Time

Display them in a clean table.

### Deliverable

```
GET

/users/profile

Status
200

Host
api.example.com

Response Time
120 ms
```

---

# Day 3 (Monday – 1–2 Hours)

## Goal

Build the Metadata Extraction Engine.

Identify

* JWT
* API Keys
* Bearer Tokens
* Password Fields
* Email Addresses
* Cookies
* Authorization Headers
* HTTPS
* Content-Type

Generate structured metadata like

```json
{
  "authentication": "Bearer Token",
  "contains_password": true,
  "contains_email": true,
  "contains_cookie": true,
  "https": true
}
```

---

# Day 4 (Tuesday – 1–2 Hours)

## Goal

Security Analysis Engine.

Detect

* Passwords in plaintext
* HTTP instead of HTTPS
* Missing Authorization
* Missing Secure Cookie
* Missing HttpOnly
* Missing SameSite
* File Uploads
* Dangerous HTTP Methods
* Sensitive Endpoints

Assign severity

* Low
* Medium
* High

---

# Day 5 (Wednesday – 1–2 Hours)

## Goal

Implement AI Analysis.

Prompt

```
Analyze the following HTTP request.

Explain:

What
Who
Why
Where
How

Sensitive Data

Authentication

Potential Risks

Recommendations
```

Return Markdown.

Display inside the frontend.

---

# Day 6 (Thursday – 1–2 Hours)

## Goal

Create Risk Score.

Example

| Check                 | Score |
| --------------------- | ----: |
| HTTPS                 |   +10 |
| Authorization         |   +10 |
| JWT                   |    +5 |
| Password              |   -20 |
| HTTP                  |   -40 |
| Missing Secure Cookie |   -15 |

Display

```
Risk Score

82/100

Medium Risk
```

---

# Day 7 (Friday – 1–2 Hours)

## Goal

Improve UI.

Dashboard

* Upload HAR
* Requests List
* Request Details
* AI Analysis
* Security Findings
* Risk Score

Add

* Search
* Filters
* Color-coded severity badges

---

# Saturday (Buffer & Demo Preparation)

## Polish

* Fix bugs
* Improve styling
* Test with multiple HAR files
* Prepare screenshots
* Record a demo video (optional)

---

# Minimum Features for the MVP

✅ Upload HAR file

✅ Parse requests

✅ Display request information

✅ Detect sensitive information

✅ Detect security issues

✅ Risk scoring

✅ AI-generated explanation

✅ Dashboard

---

# Stretch Goals (Only If Time Allows)

* Export PDF report
* SQLite history
* Endpoint grouping
* AI chat ("Explain this request")
* Response comparison
* OWASP Top 10 mapping
* mitmproxy live traffic capture
* PCAP import
* API documentation generation

---

# Suggested Folder Structure

```
Reqlyzer/

├── backend/
│   ├── app.py
│   ├── parser.py
│   ├── analyzer.py
│   ├── ai.py
│   ├── scoring.py
│   ├── report.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   ├── styles.css
│
├── uploads/
│
├── sample_data/
│   └── sample.har
│
├── reports/
│
└── README.md
```

---

# Final Deliverable

By the end of the week, Reqlyzer should support the following workflow:

1. User uploads a HAR file.
2. The backend extracts all HTTP requests and responses.
3. The parser identifies request metadata, authentication mechanisms, headers, cookies, and sensitive fields.
4. The security engine evaluates each request for common risks and assigns a severity level and risk score.
5. The AI generates a concise explanation covering:

   * What the request does
   * Who initiated it
   * Why it exists
   * Where it is sent
   * How it communicates
   * Potential security concerns
   * Recommendations
6. The dashboard presents the analysis in a searchable, human-readable format suitable for demonstrations and project evaluation.

This MVP demonstrates networking fundamentals, HTTP analysis, secure coding concepts, AI-assisted security analysis, and practical web application development while remaining achievable within one week.
