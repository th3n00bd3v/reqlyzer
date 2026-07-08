const analyzeButton = document.getElementById("analyzeBtn");
const fileInput = document.getElementById("harFile");
const spinner = document.getElementById("loadingSpinner");


analyzeButton.addEventListener("click", async () => {

    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a HAR file.");
        return;
    }

    spinner.classList.remove("d-none");
    analyzeButton.disabled = true;

    try {

        const result = await uploadHAR(file);

        console.log(result);

        renderDashboard(result);

    } catch (error) {

        console.error(error);

        alert(error.message);

    } finally {

        spinner.classList.add("d-none");

        analyzeButton.disabled = false;

    }

});