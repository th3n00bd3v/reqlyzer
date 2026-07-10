from models.request import AnalyzedRequest


class PromptBuilder:
    """
    Builds prompts for the AI model.

    This class converts analyzed requests and HAR captures
    into prompts that generate clear, user-friendly
    explanations suitable for non-technical users.
    """

    def build_request_prompt(
        self,
        request: AnalyzedRequest,
    ) -> str:

        findings = []

        for finding in request.security.findings:

            findings.append(
                f"- {finding.severity}: {finding.title}"
            )

        findings_text = (
            "\n".join(findings)
            if findings
            else "None"
        )

        recommendations = (
            "\n".join(
                f"- {rec}"
                for rec in request.risk.recommendations
            )
            or "None"
        )

        return f"""
You are Reqlyzer AI.

Your purpose is to explain backend network requests in simple,
friendly language.

Assume the reader has little or no cybersecurity knowledge.

Avoid technical jargon whenever possible.

Request Information

Method:
{request.method}

Host:
{request.host}

Endpoint:
{request.path}

Status Code:
{request.status_code}

Risk Level:
{request.risk.level}

Risk Score:
{request.risk.score}/100

Application Summary:
{request.analysis.summary}

What Happened:
{request.analysis.what}

Who Made the Request:
{request.analysis.who}

Purpose:
{request.analysis.why}

Destination:
{request.analysis.where}

Connection Details:
{request.analysis.how}

Security Findings

{findings_text}

Recommendations

{recommendations}

Instructions

Write between 40 and 80 words.

Explain:

• What this request is doing.
• Whether it appears to be normal website activity.
• If there is anything the user should know.
• Mention any important security concern in simple language.

If the request appears harmless, clearly reassure the user.

Do not repeat the information already shown above.

Do not use bullet points.

Avoid words like:

- security posture
- assessment
- comprehensive
- observed
- utilized
- indicates
- demonstrates
- vulnerability assessment

Write naturally, like a helpful browser assistant.
""".strip()

    def build_har_summary_prompt(
        self,
        requests: list[AnalyzedRequest],
    ) -> str:

        total = len(requests)

        low = 0
        medium = 0
        high = 0
        critical = 0

        hosts = {}

        methods = {}

        for request in requests:

            hosts[request.host] = (
                hosts.get(request.host, 0) + 1
            )

            methods[request.method] = (
                methods.get(request.method, 0) + 1
            )

            level = request.risk.level

            if level == "Low":
                low += 1

            elif level == "Medium":
                medium += 1

            elif level == "High":
                high += 1

            elif level == "Critical":
                critical += 1

        top_hosts = sorted(
            hosts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        top_methods = sorted(
            methods.items(),
            key=lambda x: x[1],
            reverse=True
        )

        host_summary = "\n".join(
            f"- {host}: {count} requests"
            for host, count in top_hosts
        )

        method_summary = "\n".join(
            f"- {method}: {count}"
            for method, count in top_methods
        )

        return f"""
You are Reqlyzer AI.

Your job is to explain an application's network activity
to a normal computer user.

The HAR file has already been analyzed.

Statistics

Total Requests:
{total}

Unique Hosts:
{len(hosts)}

Risk Distribution

Low: {low}

Medium: {medium}

High: {high}

Critical: {critical}

Most Active Hosts

{host_summary}

HTTP Methods

{method_summary}

Instructions

Write an executive summary between 120 and 180 words.

Organize the response using these headings:

### Overall Activity

Briefly describe what the browsing session was doing.

### Security Overview

Explain whether anything unusual or risky was detected.

### Interesting Findings

Mention two or three noteworthy observations.

### Overall Verdict

Finish with one simple conclusion that tells the user whether
the browsing session appears normal.

Rules

- Use simple, friendly language.
- Avoid cybersecurity jargon.
- Do not repeat the statistics above.
- Do not invent vulnerabilities.
- If nothing serious was found, clearly reassure the user.
- Do not sound like a penetration tester or consultant.
- Keep the tone informative and easy to understand.


Format the response using Markdown.

Use exactly this structure:

# Executive Summary

## Overall Activity

<2-3 sentences>

## Security Overview

<2-3 sentences>

## Interesting Findings

<2-3 sentences>

## Overall Verdict

<2-3 sentences>

## Recommendations

- Recommendation 1
- Recommendation 2
- Recommendation 3

Rules:
- Place each heading on its own line.
- Leave one blank line after each heading.
- Keep the response under 250 words.
- Do not include the statistics already shown in the dashboard.

""".strip()