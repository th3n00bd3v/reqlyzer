/*
====================================================
Method Badge
====================================================
*/

function methodBadge(method) {

    switch ((method || "").toUpperCase()) {

        case "GET":
            return '<span class="badge bg-primary">GET</span>';

        case "POST":
            return '<span class="badge bg-success">POST</span>';

        case "PUT":
            return '<span class="badge bg-warning text-dark">PUT</span>';

        case "PATCH":
            return '<span class="badge bg-info text-dark">PATCH</span>';

        case "DELETE":
            return '<span class="badge bg-danger">DELETE</span>';

        case "OPTIONS":
            return '<span class="badge bg-secondary">OPTIONS</span>';

        case "HEAD":
            return '<span class="badge bg-dark">HEAD</span>';

        default:
            return `<span class="badge bg-light text-dark">${method || "-"}</span>`;

    }

}

/*
====================================================
Risk Badge
====================================================
*/

function riskBadge(level) {

    switch (level) {

        case "Low":
            return '<span class="badge bg-success">Low</span>';

        case "Medium":
            return '<span class="badge bg-warning text-dark">Medium</span>';

        case "High":
            return '<span class="badge bg-danger">High</span>';

        case "Critical":
            return '<span class="badge bg-dark">Critical</span>';

        default:
            return '<span class="badge bg-secondary">Unknown</span>';

    }

}

/*
====================================================
Display Request Details
====================================================
*/

function showRequestDetails(request) {

    //--------------------------------------------------
    // 5W1H
    //--------------------------------------------------

    document.getElementById("whatText").textContent =
        request.analysis?.what || "-";

    document.getElementById("whoText").textContent =
        request.analysis?.who || "-";

    document.getElementById("whyText").textContent =
        request.analysis?.why || "-";

    document.getElementById("whereText").textContent =
        request.analysis?.where || "-";

    document.getElementById("howText").textContent =
        request.analysis?.how || "-";

    //--------------------------------------------------
    // Security Findings
    //--------------------------------------------------

    const findingsDiv =
        document.getElementById("securityFindings");

    findingsDiv.innerHTML = "";

    const findings =
        request.security?.findings || [];

    if (findings.length === 0) {

        findingsDiv.innerHTML = `

            <div class="alert alert-success mb-0">

                No security findings detected.

            </div>

        `;

    } else {

        findings.forEach(finding => {

            let badge = "secondary";

            switch (finding.severity) {

                case "Info":
                    badge = "primary";
                    break;

                case "Low":
                    badge = "success";
                    break;

                case "Medium":
                    badge = "warning";
                    break;

                case "High":
                    badge = "danger";
                    break;

                case "Critical":
                    badge = "dark";
                    break;

            }

            findingsDiv.innerHTML += `

                <div class="card mb-2 shadow-sm">

                    <div class="card-body">

                        <div class="d-flex justify-content-between align-items-center">

                            <strong>

                                ${finding.title}

                            </strong>

                            <span class="badge bg-${badge}">

                                ${finding.severity}

                            </span>

                        </div>

                        <p class="mt-2 mb-0">

                            ${finding.description}

                        </p>

                    </div>

                </div>

            `;

        });

    }

    //--------------------------------------------------
    // Recommendations
    //--------------------------------------------------

    const recommendations =
        document.getElementById("recommendations");

    recommendations.innerHTML = "";

    const recommendationList =
        request.risk?.recommendations || [];

    if (recommendationList.length === 0) {

        recommendations.innerHTML = `

            <li>

                No recommendations available.

            </li>

        `;

    } else {

        recommendationList.forEach(rec => {

            recommendations.innerHTML += `

                <li class="mb-2">

                    ${rec}

                </li>

            `;

        });

    }

}