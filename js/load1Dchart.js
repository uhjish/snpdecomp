
function load1Dchart(atitle, subtitle, seriesid, categories, values, xaxs, yaxs) {
    var chart = new Highcharts.Chart({
        chart: {
            renderTo: 'container',
            defaultSeriesType: 'scatter'
        },
        title: {
            text: atitle
        },
        subtitle: {
            text: subtitle
        },
        xAxis: {
            categories: categories,
            title: {
                text: xaxs
            }
        },
        yAxis: {
            title: {
                text: yaxs
            }
        },
        legend: {
            enabled: false
        },
        tooltip: {
            formatter: function() {
                    return '<b>'+ this.series.name +'</b><br/>'+
                    this.x +': '+ this.y ;
            }
        },
        plotOptions: {
            spline: {
                cursor: 'pointer',
                point: {
                    events: {
                        click: function() {
                            alert ('this.category: '+ this.category +'\nthis.y: '+ this.y);
                        }
                    }
                }
            }
        },
        series: [{
            name: seriesid,
            data: values
        }]
    });
}

