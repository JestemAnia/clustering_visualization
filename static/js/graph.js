function post2() {
    $.post("kmeans/", {})
        .done(function (data) {
            let labels = [];
            let set_of_clusters = [];
            $.each(data, function (i, val) {
                labels.push(val.cluster);
                if ($.inArray(val, set_of_clusters) === -1) set_of_clusters.push(val.cluster);
            });
            let X = [];
            let Y = [];
            $.each(data, function (i, val) {
                if (X[val.cluster] === undefined) {
                    X[val.cluster] = [];
                    Y[val.cluster] = [];
                }
                X[val.cluster].push(val.coordinates.x);
                Y[val.cluster].push(val.coordinates.y);
            });
            let d = [];
            $.each(X, function (i, val) {
                d.push(create_cluster(X[i], Y[i], 'Cluster ' + i));
            });
            let layout = {
                xaxis: {
                    range: [0.75, 5.25]
                },
                yaxis: {
                    range: [0, 8]
                },
                title: 'Data Labels Hover'
            };
            Plotly.newPlot('myDiv', d, layout, {displayModeBar: false});
        });
}


function create_cluster(x, y, name) {
    return {
        x: x,
        y: y,
        mode: 'markers',
        type: 'scatter',
        name: name,
        marker: {size: 12}
    }
}


post2();
