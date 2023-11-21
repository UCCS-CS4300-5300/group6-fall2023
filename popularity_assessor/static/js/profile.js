$(document).ready(function () {
    const ctx = document.getElementById('metricsChart');

    var dates = JSON.parse(document.getElementById('dates').textContent);
    var likes = JSON.parse(document.getElementById('likes').textContent);
    var followers = JSON.parse(document.getElementById('followers').textContent);

    const data = {
        labels: dates,
        datasets: [
            {
                label: 'Likes',
                data: likes,
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
                text: 'Weekly Gain/Loss'
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