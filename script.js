// Fetch the aggregated flights data
fetch('aggregated_flights.json')
    .then(response => response.json())
    .then(data => {
        // Extracting hours, crew counts, and pilot counts
        const hours = data.map(item => item.Zeit);
        const crewCounts = data.map(item => item.Crew);
        const pilotCounts = data.map(item => item.Pilots);
        const passengerCounts = data.map(item => item.Passagiere);

        // Calculate totals
        const totalCrew = crewCounts.reduce((sum, count) => sum + count, 0);
        const totalPilots = pilotCounts.reduce((sum, count) => sum + count, 0);

        document.getElementById("totalCrew").innerHTML = "Total Crew: " + totalCrew;
        document.getElementById("totalPilots").innerHTML = "Total Pilots:" + totalPilots;

        // Creating the bar chart for crew and pilots
        const ctx = document.getElementById('crewChart').getContext('2d');
        const crewChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: hours,
                datasets: [
                    {
                        label: 'Anzahl Crew',
                        data: crewCounts,
                        backgroundColor: 'skyblue',
                        borderColor: 'blue',
                        borderWidth: 1,
                    },
                    {
                        label: 'Anzahl Piloten',
                        data: pilotCounts,
                        backgroundColor: 'lightgreen',
                        borderColor: 'green',
                        borderWidth: 1,
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                const index = context.dataIndex;
                                const label = context.dataset.label;
                                const value = context.raw;
                                return `${label}: ${value}`;
                            }
                        }
                    },
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Uhrzeit',
                            color: '#333',
                            font: {
                                size: 14
                            }
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Anzahl Personal',
                            color: '#333',
                            font: {
                                size: 14
                            }
                        },
                        beginAtZero: true,
                        ticks: {
                            stepSize: 10
                        }
                    }
                }
            }
        });

        // Creating the line chart for passengers
        const ctxLine = document.getElementById('passengerChart').getContext('2d');
        const passengerChart = new Chart(ctxLine, {
            type: 'line',
            data: {
                labels: hours,
                datasets: [{
                    label: 'Anzahl der Passagiere',
                    data: passengerCounts,
                    backgroundColor: 'lightcoral',
                    borderColor: 'red',
                    borderWidth: 2,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                const index = context.dataIndex;
                                const label = context.dataset.label;
                                const value = context.raw;
                                return `${label}: ${value}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Uhrzeit',
                            color: '#333',
                            font: {
                                size: 14
                            }
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Anzahl der Passagiere',
                            color: '#333',
                            font: {
                                size: 14
                            }
                        },
                        beginAtZero: true,
                        ticks: {
                            stepSize: 100
                        }
                    }
                }
            }
        });
    })
    .catch(error => {
        console.error('Error fetching the JSON data:', error);
    });

// Fetch the aggregated flights data by hour and flugzeugtyp
fetch('most_used_flights_per_hour.json')
    .then(response => response.json())
    .then(data => {
        // Extracting hours, flugzeugtyp labels, and counts
        const hours = data.map(item => item.Zeit);
        const flugzeugtypLabels = data.map(item => item.Flugzeugtyp);
        const counts = data.map(item => item.Count);

        // Calculate total number of planes
        const totalPlanes = counts.reduce((sum, count) => sum + count, 0);

        // Creating the bar chart
        const ctxBar = document.getElementById('flugzeugtypChart').getContext('2d');
        const flugzeugtypChart = new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: hours,
                datasets: [{
                    label: 'Meist genutztes Flugzeug pro Stunde',
                    data: counts,
                    backgroundColor: 'red',
                    borderColor: 'white',
                    borderWidth: 1,
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                const index = context.dataIndex;
                                const flugzeugtyp = flugzeugtypLabels[index];
                                const count = context.raw;
                                return `${flugzeugtyp}: ${count}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Uhrzeit',
                            color: '#333',
                            font: {
                                size: 14
                            }
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Anzahl der Flüge',
                            color: '#335',
                            font: {
                                size: 14
                            }
                        },
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    })
    .catch(error => {
        console.error('Error fetching the JSON data:', error);
    });

// Fetch the aggregated staff data by Flugzeugtyp
fetch('aggregated_staff_by_flugzeugtyp.json')
    .then(response => response.json())
    .then(data => {
        // Extracting flugzeugtyp labels and staff counts
        const flugzeugtypLabels = data.map(item => item.Flugzeugtyp);
        const staffCounts = data.map(item => item.Staff);

        // Creating the pie chart with moderately soft colors
        const ctxPie = document.getElementById('flugzeugtypPieChart').getContext('2d');
        const flugzeugtypPieChart = new Chart(ctxPie, {
            type: 'pie',
            data: {
                labels: flugzeugtypLabels,
                datasets: [{
                    label: 'Anzahl der Staff nach Flugzeugtyp',
                    data: staffCounts,
                    backgroundColor: [
                        'lightcoral', 'skyblue', 'lightgoldenrodyellow', 'mediumaquamarine', 'orchid', 'lightsalmon', 'lightpink'
                    ],
                    borderColor: [
                        'indianred', 'steelblue', 'gold', 'seagreen', 'mediumorchid', 'salmon', 'palevioletred'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                const label = context.label || '';
                                const value = context.raw;
                                return `${label}: ${value}`;
                            }
                        }
                    }
                }
            }
        });
    })
    .catch(error => {
        console.error('Error fetching the JSON data:', error);
    });

// Function to open the JSON modal
const openModalBtn = document.getElementById('openModalBtn');
const modal = document.getElementById('jsonModal');
const span = document.getElementsByClassName('close')[0];
const jsonDataElement = document.getElementById('jsonData');

openModalBtn.onclick = function () {
    fetch('updated_flights.json')
        .then(response => response.json())
        .then(data => {
            jsonDataElement.textContent = JSON.stringify(data, null, 2);
            modal.style.display = 'block';
        })
        .catch(error => {
            console.error('Error fetching the JSON data:', error);
        });
};

// Close the modal when the user clicks on <span> (x)
span.onclick = function () {
    modal.style.display = 'none';
};

// Close the modal when the user clicks anywhere outside of the modal
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};
