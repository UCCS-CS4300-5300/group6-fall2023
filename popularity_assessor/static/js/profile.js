$(document).ready(function () {
    const ctx = document.getElementById('metricsChart');

    var dates = JSON.parse(document.getElementById('dates').textContent);
    var likes = JSON.parse(document.getElementById('likes').textContent);

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
                data: [76, 10, 43, 30, 100, 25, 40],
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