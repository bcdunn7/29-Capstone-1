// Get canvas/chart element
let ctx = document.getElementById('chartjs-simulator').getContext('2d');
    
// set data (from Jinja template 'simulator.html' provided from flask app.py)
let data = {
    labels: race_labels,
    datasets: datasets
}

// set options
let options = {}

// Initialize the actual chart
let simulatorChart = new Chart(ctx, {
    type: 'line',
    data: data
});