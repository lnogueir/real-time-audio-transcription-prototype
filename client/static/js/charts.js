
console.log('hello world')

var ctx = document.getElementById('chart1').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',
    // The data for our dataset
    // let birthday = new Date('December 17, 1995 03:24:00')
    data: {
        yLabels: ["Joy", "Eager", "Neutral", "Sad", "Serious"],
        labels: [
            '00:00',
            '00:06',
            '00:12',
            '00:18',
            '00:24',
            '00:30',
        ],
        datasets: [{
            // steppedLine: true,
            label: 'Lucas',
            fill: false,
            backgroundColor: 'rgba(255, 99, 132, 0.3)',
            borderColor: 'rgba(255, 99, 132, 0.5)',
            data: ['Joy', 'Eager', 'Neutral', 'Neutral', 'Serious', 'Serious']
        },
        {
            // steppedLine: true,
            label: 'Jawad',
            fill: false,
            backgroundColor: 'rgba(145, 255, 53, .3)',
            borderColor: 'rgba(145, 255, 53, .5)',
            data: ['Neutral', 'Neutral', 'Eager', 'Eager', 'Serious', 'Serious']
        },
        {
            // steppedLine: true,
            label: 'Muller',
            fill: false,
            backgroundColor: 'rgba(77, 171, 245, 0.3)',
            borderColor: 'rgba(77, 171, 245, 0.5)',
            data: ['Eager', 'Sad', 'Serious', 'Serious', 'Sad', 'Neutral']
        },
        {
            // steppedLine: true,
            label: 'Lagan',
            fill: false,
            backgroundColor: 'rgba(131, 75, 255, 0.3)',
            borderColor: 'rgba(131, 75, 255, 0.5)',
            data: ['Neutral', 'Neutral', 'Serious', 'Neutral', 'Joy', 'Joy']
        }
        ]
    },
    // Configuration options go here
    options: {
        title: {
            display: true,
            fontSize: 14,
            text: 'Participats expressions over the meeting',
        },
        scales:{
            xAxes: [{
                display: true,
                scaleLabel: {
                  display: true,
                  labelString: 'Time elapsed'
                }
            }],
            yAxes: [{
                type: 'category',
                position: 'left',
                display: true,
                scaleLabel: {
                  display: true,
                  labelString: 'Participants Emotions'
                },
                ticks: {
                  reverse: true
                },
            }],
        }
    }
});