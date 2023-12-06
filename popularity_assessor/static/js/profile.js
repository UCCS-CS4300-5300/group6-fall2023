$(document).ready(async function () {
    console.log('Profile.js is working');

    const ctx = document.getElementById('metricsChart');

    // Initial empty or placeholder data
    const initialData = {
        labels: [],
        datasets: [
            {
                label: 'Views',
                data: [],
                fill: true,
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, .4)',
                tension: 0.1
            },
            {
                label: 'Followers',
                data: [],
                fill: true,
                borderColor: 'rgb(233, 30, 99)',
                backgroundColor: 'rgba(233, 30, 99, .4)',
                tension: 0.1
            }
        ]
    };

    const config = {
        type: 'line',
        data: initialData,
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Weekly Gain/Loss',
                    font: {
                        size: 30,
                        style: 'italic'
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    };

    // Create a chart instance with the initial data
    const chart = new Chart(ctx, config);

    async function fetchDataAndRenderChart() {
        const resp = await fetch('/popularity_assessor/timed_metrics/');
        const body = await resp.json();
        const dates = JSON.parse(document.getElementById('dates').textContent);
        const views = body.views;
        const followers = body.follows;

        // Update the chart with actual data
        chart.data.labels = dates;
        chart.data.datasets[0].data = views;
        chart.data.datasets[1].data = followers;
        console.log(views);
        console.log(followers);
        // Update the chart options if needed
        // chart.options = updatedOptions;

        // Update the chart
        chart.update();
    }

    // Call the function to fetch data and render the chart
    await fetchDataAndRenderChart();
});
