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
    populateTable(simulatorChart);
}


function previousData(chart) {
    chart.data.labels.pop();
    for (let i=0; i < chart.data.datasets.length; i++) {
        chart.data.datasets[i].data.pop()
    }
    chart.update()
    populateTable(simulatorChart);
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
    initializeChart();
    
    raceNo = 1;

    $('#back-btn-form').removeClass('d-none');
    $('#overview').addClass('d-none');
    $('#chart-div').removeClass('d-none');
    $('#table-container').removeClass('d-none');

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


$('#prev-race-btn').on('click', function() {
    if (raceNo > 2) {
        previousData(simulatorChart);
        raceNo--;
        showBlurbIfAvail(raceNo, raceLabels);
        if (raceNo === raceLabels.length-1) {
            $('#restart-replay-btn').addClass('d-none');
            $('#next-race-btn').removeClass('d-none');
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

// On 'open simulator' create manipulatable toggles
$('#sandbox-btn').on('click', function() {

    initializeChart();

    $('#back-btn-form').removeClass('d-none');
    $('#overview').addClass('d-none');
    $('#chart-div').removeClass('d-none');
    $('#table-container').removeClass('d-none');

    // create toggles
    for (raceId of Object.keys(changeTexts)) {
        $('#sandbox-toggles-div').append(`<div class='form-check form-switch m-1'><input id=${raceId} data-round='${changeTexts[raceId]['round']}' class='form-check-input' type='checkbox' id='flexSwitchCheckDefault'><label class='form-check-label' for='${raceId}'><b>${changeTexts[raceId]['abbr']}</b>: ${changeTexts[raceId]['change_text']}</label></div>`)
    }

    // toggle changes that the user has previously saved
    for (i in userChanges) {
        let toggle = document.getElementById(`${userChanges[i]}`)
        toggle.checked = true;
        toggle.parentElement.classList.add('toggle-on');
        let raceId = parseInt(toggle.id);
        let round = parseInt(toggle.dataset.round);
        manipulateRaceData(raceId, round, simulatorChart)
    }

    $('#sandbox-toggles-div').removeClass('d-none');
    $('#save-btn-div').removeClass('d-none');

    // standings table
    populateTable(simulatorChart);
})


function populateTable(chart) {
    // find data to first sort before appending to table
    let chartDatasets = chart.data.datasets;

    let tableData = [];

    for (let i=0; i<chartDatasets.length; i++) {
        tableData.push([chartDatasets[i].label, chartDatasets[i].data.slice(-1)[0], chartDatasets[i].backgroundColor])
    }

    // sort tableData

    tableData.sort(function(a,b) {
        return (b[1]-a[1]);
    })

    // append sorted data to table
    let body = $('#table-body');
    body.empty()

    for (let i=0; i<tableData.length; i++) {
        if (i === 0) {
            body.append(`<tr><th><i class="fas fa-medal"></i></th><td><i class="fas fa-user-circle" style="color:${tableData[i][2]}"></i> ${tableData[i][0]}</td><td>${tableData[i][1]}</td></tr>`)
        }
        else {
            body.append(`<tr><th>${i+1}</i></th><td><i class="fas fa-user-circle" style="color:${tableData[i][2]}"></i> ${tableData[i][0]}</td><td>${tableData[i][1]}</td></tr>`)
        }

    }

    body.addClass('tbody-style');
}


// function to manipulate race data based on toggle
function manipulateRaceData(raceId, round, chart) {
    let newDatasets = chart.data.datasets;
    // find all race changes for this race
    let raceChanges = [];
    for (i in changes) {
        if (changes[i]['race'] === raceId) {
            raceChanges.push(changes[i])
        }
    }
    // change the data
    for (i in raceChanges) {
        for (j in newDatasets) {
            if (raceChanges[i]['driver'] === newDatasets[j]['label']) {
                let points = newDatasets[j]['data'];

                // need to find difference between original score and new score
                let newPnt = raceChanges[i]['new_points'];
                let oldPnt = (points[round]-points[round-1]);
                let diff = newPnt-oldPnt;

                // update points based on difference
                let newPoints = points.map(function(pnt, i){
                    if (i >= round) {
                        return (pnt+diff);
                    }
                    else return pnt;
                })

                chart.data.datasets[j].data = newPoints;
            }
        }
    }
    chart.update();
    populateTable(simulatorChart);
}

// function to undo manipulation on 'uncheck'
function undoRaceDataManipulation(raceId, round, chart) {
    //current datasets
    let currDatasets = chart.data.datasets;
    // find all race changes for this race
    let raceChanges = [];
    for (i in changes) {
        if (changes[i]['race'] === parseInt(raceId)) {
            raceChanges.push(changes[i])
        }
    }
    // change the data back
    for (i in raceChanges) {
        for (j in currDatasets) {
            if (raceChanges[i]['driver'] === refDatasets[j]['label']) {
                let points = currDatasets[j]['data'];

                // find original value in order to find difference
                let origPoints = refDatasets[j]['data'];

                let origPnt = (origPoints[round]-origPoints[round-1]);
                let adjPnt = raceChanges[i]['new_points'];
                let diff = origPnt-adjPnt;

                // update data
                let newPoints = points.map(function(pnt, i) {
                    if (i >= round) {
                        return (pnt+diff)
                    }
                    else return pnt;
                })

                chart.data.datasets[j].data = newPoints;
            }
        }
    }
    chart.update()
    populateTable(simulatorChart);
}

// event listener for toggle changes
$('#sandbox-toggles-div').on('change', '.form-check-input', function() {
    let raceId = parseInt(this.id);
    let round = parseInt(this.dataset.round);
    if(this.checked) {
        manipulateRaceData(raceId, round, simulatorChart);
        this.parentElement.classList.add('toggle-on');
    }
    if(!this.checked) {
        undoRaceDataManipulation(raceId, round, simulatorChart);
        this.parentElement.classList.remove('toggle-on');
    }
})


$('#save-btn').on('click', function(){
    // get race ids for toggled races
    let toggles = Array.from($('.form-check-input'))
    
    let raceIds = toggles.reduce(function(ids, tog) {
        if (tog.checked) {
            ids.push(tog.id)
        }
        return ids
    }, [])

    // get season year
    let heading = document.querySelector('#season-heading');
    let year = heading.dataset.year;

    // need to run even if empty, because untoggles needs to be marked too
    postUserChanges(raceIds, year);

    changesSaved()
})

async function postUserChanges(raceIds, year) {
    let resp = await axios.post('/simulator/save', {raceIds:raceIds, year:year})
}


function changesSaved(){
    $('#changes-saved').removeClass('d-none');
    $('#changes-saved').delay(1250).fadeTo(500, 0, function(){
        this.classList.add('d-none');
        this.setAttribute('style', "")
    });
}

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
