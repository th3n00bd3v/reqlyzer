const analyzeButton =
    document.getElementById("analyzeBtn");

const clearButton =
    document.getElementById("clearBtn");

const fileInput =
    document.getElementById("harFile");

const spinner =
    document.getElementById("loadingSpinner");

// Initial button state

analyzeButton.disabled = true;
clearButton.disabled = true;

// Enable Analyze button after selecting a HAR

fileInput.addEventListener("change", () => {

    analyzeButton.disabled =
        fileInput.files.length === 0;

});

// Analyze HAR

analyzeButton.addEventListener("click", async () => {

    const file = fileInput.files[0];

    if (!file) {

        alert("Please select a HAR file.");

        return;

    }

    spinner.classList.remove("d-none");

    analyzeButton.disabled = true;
    clearButton.disabled = true;

    try {

        const result =
            await uploadHAR(file);

        console.log(result);

        renderDashboard(result);

    }

    catch (error) {

        console.error(error);

        showError(error.message);

    }

    finally {

        spinner.classList.add("d-none");

        analyzeButton.disabled = false;
        clearButton.disabled = false;

    }

});

// Clear dashboard

clearButton.addEventListener("click", () => {

    clearDashboard();

    analyzeButton.disabled = true;
    clearButton.disabled = true;

});