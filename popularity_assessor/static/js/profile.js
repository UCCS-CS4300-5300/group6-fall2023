$(document).ready(async function () {

    console.log('Profile.js is working');


    const ctx = document.getElementById('metricsChart');

    // var data = await fetch('/popularity_assessor/timed_metrics/');
    // console.log(data);

    const resp = await fetch('/popularity_assessor/timed_metrics/')
    const body = await resp.json()
    var dates = JSON.parse(document.getElementById('dates').textContent);
    var views = body.views
    var followers = body.followers

    const data = {
        labels: dates,
        datasets: [
            {
                label: 'Views',
                data: views,
                fill: true,
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, .4)',
                tension: 0.1
            },
            {
                label: 'Followers',
                data: followers,
                fill: true,
                borderColor: 'rgb(233, 30, 99)',
                backgroundColor: 'rgba(233, 30, 99, .4)',
                tension: 0.1
            }
        ]
    };

    const config = {
        type: 'line',
        data: data,
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
              }
          }
      }
    };

    new Chart(ctx, config);
});