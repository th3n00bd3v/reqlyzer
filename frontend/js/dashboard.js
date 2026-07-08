let allRequests = [];

/*
===========================================
Dashboard Rendering
===========================================
*/

function renderDashboard(result) {

    allRequests = result.requests || [];

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

        switch (request.risk.level) {

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
                title="${request.path}">

                ${truncate(request.path, 45)}

            </td>

            <td>${request.status_code}</td>

            <td>${riskBadge(request.risk.level)}</td>

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
Helpers
===========================================
*/

function truncate(text, maxLength) {

    if (!text)
        return "";

    if (text.length <= maxLength)
        return text;

    return text.substring(0, maxLength) + "...";

}