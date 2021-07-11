// **********************************************
// Open Simulator Logic

$('#open-simulator-btn').on('click', function() {
    $('#overview').addClass('d-none');
    $('#chart-div').removeClass('d-none');
    $('#modes-div').removeClass('d-none');
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
    chart.update();
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
// Sandbox Logic

// On 'sandbox' create manipulatable toggles
$('#sandbox-btn').on('click', function() {

    for (race_id of Object.keys(change_texts)) {
        $('#sandbox-toggles-div').append(`<div class='form-check form-switch'><input id=${race_id} data-round='${change_texts[race_id]['round']}' class='form-check-input' type='checkbox' id='flexSwitchCheckDefault'><label class='form-check-label' for='${race_id}'>${change_texts[race_id]['abbr']}: ${change_texts[race_id]['change_text']}</label></div>`)
    }

    $('#sandbox-toggles-div').removeClass('d-none');
    $('#save-btn-div').removeClass('d-none');
})


// function to manipulate race data based on toggle
function manipulate_race_data(race_id, round, chart) {
    let newDatasets = chart.data.datasets;
    // find all race changes for this race
    let race_changes = [];
    for (i in changes) {
        if (changes[i]['race'] === race_id) {
            race_changes.push(changes[i])
        }
    }
    // change the data
    for (i in race_changes) {
        for (j in newDatasets) {
            if (race_changes[i]['driver'] === newDatasets[j]['label']) {
                let points = newDatasets[j]['data'];

                // need to find difference between original score and new score
                let new_pnt = race_changes[i]['new_points'];
                let old_pnt = (points[round]-points[round-1]);
                let diff = new_pnt-old_pnt;

                // update points based on difference
                let new_points = points.map(function(pnt, i){
                    if (i >= round) {
                        return (pnt+diff);
                    }
                    else return pnt;
                })

                chart.data.datasets[j].data = new_points;
            }
        }
    }
    chart.update();
}

// function to undo manipulation on 'uncheck'
function undo_race_data_manipulation(race_id, round, chart) {
    //current datasets
    let currDatasets = chart.data.datasets;
    // find all race changes for this race
    let race_changes = [];
    for (i in changes) {
        if (changes[i]['race'] === parseInt(race_id)) {
            race_changes.push(changes[i])
        }
    }
    // change the data back
    for (i in race_changes) {
        for (j in currDatasets) {
            if (race_changes[i]['driver'] === refDatasets[j]['label']) {
                let points = currDatasets[j]['data'];

                // find original value in order to find difference
                let orig_points = refDatasets[j]['data'];

                let orig_pnt = (orig_points[round]-orig_points[round-1]);
                let adj_pnt = race_changes[i]['new_points'];
                let diff = orig_pnt-adj_pnt;

                // update data
                let new_points = points.map(function(pnt, i) {
                    if (i >= round) {
                        return (pnt+diff)
                    }
                    else return pnt;
                })

                chart.data.datasets[j].data = new_points;
            }
        }
    }
    chart.update()
}

// event listener for toggle changes
$('#sandbox-toggles-div').on('change', '.form-check-input', function() {
    let race_id = parseInt(this.id);
    let round = parseInt(this.dataset.round);
    if(this.checked) {
        manipulate_race_data(race_id, round, simulatorChart)
    }
    if(!this.checked) {
        undo_race_data_manipulation(race_id, round, simulatorChart)
    }
})


$('#save-btn').on('click', function(){
    //save to user account here.
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
