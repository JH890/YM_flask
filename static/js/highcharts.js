$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container',
            defaultSeriesType: 'spline'
//            events: {
//                load: requestData
//            }
        },
        title: {
            text: 'Live random data'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150,
            maxZoom: 20 * 1000
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Value',
                margin: 80
            }
        },
        series: [{
            name: 'Random data',
            data: []
        }]
    });
});

var chart;

setInterval(function(){
    $.ajax({
        url: '/live-data',
        success: function(point) {
            var series = chart.series[0],
                shift = series.data.length > 20; // shift if the series is
                                                 // longer than 20

            chart.series[0].addPoint(point, true, shift);

            var d = new Date();
            console.log(d.getMilliseconds());
        },
        cache: false
    })
}, 1000);

