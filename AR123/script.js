// Wait for the DOM to fully load before adding event listeners
document.addEventListener("DOMContentLoaded", function () {

    // Form handling for the recommendations form
    const recommendationsForm = document.getElementById("recommendations-form");
    if (recommendationsForm) {
        recommendationsForm.addEventListener("submit", function (event) {
            // Client-side validation
            const maxFuelInput = document.getElementById("max_fuel");
            const maxEmissionsInput = document.getElementById("max_emissions");

            let isValid = true;
            let errorMessage = "";

            // Validate max fuel
            if (maxFuelInput && maxFuelInput.value !== "") {
                const maxFuelValue = parseFloat(maxFuelInput.value);
                if (isNaN(maxFuelValue) || maxFuelValue <= 0) {
                    isValid = false;
                    errorMessage += "Please enter a valid positive number for Max Fuel.\n";
                }
            }

            // Validate max emissions
            if (maxEmissionsInput && maxEmissionsInput.value !== "") {
                const maxEmissionsValue = parseFloat(maxEmissionsInput.value);
                if (isNaN(maxEmissionsValue) || maxEmissionsValue <= 0) {
                    isValid = false;
                    errorMessage += "Please enter a valid positive number for Max Emissions.\n";
                }
            }

            // If validation fails, prevent form submission and display errors
            if (!isValid) {
                event.preventDefault();
                alert(errorMessage);
            }
        });
    }

    // Interactive chart switching
    const chartSwitchButtons = document.querySelectorAll(".chart-switch");
    chartSwitchButtons.forEach(button => {
        button.addEventListener("click", function () {
            const targetChart = this.dataset.target;
            const allCharts = document.querySelectorAll(".chart-container");

            // Hide all charts and show the selected one
            allCharts.forEach(chart => chart.style.display = "none");
            document.getElementById(targetChart).style.display = "block";
        });
    });

    // Add some interactivity for the summary page
    const refreshSummaryButton = document.getElementById("refresh-summary");
    if (refreshSummaryButton) {
        refreshSummaryButton.addEventListener("click", function () {
            alert("Summary data refreshed successfully!"); // Placeholder for future dynamic updates
        });
    }
});
