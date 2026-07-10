let allRequests = [];

/*
===========================================
Dashboard Rendering
===========================================
*/

function renderDashboard(result) {

    allRequests = result.requests || [];

    //---------------------------------------
    // Show Dashboard
    //---------------------------------------

    const analysisSection =
        document.getElementById("analysisSection");

    if (analysisSection) {

        analysisSection.classList.remove("d-none");

    }

    //---------------------------------------
    // Enable Clear Button
    //---------------------------------------

    const clearButton =
        document.getElementById("clearBtn");

    if (clearButton) {

        clearButton.disabled = false;

    }

    //---------------------------------------
    // AI Executive Summary
    //---------------------------------------

    const harSummary =
        document.getElementById("harSummary");

    if (harSummary) {

        const summary =
            result.har_summary ||
            "No AI summary available.";

        harSummary.innerHTML =
            marked.parse(summary);

    }

    updateSummary(allRequests);

    renderRequestTable(allRequests);

    setupSearch();

}

/*
===========================================
Summary Cards
===========================================
*/

function updateSummary(requests) {

    document.getElementById("totalRequests").textContent =
        requests.length;

    let low = 0;
    let medium = 0;
    let high = 0;
    let critical = 0;

    requests.forEach(request => {

        switch (request.risk?.level) {

            case "Low":
                low++;
                break;

            case "Medium":
                medium++;
                break;

            case "High":
                high++;
                break;

            case "Critical":
                critical++;
                break;

        }

    });

    document.getElementById("lowRisk").textContent = low;
    document.getElementById("mediumRisk").textContent = medium;
    document.getElementById("highRisk").textContent = high;
    document.getElementById("criticalRisk").textContent = critical;

}

/*
===========================================
Requests Table
===========================================
*/

function renderRequestTable(requests) {

    const tableBody =
        document.getElementById("requestsTable");

    tableBody.innerHTML = "";

    requests.forEach(request => {

        const row = document.createElement("tr");

        row.classList.add("request-row");

        row.innerHTML = `

            <td>${request.id}</td>

            <td>${methodBadge(request.method)}</td>

            <td>${request.host}</td>

            <td
                class="endpoint-column"
                title="${request.path || ""}">

                ${truncate(request.path || "-", 45)}

            </td>

            <td>${request.status_code}</td>

            <td>${riskBadge(request.risk?.level || "Unknown")}</td>

        `;

        row.addEventListener("click", () => {

            document
                .querySelectorAll(".request-row")
                .forEach(r => r.classList.remove("table-primary"));

            row.classList.add("table-primary");

            showRequestDetails(request);

        });

        tableBody.appendChild(row);

    });

}

/*
===========================================
Search
===========================================
*/

function setupSearch() {

    const searchBox =
        document.getElementById("requestSearch");

    if (!searchBox)
        return;

    searchBox.oninput = function () {

        const query =
            this.value
                .toLowerCase()
                .trim();

        if (!query) {

            renderRequestTable(allRequests);

            return;

        }

        const filtered = allRequests.filter(request => {

            return (

                (request.host || "")
                    .toLowerCase()
                    .includes(query)

                ||

                (request.path || "")
                    .toLowerCase()
                    .includes(query)

                ||

                (request.method || "")
                    .toLowerCase()
                    .includes(query)

                ||

                String(request.status_code || "")
                    .includes(query)

            );

        });

        renderRequestTable(filtered);

    };

}

/*
===========================================
Clear Dashboard
===========================================
*/

function clearDashboard() {

    allRequests = [];

    //---------------------------------------
    // Reset File Input
    //---------------------------------------

    const fileInput =
        document.getElementById("harFile");

    if (fileInput) {

        fileInput.value = "";

    }

    //---------------------------------------
    // Hide Dashboard
    //---------------------------------------

    const analysisSection =
        document.getElementById("analysisSection");

    if (analysisSection) {

        analysisSection.classList.add("d-none");

    }

    //---------------------------------------
    // Disable Clear Button
    //---------------------------------------

    const clearButton =
        document.getElementById("clearBtn");

    if (clearButton) {

        clearButton.disabled = true;

    }

    //---------------------------------------
    // Reset Summary Cards
    //---------------------------------------

    document.getElementById("totalRequests").textContent = "0";
    document.getElementById("lowRisk").textContent = "0";
    document.getElementById("mediumRisk").textContent = "0";
    document.getElementById("highRisk").textContent = "0";
    document.getElementById("criticalRisk").textContent = "0";

    //---------------------------------------
    // Reset Executive Summary
    //---------------------------------------

    document.getElementById("harSummary").innerHTML = "";

    //---------------------------------------
    // Reset Table
    //---------------------------------------

    document.getElementById("requestsTable").innerHTML = "";

    //---------------------------------------
    // Reset Search
    //---------------------------------------

    const searchBox =
        document.getElementById("requestSearch");

    if (searchBox) {

        searchBox.value = "";

    }

    //---------------------------------------
    // Reset 5W1H
    //---------------------------------------

    document.getElementById("whatText").textContent = "-";
    document.getElementById("whoText").textContent = "-";
    document.getElementById("whyText").textContent = "-";
    document.getElementById("whereText").textContent = "-";
    document.getElementById("howText").textContent = "-";

    //---------------------------------------
    // Reset AI Request Summary
    //---------------------------------------

    document.getElementById("aiSummary").innerHTML =
        "Select a request to generate an AI explanation.";

    //---------------------------------------
    // Reset Findings
    //---------------------------------------

    document.getElementById("securityFindings").innerHTML = "";

    //---------------------------------------
    // Reset Recommendations
    //---------------------------------------

    document.getElementById("recommendations").innerHTML = "";

}

/*
===========================================
Helpers
===========================================
*/

function truncate(text, maxLength) {

    if (!text)
        return "-";

    if (text.length <= maxLength)
        return text;

    return text.substring(0, maxLength - 3) + "...";

}