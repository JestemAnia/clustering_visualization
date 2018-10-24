const kmeans_button = $('#kmeans');
kmeans_button.click(function() {
    preferences('kmeans')
});


function preferences(method) {
    var parameters = $('#parameters')[0];
    switch (method) {
        case 'kmeans':

            var input = document.createElement("input"); //input element, text
            input.setAttribute('type',"number");
            input.setAttribute('name',"n_cluster");
            input.setAttribute('defaultValue',"2");

            var submit = document.createElement("input"); //input element, Submit button
            submit.setAttribute('type',"submit");
            submit.setAttribute('value',"Submit");


            submit.onclick = function() {
                let n_cluster = input.value;
                post(method + '/', n_cluster)
            };

            parameters.appendChild(input);
            parameters.appendChild(submit);
            document.getElementsByTagName('body')[0].appendChild(parameters);


            break;
        case 'dbscan':
            break;
    }


}




//  evaluate algorithm
function post(method, clusters) {
    $.post(method, {n_cluster: clusters})
        .done(function (data) {
            let labels = [];
            let set_of_clusters = [];
            let minx;
            let maxx;
            let miny;
            let maxy;
            $.each(data, function (i, val) {
                if (i === 0) {
                    minx = val.coordinates.x;
                    maxx = val.coordinates.x;
                    miny = val.coordinates.y;
                    maxy = val.coordinates.y;
                }
                else {
                    if (val.coordinates.x < minx){
                        minx = val.coordinates.x
                    }
                    if (val.coordinates.x > maxx){
                        maxx = val.coordinates.x
                    }
                    if (val.coordinates.y < miny){
                        miny = val.coordinates.y
                    }
                    if (val.coordinates.y > maxy){
                        maxy = val.coordinates.y
                    }
                }
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
                    range: [minx - 0.5, maxx + 0.5]
                },
                yaxis: {
                    range: [miny - 0.5, maxy + 0.5]
                },
                title: 'Cluster Visualization'
            };
            Plotly.newPlot('myDiv', d, layout, {displayModeBar: false} );
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


