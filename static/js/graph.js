let buttons = [];

$.get('methods/').done(function(data){
    for(let i = 0; i < data.length; i++){
        buttons[i] = $('#'+data[i]);
        buttons[i].click(function(){
            preferences(data[i])
        })
    }
});


function preferences(method) {
    let params = {};
    $.get(method + '/parameters/')
        .done(function(data){
            params = data;
            createParametersDiv(params, method)
        });
}


function post(method, dict) {
    $.post(method, dict)
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

function createParametersDiv(params, method){
    let parametersDiv = $('#parameters')[0];
    console.log(parametersDiv)
    let input = [];
    let i = 0;
    let t;
    let br;
    for (let key in params)
    {
        input[i] = document.createElement("input");
        input[i].setAttribute('type',params[key]);
        input[i].setAttribute('name',key);
        t = document.createTextNode(key + ': ');
        parametersDiv.appendChild(t);
        parametersDiv.appendChild(input[i]);
        i = i + 1;
    }

    let submit = document.createElement("input"); //input element, Submit button
    submit.setAttribute('type',"submit");
    submit.setAttribute('value',"Submit");
    submit.onclick = function() {
        let method_dictionary = {};
        let i = 0;
        for(let key in params)
        {
            method_dictionary[key] = input[i].value;
            i = i + 1;
        }
        post(method + '/', method_dictionary)
    };

    parametersDiv.appendChild(submit);
}




formdata = new FormData();
$("#image_to_upload").on("change", function() {
        var file = this.files[0];
        if (formdata && file.name.endsWith('.py')) {
            $("#subimt_upload").prop('disabled', false);
            $("#subimt_upload").off().on("click", function(){
                formdata.append("file", file);
                $.ajax({
                    url: "upload/",
                    type: "POST",
                    data: formdata,
                    processData: false,
                    contentType: false,
                    success:function(){}
                });
            });

        }
    });