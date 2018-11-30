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

// if there is -1 in labels, this function will create new label > 0 and remove -1
function validLabels(labels, lastLabel){
    let newLabel = [];
    let index = labels.indexOf(-1);
    if (index > -1) {
        for (let i=0; i<labels.length; i++){
            if(i !== index){
                newLabel.push(labels[i])
            }
        }
        newLabel.push(lastLabel + 1);
        return newLabel
    }
    return labels
}

function post(method, dict) {
    $.post(method, dict)
        .done(function (full_data) {
            let labelsSet = full_data['labels'];
            let lastLabel = Math.max.apply(null, labelsSet);
            let validatedLabels = validLabels(labelsSet, lastLabel);
            let data = full_data['data'];
            let frames = [];
            let minx;
            let maxx;
            let miny;
            let maxy;
            let layout = {};
            let d0 =[];
            let sliderSteps = [];
            $.each(data, function (key, value) {
                $.each(value, function (i, val) {
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
                });

                let X = {};
                let Y = {};
                $.each(value, function (i, val) {

                    if (val.cluster == -1) {
                        let new_key = lastLabel + 1
                        if (X[new_key] === undefined) {
                            X[new_key] = [];
                            Y[new_key] = [];
                        }
                        X[new_key] = [];
                        Y[new_key] = [];
                        X[new_key].push(val.coordinates.x);
                        Y[new_key].push(val.coordinates.y);
                    }
                    else {
                        if (X[val.cluster] === undefined) {
                            X[val.cluster] = [];
                            Y[val.cluster] = [];
                        }
                        X[val.cluster].push(val.coordinates.x);
                        Y[val.cluster].push(val.coordinates.y);
                    }

                });
                let d = [];
                $.each(validatedLabels, function (i, val) {
                    let name;
                    if (labelsSet.includes(-1.0) && val === lastLabel + 1){
                        name = 'Noise'
                    }
                    else {
                        name = 'Cluster ' + i
                    }
                    if(X[i] === undefined){
                        d.push(create_cluster([], [], name, validatedLabels));
                        return true;
                    }
                    d.push(create_cluster(X[i], Y[i], name, validatedLabels));
                });


                sliderSteps.push({
                    method: 'animate',
                    label: key,
                    args: [[key], {
                        mode: 'immediate',
                        transition: {duration: 0},
                        frame: {duration: 300, redraw: false},
                    }]
                });
                layout = {
                    xaxis: {
                        range: [minx - 0.5, maxx + 0.5]
                    },
                    yaxis: {
                        range: [miny - 0.5, maxy + 0.5]
                    },
                    title: 'Cluster Visualization',
                    hovermode: 'closest',
                    updatemenus: [{
                        x: 0,
                        y: 0,
                        yanchor: 'top',
                        xanchor: 'left',
                        showactive: false,
                        direction: 'left',
                        type: 'buttons',
                        pad: {t: 87, r: 10},
                        buttons: [
                            {
                                method: 'animate',
                                args: [null, {
                                    mode: 'immediate',
                                    fromcurrent: true,
                                    transition: {duration: 0},
                                    frame: {duration: 500, redraw: false}
                                }],
                                label: 'Play'
                            }, {
                          method: 'animate',
                          args: [[null], {
                              mode: 'immediate',
                              transition: {duration: 0},
                              frame: {duration: 0, redraw: false}
                          }],
                          label: 'Pause'
                        }]
                    }],
                        sliders: [{
                              pad: {l: 130, t: 55},
                              currentvalue: {
                                visible: true,
                                prefix: 'Iteration:',
                                xanchor: 'right',
                                font: {size: 20, color: '#666'}
                              },
                              steps: sliderSteps
                            }]
                };

            frames.push({
                'name': key-1,
                'data': d
            });

            if(key === '1'){
                d0=d;
            }
            });

        Plotly.newPlot('myDiv', {
            data: d0,
            layout: layout,
            frames: frames
        })
    });
}


function create_cluster(x, y, name, validatedLabels) {
    if (x.length === 0){
        x = [null];
        y = [null];
    }
    return {
        visible: true,
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
    let input = [];
    let i = 0;
    let t;
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

                console.log(file.name.slice(0,-3))
        }
    })


