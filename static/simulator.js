// **********************************************
// Navigation Logic

$('#open-simulator-btn').on('click', function() {
    $('#overview').addClass('d-none');
    $('#chart-div').removeClass('d-none');
    $('#replay-season-btn').removeClass('d-none');
    initializeChart();
})


// **********************************************
// Replay Season and Blurb Logic

// raceNo of current race
let raceNo = 1;


// get barebones initial dataset
function getInitialDataset(datasets) {
    for (dataset of datasets) {
        dataset['data'] = [0];
    };
    return datasets;
}


// function to clear out chart of all data
function removeChartData(chart, initialDataset) {
    chart.data.labels = [""];
    chart.data.datasets = initialDataset;

    chart.update();
}


// Get data array for each driver
// this is for adding data, 1 race at a time
function separateAndStoreData(raceDatasets) {
    let storedData = {}
    for (let i=0; i < raceDatasets.length; i++) {
        storedData[i] = raceDatasets[i].data
    }
    return storedData
}


// add next data to chart
function nextData(raceNo, separateData, raceLabels, chart) {
    let chartData = chart.data;
    chartData.labels.push(raceLabels[raceNo]);
    for (let i = 0; i < chartData.datasets.length; i++) {
        chartData.datasets[i].data.push(separateData[i][raceNo])
    }
    chart.update('active');
}


// show a blurb if available
function showBlurbIfAvail(raceNo, raceLabels) {
    if (raceLabels[raceNo-1] in blurbs) {
        $('#blurb-p').text(blurbs[raceLabels[raceNo-1]]);
        $('#blurb-div').removeClass('d-none')
    }
    else {
        $('#blurb-p').text('')
    }
}


// initialize so that we have access in next race button function as well
let separateData;


// Begin Replay Mode
$('#replay-season-btn').on('click', function() {
    raceNo = 1;

    // remove data from chart
    let initialDataset = getInitialDataset(manipDatasets);
    removeChartData(simulatorChart, initialDataset);
    
    // get data ready to be added
    separateData = separateAndStoreData(raceDatasets);

    // add data and possible blurb
    nextData(raceNo, separateData, raceLabels, simulatorChart);
    raceNo++;
    showBlurbIfAvail(raceNo, raceLabels);

    // show replay manipulation buttons
    $('#replay-btns-div').removeClass('d-none')
})


// Next Race (replay mode)
$('#next-race-btn').on('click', function() {
    if (raceNo < raceLabels.length) {
        nextData(raceNo, separateData, raceLabels, simulatorChart);
        raceNo++;
        showBlurbIfAvail(raceNo, raceLabels);
        if (raceNo === raceLabels.length) {
            $('#restart-replay-btn').removeClass('d-none');
            $('#next-race-btn').addClass('d-none');
        }
    }
}) 


// Restart replay
$('#restart-replay-btn').on('click', function() {
    //reset race number
    raceNo = 1;

    // remove data from chart
    let initialDataset = getInitialDataset(manipDatasets);
    removeChartData(simulatorChart, initialDataset);

    // add data and possible blurb
    nextData(raceNo, separateData, raceLabels, simulatorChart);
    raceNo++;
    showBlurbIfAvail(raceNo, raceLabels);

    // show replay manipulation buttons
    $('#next-race-btn').removeClass('d-none');
    $('#restart-replay-btn').addClass('d-none');

})


// **********************************************
// Line Chart (chart.js)

// Get canvas/chart element
let ctx = document.getElementById('chartjs-simulator').getContext('2d');
    
// set data (from Jinja template 'simulator.html' provided from flask app.py)
let data = {
    labels: raceLabels,
    datasets: raceDatasets
}

// set options
let options = {
    title:{
        display:true,
        text:"World Drivers' Championship"
    }
}

// initialize delayed for animation options below
let delayed;
// Initialize the actual chart
let simulatorChart;
function initializeChart() {
    simulatorChart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: false
                }
            },
            animation: {
                onComplete: () => {
                  delayed = true;
                },
                delay: (context) => {
                  let delay = 0;
                  if (context.type === 'data' && context.mode === 'default' && !delayed) {
                    delay = context.dataIndex * 200 + context.datasetIndex * 100;
                  }
                  return delay;
                },
            },
            elements: {
                point: {
                    radius: 2.5
                },
                line: {
                    tension: 0.2,
                    borderWidth: 1.5
                }
            }
          },
    });
}
