/*-- get data from HTML and parse this to dictionary --*/
var jsonFromHTML = document.getElementById("json").innerHTML;
var cleanJsonFromHTML1 = jsonFromHTML.replace(/"/g,'');
var cleanJsonFromHTML = cleanJsonFromHTML1.replace(/&#34;/g,'"');
// jsonDictionary is global variable which is used and overriding in many functions
var jsonDictionary = JSON.parse(cleanJsonFromHTML);


// set max file size
sessionStorage['file_size'] = jsonDictionary['file_size']


// makes button unavailable

$("#Submit").prop("disabled",false);
$("#Apply").prop("disabled",true);
$("#Train").prop("disabled",true);
$("#Save").prop("disabled",true);
$("#Reset").prop("disabled",true);
$("#Build").prop("disabled",true);
$("#attributes-block").addClass("disabledfilter");
$("#distrChart").addClass("disabledfilter");
$("#distr-block").addClass("disabledfilter");
$("#statInfoBlock").addClass("disabledfilter");
$("#dynamicChartBlock").addClass("disabledfilter");
$("#topTerm").addClass('disabledfilter');
$("#load").removeAttr("style").hide();


// unlock single mod and multiple mod for open source version
function lock_mode(single_mad, multiple_mod){
if(single_mad == true)
    $("#menu-single-descr-mode").removeClass('disabled');

if(multiple_mod == true)
    $("#menu-multiple-descr-mode").removeClass('disabled');
}
lock_mode(jsonDictionary['single_mod'], jsonDictionary['multiple_mod'])

/*-- put data from dictionary to HTML --*/
if('undefined'.localeCompare(jsonDictionary['username']) == 0){
    user.innerHTML = 'unknown user';
}
else{putUser()}
function putUser(){
    var user = document.getElementById('username');
        user.innerHTML = jsonDictionary['username'];
}


// create fields on GUI, mandatory_fields, special_fields, areas_fields
// and setting up this for any field_type_backend
function addField(parent_div, div_class, label_class,
                  inner_div_class, field_name, field_name_GUI,
                  field_class, field_tag, field_type, field_type_backend){
    // create div
    var i_div = document.createElement('div');
    i_div.className = div_class;
    // create inner div
    var i_inner_div = document.createElement('div');
    i_inner_div.className = inner_div_class;
    // create label
    var i_label = document.createElement('label');
    i_label.className = label_class;
    i_label.innerHTML = field_name_GUI
    // create field
    var i_field = document.createElement(field_tag);
    i_field.id = field_name
    i_field.name = field_name
    if(field_type_backend == 'categorical'){
        i_field.multiple="multiple"
        var newScript = document.createElement("script");
        newScript.async = false;
        // jquery doesn't work with # and id with spaces
        var inlineScript = document.createTextNode("document.addEventListener('DOMContentLoaded',"+ "function categorical(e){$(\"[id='"+field_name+"']\").select2({width:'100%'});}, false);");
        newScript.appendChild(inlineScript);
        var test = document.getElementById('loadDiv')
        test.appendChild(newScript)
    }
    if(field_type_backend == 'text'){
        i_field.type = field_type
        i_field.pattern = "[A-Z]{1,10}[\-][0-9]{1,10}"
        i_field.className = field_class[0]
        }
    if(field_type_backend == 'text2'){
        i_field.type = field_type
        i_field.className = field_class[0];
        }
    if(field_type_backend == 'text1'){
        i_field.type = field_type
        i_field.className = field_class[0];
    }
    if(field_type_backend == 'number'){
        i_field.className = field_class[1];
        i_field.pattern = "[0-9]+"
        i_field.min = 0
        i_field.placeholder = '>=0'
        i_field.id = field_name + '1'
        i_field.name = field_name + '1'
        i_span = document.createElement('span')
        i_span.innerHTML = '&amp;'
        i_field1 = i_field.cloneNode(false)
        i_field1.className = field_class[0]
        i_field1.id = field_name + '0'
        i_field1.name = field_name + '0'
        i_inner_div.appendChild(i_field1)
        i_inner_div.appendChild(i_span)
    }
    if(field_type_backend == 'date'){
        i_field.pattern = "^[0-9]{2}-[0-9]{2}-[0-9]{4}$"
        i_field.type = 'text'
        i_field.className = field_class[1]
        i_field.autocomplete="on"
        i_field.id = field_name + '1'
        i_field.name = field_name + '1'
        i_field.placeholder = 'to'
        i_span = document.createElement('span')
        i_span.innerHTML = '&amp;'
        i_field1 = i_field.cloneNode(false)
        i_field1.id = field_name + '0'
        i_field1.name = field_name + '0'
        i_field1.placeholder = 'from'
        i_field1.className = field_class[0]
        i_inner_div.appendChild(i_field1)
        i_inner_div.appendChild(i_span)
    }
    if(field_type_backend == 'bool'){
        i_field.className = field_class[0];
        var masVal = ['', 'Yes', 'No']
        for (var i = 0; i<masVal.length; i++){
            var i_option = document.createElement('option')
            i_option.value = masVal[i]
            i_option.innerHTML = masVal[i]
            i_field.appendChild(i_option)
        }
    }
    // add label to div
    parent_div.appendChild(i_div)
    i_div.appendChild(i_label)
    i_div.appendChild(i_inner_div)
    i_inner_div.appendChild(i_field)
    }


function create_group_fields_div(parent_div, name){
    var areas_div = document.createElement('div')
    areas_div.id = name
    parent_div.appendChild(areas_div)
    var inner_areas_div = document.createElement('div')
    inner_areas_div.className = 'headline'
    inner_areas_div.innerHTML = name
    areas_div.appendChild(inner_areas_div)
    return areas_div
}


function field_factory(id){
// get parent div
for (var group in jsonDictionary['fields']){
    var parent_div = document.getElementById(id);
    // create group div for fields
    if(group == 'area_of_testing_fields' && Object.keys(jsonDictionary['fields'][group]).length > 0){
        parent_div = create_group_fields_div(parent_div, 'AREAS OF TESTING')
    }
    /*
    if(group == 'special_fields' && Object.keys(jsonDictionary['fields'][group]).length > 0){
        parent_div = create_group_fields_div(parent_div, 'SPECIAL FIELDS')
    }
    */
    if(group == 'mondatory_fields' && Object.keys(jsonDictionary['fields'][group]).length > 0){
        parent_div = create_group_fields_div(parent_div, 'MANDATORY FIELDS')
    }
    
    for (var key in jsonDictionary['fields'][group]){
        var div_class = 'form-group'
        var label_class = 'col-sm-3 control-label'
        var inner_div_class = 'col-sm-9'
        var field_class = ['form-control input-custom']
        var field_type = null
        var field_tag = null
        if(jsonDictionary['fields'][group][key]['type'] == 'categorical'){
            field_tag = 'select'
            field_type = null
            inner_div_class = 'col-sm-9'
            }
        else{
            field_tag = 'input'
            if(['text', 'text1', 'text2'].includes(jsonDictionary['fields'][group][key]['type'])){
                field_type = 'text'
                div_class = 'form-group form-group-custom'
                }
            if(['number', 'date'].includes(jsonDictionary['fields'][group][key]['type'])){
                field_type = 'number'
                inner_div_class = "col-sm-9 input-interval"
                if(jsonDictionary['fields'][group][key]['type'] == 'date')
                    field_class = ['form-control input-custom req-selectCr1', "form-control input-custom req-selectCr3"]
                if(jsonDictionary['fields'][group][key]['type'] == 'number')
                    field_class = ['form-control input-custom req-selectCom1', "form-control input-custom req-selectCom3"]
                    }
            if(['bool'].includes(jsonDictionary['fields'][group][key]['type'])){
                field_tag = 'select'
                }
            }
            if (group == 'area_of_testing_fields'){
                addField(parent_div, div_class, label_class, inner_div_class,
                    key,jsonDictionary['fields'][group][key]['gui_name'], field_class, field_tag, field_type,
                    'bool')
            }
            else{
                addField(parent_div, div_class, label_class, inner_div_class,
                    key,jsonDictionary['fields'][group][key]['name'], field_class, field_tag, field_type,
                    jsonDictionary['fields'][group][key]['type'])
            }
        
    }
}
}


// ANALISYS & TRAINING page fields creation
if('undefined'.localeCompare(jsonDictionary['fields']) != 0){
    field_factory('fields');
    }


function set_placeholder(){
    for(var field in jsonDictionary['placeholder'])
        $('input[name="'+field+'"]').attr("placeholder", jsonDictionary['placeholder'][field])
}


if('undefined'.localeCompare(jsonDictionary['placeholder']) != 0){
    set_placeholder();
    }


// setting up markup only if version == 0
// disable settings module if version == 1
if('undefined'.localeCompare(jsonDictionary['inner']) != 0){
    if(jsonDictionary['inner'] == '1'){
        $("#div_murkup").addClass('disabledfilter');
        $("#areasDiv").addClass('disabledfilter');
        $("#setting").addClass('disabledfilter');

    }
}

// open train only if markup == 1
if('undefined'.localeCompare(jsonDictionary['murkup']) != 0){
    if(!jsonDictionary['isTrain']){
        $("#Train").prop("disabled",true);
    }
    else $("#Train").prop("disabled",false);
}


$('#murkup').change(function setAreas(){
    if($('#murkup').val()=='yes'){
        $("#areasDiv").removeClass('disabledfilter');
        $("#areas").prop('required',true);
        sessionStorage['murkup'] = $('#murkup').val();
        }
    else {
        $("#areasDiv").addClass('disabledfilter');
        $("#areas").prop('required',false);
        sessionStorage['murkup'] = $('#murkup').val();
    }
})
//---------------------------------------------------------------------------------------//


var successMas = ['file uploaded successfully',
                 'data filtered',
                 'filter dropped',
                 'file saved',
                 'chart builded']
function setMessage(){
    var idMessage = document.getElementById('message');
    idMessage.innerHTML = '';
    if('undefined'.localeCompare(jsonDictionary['message']) != 0)
        optimize_message(jsonDictionary['message']);
    if('undefined'.localeCompare(jsonDictionary['plot']) != 0)
        if(jsonDictionary['plot']['dynamic bugs'] == 'error'){
            optimize_message('CUMULATIVE CHART OF DEFECT SUBMISSION: dataset is small for this period ');
            document.getElementById('period').value = '1 weak';
            $('html, body').animate({scrollTop: 0}, 600);
            }
    if(!successMas.includes(jsonDictionary['message']))
        $('html, body').animate({scrollTop: 0}, 600);

    }
setMessage();


function optimize_message(message){
    var array = message.split(" ");

    var arrays = [], size = 6;
    while (array.length > 0)
        arrays.push(array.splice(0, size).join(" "));

    var files = ''
    for(var key in Object.keys(arrays))
        files = files + arrays[key] + '\n'
    var text = $("#message").text(files)
    text.html(text.html().replace(/\n/g,'<br/>'));
    text.html(text.html().replace(/"/g, ''));
    text.html(text.html().replace('&amp;#39;', "'"));
    text.html(text.html().replace('&amp;#39;', "'"));
    text.html(text.html().replace(/^(?:')/, ""));
    text.html(text.html().replace(/(?:'<br>)$/, ""));
}


function disableButtons(jsonDictionary){
    if('file uploaded successfully'.localeCompare(jsonDictionary['message']) == 0){
        $("#Apply").prop("disabled",false);
        $("#Build").prop("disabled",false);
        $("#Save").prop("disabled",false);
        $("#attributes-block").removeClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#distr-block").removeClass("disabledfilter");
        $("#statInfoBlock").removeClass("disabledfilter");
        $("#dynamicChartBlock").removeClass("disabledfilter");
        $("#topTerm").removeClass('disabledfilter');
    }
    if('data filtered'.localeCompare(jsonDictionary['message']) == 0){
        $("#Apply").prop("disabled",false);
        $("#Build").prop("disabled",false);
        $("#Save").prop("disabled",false);
        $("#Reset").prop("disabled",false);
        $("#attributes-block").removeClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#distr-block").removeClass("disabledfilter");
        $("#statInfoBlock").removeClass("disabledfilter");
        $("#dynamicChartBlock").removeClass("disabledfilter");
        $("#topTerm").removeClass('disabledfilter');
    }
    if('filter dropped'.localeCompare(jsonDictionary['message']) == 0){
        $("#Apply").prop("disabled",false);
        $("#Build").prop("disabled",false);
        $("#Save").prop("disabled",false);
        $("#Reset").prop("disabled",true);
        $("#attributes-block").removeClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#distr-block").removeClass("disabledfilter");
        $("#statInfoBlock").removeClass("disabledfilter");
        $("#dynamicChartBlock").removeClass("disabledfilter");
        $("#topTerm").removeClass('disabledfilter');
    }
    if('file saved'.localeCompare(jsonDictionary['message']) == 0){
        $("#Apply").prop("disabled",false);
        $("#Build").prop("disabled",false);
        $("#Reset").prop("disabled",false);
        $("#attributes-block").removeClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#distr-block").removeClass("disabledfilter");
        $("#statInfoBlock").removeClass("disabledfilter");
        $("#dynamicChartBlock").removeClass("disabledfilter");
        $("#topTerm").removeClass('disabledfilter');
    }
    if('chart builded'.localeCompare(jsonDictionary['message']) == 0){
        $("#Apply").prop("disabled",false);
        $("#Build").prop("disabled",false);
        $("#Save").prop("disabled",false);
        $("#Reset").prop("disabled",false);
        $("#attributes-block").removeClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#distr-block").removeClass("disabledfilter");
        $("#statInfoBlock").removeClass("disabledfilter");
        $("#dynamicChartBlock").removeClass("disabledfilter");
        $("#topTerm").removeClass('disabledfilter');
    }
    if('there are no rows corresponding to the condition'.localeCompare(jsonDictionary['message']) == 0){
        $("#Apply").prop("disabled",false);
        $("#Build").prop("disabled",false);
        $("#Save").prop("disabled",false);
        $("#attributes-block").removeClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#distr-block").removeClass("disabledfilter");
        $("#statInfoBlock").removeClass("disabledfilter");
        $("#dynamicChartBlock").removeClass("disabledfilter");
        $("#topTerm").removeClass('disabledfilter');
        // reset all values in filter form
        // $("#filterForm")[0].reset();
    }
    if('please use .csv file extension'.localeCompare(jsonDictionary['message']) == 0){
        $("#Apply").prop("disabled",false);
        $("#Build").prop("disabled",false);
        $("#Save").prop("disabled",false);
        $("#Reset").prop("disabled",false);
        $("#attributes-block").removeClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#distr-block").removeClass("disabledfilter");
        $("#statInfoBlock").removeClass("disabledfilter");
        $("#dynamicChartBlock").removeClass("disabledfilter");
        $("#topTerm").removeClass('disabledfilter');
    }
    if('incorrect file format. Please use only csv or xml'.localeCompare(jsonDictionary['message']) == 0){
        $("#Submit").prop("disabled",false);
        $("#Apply").prop("disabled",true);
        $("#Train").prop("disabled",true);
        $("#Save").prop("disabled",true);
        $("#Reset").prop("disabled",true);
        $("#Build").prop("disabled",true);
        $("#murkup").prop("disabled",true);
        $("#attributes-block").addClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#distr-block").addClass("disabledfilter");
        $("#statInfoBlock").addClass("disabledfilter");
        $("#dynamicChartBlock").addClass("disabledfilter");
        $("#topTerm").addClass('disabledfilter');
    }
    if('please use Xmax and StepSize value in the array [0,maxValue from stat info]'.localeCompare(jsonDictionary['message']) == 0){
        $("#Apply").prop("disabled",false);
        $("#Build").prop("disabled",false);
        $("#Save").prop("disabled",false);
        $("#Reset").prop("disabled",false);
        $("#attributes-block").removeClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#distr-block").removeClass("disabledfilter");
        $("#statInfoBlock").removeClass("disabledfilter");
        $("#dynamicChartBlock").removeClass("disabledfilter");
        $("#topTerm").removeClass('disabledfilter');
    }
    if('incorrect value for Xmax or StepSize'.localeCompare(jsonDictionary['message']) == 0){
        $("#Apply").prop("disabled",false);
        $("#Build").prop("disabled",false);
        $("#Save").prop("disabled",false);
        $("#Reset").prop("disabled",false);
        $("#attributes-block").removeClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#distr-block").removeClass("disabledfilter");
        $("#statInfoBlock").removeClass("disabledfilter");
        $("#dynamicChartBlock").removeClass("disabledfilter");
        $("#topTerm").removeClass('disabledfilter');
    }
    if('you are cannot to build frequency density chart for data with one value'.localeCompare(jsonDictionary['message']) == 0){
        $("#Apply").prop("disabled",false);
        $("#Build").prop("disabled",false);
        $("#Save").prop("disabled",false);
        $("#Reset").prop("disabled",false);
        $("#attributes-block").removeClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#distr-block").removeClass("disabledfilter");
        $("#statInfoBlock").removeClass("disabledfilter");
        $("#dynamicChartBlock").removeClass("disabledfilter");
        $("#topTerm").removeClass('disabledfilter');
    }
    if('not find regularExpression.csv'.localeCompare(jsonDictionary['message']) == 0){
        $("#Submit").prop("disabled",false);
        $("#Apply").prop("disabled",true);
        $("#Train").prop("disabled",true);
        $("#Save").prop("disabled",true);
        $("#Reset").prop("disabled",true);
        $("#Build").prop("disabled",true);
        $("#murkup").prop("disabled",true);
        $("#attributes-block").addClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#distr-block").addClass("disabledfilter");
        $("#statInfoBlock").addClass("disabledfilter");
        $("#dynamicChartBlock").addClass("disabledfilter");
        $("#topTerm").addClass('disabledfilter');
        }
    if(!jsonDictionary['isTrain']){
        $("#Train").prop("disabled",true);
    }

}
disableButtons(jsonDictionary);

//---------------------------------------------------------------------------------//

/*-- CHARTS CREATION --*/

// coordinates processing
function plot(x,y){
    var dictGraph = {};
    var masGraph = [];
    for(index =0; index < x.length; index++){
        dictGraph["x"] = x[index];
        dictGraph["y"] = y[index];
        masGraph[index] = dictGraph;
        dictGraph = {};
    }
    return masGraph;

}

// getting max value for X axis
function findMax(xLine, xHist, scale){
    var finalX = xLine.concat(xHist);
    var max = 0;
    if(scale == ''){
        for(index=0; index < finalX.length; index++){
            if(finalX[index]>max){
                max = finalX[index];
            }
        }
        if(max > 1)
            return max+1;
        else return max+0.01;
    }
    else return parseInt(scale);
}

// setting up step size
function setStepSize(stepSize){
    if(stepSize == ''){
        return null;
    }
    else return parseInt(stepSize);
}

// setting up step size for Y axis (to avoid incorrect behavior when small value received)
function setStepSizeY(yLine, yHist){
    var max = findMax(yLine, yHist, 0);
    if(max <= 0.0001) return 0.00001;
    if(max <= 0.0005) return 0.00005;
    if(max <= 0.001) return 0.0001;
    if(max <= 0.005) return 0.0005;
    if(max <= 0.01) return 0.001;
    if(max <= 0.05) return 0.005;
    if(max <= 0.1) return 0.01;
    if(max <= 0.5) return 0.05;
    if(max <= 1) return 0.1;
    if(max <= 5) return 0.5;
    if(max <= 10) return 1;
    if(max <= 15) return 1;
    if(max <= 50) return 5;
    if(max <= 100) return 10;
    if(max <= 500) return 50;
    if(max <= 1000) return 100;
    if(max <= 5000) return 500;
    if(max <= 10000) return 1000;
    if(max <= 50000) return 5000;
    if(max <= 100000) return 10000;
    if(max <= 500000) return 50000;
    if(max <= 1000000) return 100000;
}

// setting up default charts value
function defaultChart(){
                var ctx = $("#DistrLine");
                var myChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: [0],
                        datasets: [
                            {
                                borderWidth: 1,
                                data: [0]
                            }
                            ]
                    },
                    options: {
                        legend: {
                                 display:true,
                                 labels: {
                                          boxWidth: 0,
                                          fontSize: 0
                                          }
                                 },
                scales:{
                            xAxes:[{
                            scaleLabel: {
                                  display: true,
                                  labelString: 'number of days'
                                        },
                            type:'linear',
                            position:'bottom',

                            }
                           ],
                           yAxes:[{
                               scaleLabel: {
                                  display: true,
                                  labelString: 'relative frequency'
                                        }
                           }
                                 ]
                        },
                          elements: { point: { radius: 1 } }
                    }
                });
                return myChart;
}

function defaultDynamicChart(){
                                              var ctx = $("#dynamic");
                                              var myChart = new Chart(ctx, {
                                                  type: 'bar',
                                                  data: {
                                                      labels: [0],
                                                      datasets: [
                                                          {
                                                              borderWidth: 1,
                                                              data: [0]
                                                          }
                                                          ]
                                                  },
                                                  options: {
                                                      legend: {
                                                               display:true,
                                                               labels: {
                                                                        boxWidth: 0,
                                                                        fontSize: 0
                                                                        }
                                                               },
                                              scales:{
                                                          xAxes:[{
                                                              scaleLabel: {
                                                                          display: true,
                                                                          labelString: 'date'
                                                                        },
                                                              type:'linear',
                                                              position:'bottom'

                                                              }
                                                         ],
                                                          yAxes:[{
                                                              scaleLabel: {
                                                                         display: true,
                                                                          labelString: 'count of defects'
                                                                        },
                                                                    }
                                                              ]
                                                      },
                                                        elements: { point: { radius: 1 } }
                                                  }
                                              });
                                              return myChart;
                              }
//----------------------------------------------------------------------------------------------------------------------

function chooseThickness(type){
    if('undefined'.localeCompare(sessionStorage[type]) == 0 || sessionStorage[type] == ''){
        return 1;
        }
    else return sessionStorage[type];
}

// Frequency top chart
function relative_frequency(data){
                var relFreq = data['Relative Frequency']
                var xLine = relFreq[0];
                var yLine = relFreq[1];
                var ctx = $("#DistrLine");
                var myChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        datasets: [
                            {
                                steppedLine:true,
                                borderWidth: chooseThickness('relative'),
                                data: plot(xLine,yLine),
                                labels: xLine,
                                backgroundColor:["rgba(54, 162, 235, 0.3)"],
                                borderColor:["rgb(54, 162, 235)"]

                            }
                            ]
                    },
                    options: {
                        legend: {
                                 display:false,
                                 labels: {
                                          boxWidth: 0,
                                          fontSize: 0
                                          }
                                 },
                    scales:{    yAxes:[{
                                    scaleLabel: {
                                              display: true,
                                              labelString: 'relative frequency'
                                                    },
                                    ticks:{
                                           stepSize: setStepSizeY(yLine, 0),
                                           beginAtZero:true
                                           }
                                    }],
                            xAxes:[{
                            scaleLabel: {
                                      display: true,
                                      labelString: 'number of days'
                                            },
                            type:'linear',
                            position:'bottom',
                                ticks:{
                                    autoSkip: false,
                                    autoSkipPadding: 20,
                                    display:true,
                                    max: findMax(xLine, 0, data['scale']),
                                    stepSize: setStepSize(data['stepSize']),
                                    scaleLabel: {
                                                  display: true,
                                                  labelString: 'TTR'
                                                }
                                }
                            }
                           ]
                        },
                          elements: { point: { radius: 1 } }
                    }
                });
                return myChart;
}

// Dynamic chart
function dynamic_bugs(data){
                var relFreq = data['dynamic bugs'];
                var xLine = relFreq[0];
                var yLine = relFreq[1];
                var ctx = $("#dynamic");
                var myChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: xLine,
                        datasets: [
                            {
                                data: yLine,
                                borderWidth: chooseThickness('dynamic'),
                                backgroundColor:"rgba(54, 162, 235, 0.3)",
                                borderColor:"rgb(54, 162, 235)"
                            }
                            ]
                    },
                    options: {
                        legend: {
                            display:false,
                            labels: {
                                            boxWidth: 0,
                                            fontSize: 0
                                        }
                        },
                        scales:{
                            xAxes:[{
                                  scaleLabel: {
                                              display: true,
                                              labelString: 'date'
                                            }
                                  }],

                            yAxes:[{
                                    scaleLabel: {
                                                  display: true,
                                                  labelString: 'count of defects'
                                                },
                                    ticks:{

                                           stepSize: setStepSizeY(yLine, 0),
                                           beginAtZero:true
                                           }
                                    }]

                        },
                          elements: { point: { radius: 1 } }
                    }
                });
                return myChart;
}

function parseToDate(data){
    newData = [];
    for(date in data){
        newData.push(new Date(date));
    }
    return newData;
}

function choosePlot(jsonDictionary){
    var plotJson = jsonDictionary['plot'];
    var distributionChart;
    var dynamicChart;
    if('undefined'.localeCompare(plotJson) == 0){
        distributionChart = defaultChart();
        dynamicChart =  defaultDynamicChart();
    }
    for(key in plotJson){
        if(key == 'Relative Frequency'){
            distributionChart = relative_frequency(plotJson);
          }
        if(key == 'dynamic bugs'){
                    if(plotJson['dynamic bugs'] == 'error'){
                        dynamicChart = defaultDynamicChart();
                    }
                    else{
                        dynamicChart = dynamic_bugs(plotJson['dynamic bugs']);}
                  }
        }
    var charts = {'distribution':distributionChart, 'dynamic':dynamicChart};
    return charts;
}

var chartDict = choosePlot(jsonDictionary);
var distributionChart = chartDict['distribution'];
var dynamicChart = chartDict['dynamic'];


// on change dynamic chart creation
$('#period').change(function ajaxDynamic() {
    $.ajax({
            type: "POST",
            url: get_periodAJAX('/buildChart/onlyDynamic/'),
            beforeSend: setLoad(),
            success: function(response, status, xhr){
                if (response.redirect) {
                     window.location.href = response.redirect;
                   }
                else{
                    var ct = xhr.getResponseHeader("content-type") || "";
                    if (ct.indexOf('html') > -1)
                        document.write(response);
                    else {
                         jsonDictionary = response;
                         setMessage();
                         dynamicChart = updateDynamicPlot(dynamicChart, jsonDictionary['plot']['dynamic bugs']);
                         hideLoad();
                         setFileName();
                         }
                     }
                    },
            error: function(error) {
                document.getElementById('message').innerHTML = 'error dynamic plotting of charts';
                $('html, body').animate({scrollTop: 0}, 600);
                hideLoad();
                        }
            });
                    })

// on change distribution chart creation
function ajaxXDistribution() {
    $.ajax({
            type: "POST",
            url: '/buildChart/onlyDistribution/',
            data: $('#distrChart').serialize(),
            beforeSend: setLoad(),
            success: function(response, status, xhr){
                if (response.redirect) {
                     window.location.href = response.redirect;
                   }
                else{
                    var ct = xhr.getResponseHeader("content-type") || "";
                    if (ct.indexOf('html') > -1)
                        document.write(response);
                    else {
                         jsonDictionary = response;
                         setMessage();
                         distributionChart = updateDistributionPlot(distributionChart, jsonDictionary);
                         hideLoad();
                         setFileName();
                         }
                     }
                    },
            error: function(error) {
                document.getElementById('message').innerHTML = 'error dynamic plotting of charts';
                $('html, body').animate({scrollTop: 0}, 600);
                hideLoad();
                        }
            });
                    }

$('#x').change(function(){
                            ajaxXDistribution();
                            if($('#x').val() == 'ttr')
                                distributionChart.options.scales.xAxes[0].scaleLabel.labelString = 'number of days'
                            else
                                distributionChart.options.scales.xAxes[0].scaleLabel.labelString = 'number of '+$('#x').val()
                            distributionChart.update()
                          })
$('#y').change(function(){
                            ajaxXDistribution();
                            distributionChart.options.scales.yAxes[0].scaleLabel.labelString = $('#y').val()
                            distributionChart.update()
                         })
$('#scale').change(function(){ajaxXDistribution()})
$('#stepSize').change(function(){ajaxXDistribution()})

function redraw(block,id){
 $('#'+id).remove();
 $('#'+block).after("<canvas id="+id+"></canvas>");
}

function updateDynamicPlot(dynamicChart, jsonDictionary){
    dynamicChart.data.labels = jsonDictionary[0];
    dynamicChart.data.datasets[0].data = jsonDictionary[1];
    dynamicChart.data.datasets[0].borderWidth = chooseThickness('dynamic');
    dynamicChart.options.scales.yAxes[0].ticks.stepSize = setStepSizeY(jsonDictionary[1], 0);
    dynamicChart.update();
    return dynamicChart;
}


function updateDistributionPlot(distributionChart, jsonDictionary){
    // get_line_thickness();
    for(key in jsonDictionary['plot']){
        if(key == 'Relative Frequency'){
            distributionChart.data.datasets[0].labels = jsonDictionary['plot']['Relative Frequency'][0];
            distributionChart.data.datasets[0].data = plot(jsonDictionary['plot']['Relative Frequency'][0],jsonDictionary['plot']['Relative Frequency'][1]);
            distributionChart.data.datasets[0].steppedLine = true;
            distributionChart.data.datasets[0].borderColor = ["rgb(54, 162, 235)"];
            distributionChart.data.datasets[0].backgroundColor = ["rgba(54, 162, 235, 0.3)"];
            distributionChart.data.datasets[0].borderWidth = chooseThickness('relative');
            distributionChart.data.datasets[1] = {};
            distributionChart.options.scales.yAxes[0].ticks.stepSize = setStepSizeY(jsonDictionary['plot']['Relative Frequency'][1], 0);
            distributionChart.options.scales.xAxes[0].ticks.max = findMax(jsonDictionary['plot']['Relative Frequency'][0], 0, jsonDictionary['plot']['scale']);
            distributionChart.options.scales.xAxes[0].ticks.stepSize = setStepSize(jsonDictionary['plot']['stepSize']);
            distributionChart.options.elements.point.radius = 0.5;
            distributionChart.update();
            //distributionChart = relative_frequency(jsonDictionary['plot']);
            return distributionChart;
          }
        if(key == 'Frequency density'){
            if(jsonDictionary['plot']['Frequency density']['line'][0] == -1 && jsonDictionary['plot']['Frequency density']['line'][1] == -1){
                distributionChart.data.datasets[0].labels = jsonDictionary['plot']['Frequency density']['histogram'][0];
                distributionChart.data.datasets[0].data = plot(jsonDictionary['plot']['Frequency density']['histogram'][0], jsonDictionary['plot']['Frequency density']['histogram'][1]);
                distributionChart.data.datasets[0].steppedLine = true;
                distributionChart.data.datasets[0].borderColor = ["rgb(54, 162, 235)"];
                distributionChart.data.datasets[0].backgroundColor = ["rgba(54, 162, 235, 0.3)"];
                distributionChart.data.datasets[0].borderWidth = chooseThickness('relative');
                distributionChart.data.datasets[1] = {};
                distributionChart.options.scales.yAxes[0].ticks.stepSize = setStepSizeY(jsonDictionary['plot']['Frequency density']['histogram'][1], 0);
                distributionChart.options.scales.xAxes[0].ticks.max = findMax(jsonDictionary['plot']['Frequency density']['histogram'][0], 0, '');
                distributionChart.options.scales.xAxes[0].ticks.stepSize = setStepSize('');
                distributionChart.options.elements.point.radius = 0.5;
                distributionChart.update();
                return distributionChart;
                }
            distributionChart.data.datasets[0].labels = jsonDictionary['plot']['Frequency density']['line'][0];
            distributionChart.data.datasets[0].data = plot(jsonDictionary['plot']['Frequency density']['line'][0],jsonDictionary['plot']['Frequency density']['line'][1]);
            distributionChart.data.datasets[0].steppedLine = false;
            distributionChart.data.datasets[0].borderColor = ["rgb(255, 99, 132)"];
            distributionChart.data.datasets[0].backgroundColor = ["rgba(255, 255, 255, 0.0)"];
            distributionChart.data.datasets[0].borderWidth = chooseThickness('density');
            distributionChart.data.datasets[1] = {};
            distributionChart.data.datasets[1].data = plot(jsonDictionary['plot']['Frequency density']['histogram'][0],jsonDictionary['plot']['Frequency density']['histogram'][1]);
            distributionChart.data.datasets[1].labels = jsonDictionary['plot']['Frequency density']['histogram'][0];
            distributionChart.data.datasets[1].steppedLine = true;
            distributionChart.data.datasets[1].borderColor = ["rgb(54, 162, 235)"];
            distributionChart.data.datasets[1].backgroundColor = ["rgba(54, 162, 235, 0.3)"];
            distributionChart.data.datasets[1].borderWidth = chooseThickness('density');
            distributionChart.options.scales.yAxes[0].ticks.stepSize = setStepSizeY(jsonDictionary['plot']['Frequency density']['line'][1], jsonDictionary['plot']['Frequency density']['histogram'][1]);
            distributionChart.options.scales.xAxes[0].ticks.max = findMax(jsonDictionary['plot']['Frequency density']['line'][0], jsonDictionary['plot']['Frequency density']['histogram'][0], jsonDictionary['plot']['scale']);
            distributionChart.options.scales.xAxes[0].ticks.stepSize = setStepSize(jsonDictionary['plot']['stepSize']);
            distributionChart.options.elements.point.radius = 0.5;
            distributionChart.update();
            //distributionChart = frequency_density(jsonDictionary['plot']);
            return distributionChart;
        }
        }
}


// dynamically change line thickness
// dynamic plot
$('#dynamic_dropdownMenu2 li').click(function(){
        //get_line_thickness();
        sessionStorage["dynamic"] = $(this).attr("value")
        dynamicChart.data.datasets[0].borderWidth = chooseThickness('dynamic');
        dynamicChart.update();
        // use return false to prevent page autoscrolling
        return false;
    })


// Distribution chart
$('#destr_dropdownMenu2 li').click(function(){
    // get_line_thickness();
    if($("#y").find(":selected").text() == 'Relative Frequency'){
        sessionStorage['relative'] = $(this).attr("value")
        distributionChart.data.datasets[0].borderWidth = chooseThickness('relative');
        distributionChart.update();
        return false
        }
    else {
        sessionStorage['density'] = $(this).attr("value")
        distributionChart.data.datasets[0].borderWidth = chooseThickness('density');
        distributionChart.data.datasets[1].borderWidth = chooseThickness('density');
        distributionChart.update();
        return false
        }
})


//-------------------------------------------------------------------------------------------//


function get_period(action){
    if(action == '/buildChart/frequency/')
        $('#distrChart').attr('action',action+'?period='+$('#period').val());
    if(action == '/filtering')
        $('#filterForm').attr('action',action+'?ReferringTo='+$('#ReferringTo').val());
    if(action == '/resetFilter')
        $('#resetForm').attr('action',action+'?period='+$('#period').val());
    if(action == '/saveSubset')
        $('#saveForm').attr('action',action+'?period='+$('#period').val());
}

function get_periodAJAX(action){
    if(action == '/buildChart/frequency/')
        return action+'?period='+$('#period').val();
    if(action == '/buildChart/onlyDynamic/')
        return action+'?period='+$('#period').val();
    if(action == '/filtering')
        return action+'?period='+$('#period').val();
    if(action == '/resetFilter')
        return action+'?period='+$('#period').val();
    if(action == '/saveSubset')
        return action+'?period='+$('#period').val();
}

//------------------------------------

/*-- STAT INFO --*/

function statInfo(jsonDictionary){
    var statInfo = jsonDictionary;

    var filtered = document.getElementById('filtered');
        filtered.innerHTML = statInfo['filtered']
    var total = document.getElementById('total');
        total.innerHTML = statInfo['total']
    var ttrStat = statInfo['ttrStat']
    var ttrMax = document.getElementById('ttrMax');
        ttrMax.innerHTML = ttrStat['max']
    var ttrMin = document.getElementById('ttrMin');
        ttrMin.innerHTML = ttrStat['min']
    var ttrMean = document.getElementById('ttrMean');
        ttrMean.innerHTML = ttrStat['mean']
    var ttrStd = document.getElementById('ttrStd');
        ttrStd.innerHTML = ttrStat['std']

    var commentStat = statInfo['commentStat']
    var commentMax = document.getElementById('commentMax');
        commentMax.innerHTML = commentStat['max']
    var commentMin = document.getElementById('commentMin');
        commentMin.innerHTML = commentStat['min']
    var commentMean = document.getElementById('commentMean');
        commentMean.innerHTML = commentStat['mean']
    var commentStd = document.getElementById('commentStd');
        commentStd.innerHTML = commentStat['std']

    var attachmentStat = statInfo['attachmentStat']
    var attachmentMax = document.getElementById('attachmentMax');
        attachmentMax.innerHTML = attachmentStat['max']
    var attachmentMin = document.getElementById('attachmentMin');
        attachmentMin.innerHTML = attachmentStat['min']
    var attachmentMean = document.getElementById('attachmentMean');
        attachmentMean.innerHTML = attachmentStat['mean']
    var attachmentStd = document.getElementById('attachmentStd');
        attachmentStd.innerHTML = attachmentStat['std']
}

if('undefined'.localeCompare(jsonDictionary['statInfo']) != 0)
        statInfo(jsonDictionary['statInfo']);

//-----------------------------------------------------------------//

// categorical fields
function addOption(name, mas){
    if(mas.length == 1 && mas[0] == 'null'){
     $(name).prop("disabled",true);
    }
    else
        for(i=0;i<mas.length;i++){
            $(name).append($("<option></option>").attr("value",replaceForCategoric(mas[i])).text(replaceForCategoric(mas[i])));
        }
}

function forEach(mas){
    for(key in mas){
        addOption("[id='"+key+"']",mas[key]);
    }
}

function categoricFields(jsonDictionary){
    var categorical = jsonDictionary;
    forEach(categorical);
}

//  categorical fields processing
if('undefined'.localeCompare(jsonDictionary['categoric']) != 0){
        categoricFields(jsonDictionary['categoric']);
        }

//---------------------------------------------------------------------------//

function addOptionAJAX(name, mas){
    if(mas.length == 1 && mas[0] == 'null'){
        $(name).prop("disabled",true);
    }
    else{
        for(i=0;i<mas.length;i++){
            $(name).append($("<option></option>").attr("value",replaceForCategoric(mas[i])).text(replaceForCategoric(mas[i])));
        }
    }
}

function forEachAJAX(mas){
    for(key in mas){
        if(key == 'ReferringTo')
            $('#ReferringTo').find('option').remove().end();
        else removeOptionsAJAX(document.getElementById(key));
        addOptionAJAX("[id='"+key+"']",mas[key]);
    }
}

function categoricFieldsAJAX(jsonDictionary){
    forEachAJAX(jsonDictionary);
}

function removeOptionsAJAX(selectbox)
{
    var i;
    for(i = selectbox.options.length - 1 ; i >= 0 ; i--)
    {
        selectbox.remove(i);
    }
}

//---------------------------------------------------------------------------//


function replace(val){
    if(val == "&gt;")
        return ">"
    else {
        if(val == "&lt;")
            return "<"
        else{
            if(val == "&lt;=")
                return "<="
                else{
                    if(val == "&gt;=")
                        return ">="
                    else{return val}
                }
        }
    }
}

function replaceForCategoric(val){
    if(Array.isArray(val))
            var val = val.join()
    //use toString() for case when val not str
    if(val === null)
        return val 
    return val.toString().replace(new RegExp('&amp;', 'g'),'&').replace(new RegExp('&gt;', 'g'),'>').replace(new RegExp('&lt;', 'g'),'<').replace(new RegExp('&lt;=', 'g'),'<=').replace(new RegExp('&gt;=', 'g'),'>=').replace(new RegExp('&gt;=', 'g'),'>=').replace(new RegExp("&#39;", 'g'),"'");
}


function attributes(attrib){
    for(key in attrib){
        if(!attrib[key]){
            $("[id^="+"'"+key+"'"+"]").prop("disabled",true);
           }
        else{
        if(key == 'SignificanceTop'){
          if(typeof attrib[key] != 'object')
              $('#significanceTop').prop("disabled",true);
          else{
                // for correct hyphenation add space for any world
                attrib[key] = attrib[key].map(function(field){return " "+field})
                $("#significanceTop").html(attrib[key].join());
          }
          }
        if(key == 'ReferringTo')
          $('#ReferringTo').val(replaceForCategoric(attrib[key]));
        if(key == 'freqTop'){
          sessionStorage['moreFreq'] = 0;
          $('#moreFreq').prop('disabled', false);
          setTopFreq();
        }
        $("[id='"+key+"']").val(replaceForCategoric(attrib[key]));
    }
    }
}


// use this function in cases when we need to convert boolean to Yes/No
function from_bool(val){
    if (typeof val === "boolean")
        if (val==true)
            return 'Yes'
        else return 'No'
    else
        return val
}


function attributesAJAX(attrib, keys){
    // use keys to put categorical fields only
    for(var key in keys){
            if(keys[key] in attrib){
                // put values of significance top
                if(keys[key] == 'ReferringTo'){
                    $('#ReferringTo').val(replaceForCategoric(attrib[keys[key]]));
                    }
                if(keys[key] == 'freqTop'){
                // reset counter
                sessionStorage['moreFreq'] = 0;
                $('#moreFreq').prop('disabled', false);
                setTopFreq();
                        }
                // if field is select2 that he have massive of values
                if(Array.isArray(attrib[keys[key]])){
                    $("[id='"+keys[key]+"']").val(attrib[keys[key]]).trigger('change');
                }
                else{
                    $("[id='"+keys[key]+"']").val(replaceForCategoric(from_bool(attrib[keys[key]])))
                }
            }
    }
    // reset values to default
    $("#period").val('1 week');
    //$("#LineWidthPeriod").val('1');
    //$("#DistributionThickness").val('1');
    sessionStorage['relative'] = 1;
    sessionStorage['density'] = 1;
    sessionStorage['dynamic'] = 1
    $("#y").val('Relative Frequency');
    $("#x").val('ttr');
    $("#stepSize").val('');
    $("#scale").val('')
}


function getPoeriods(period){
    if(period == '10D')
        return '10 days';
    if(period == 'W-SUN')
        return '1 week';
    if(period == '3M')
        return '3 months';
    if(period == '6M')
        return '6 months';
    if(period == 'A-DEC')
        return '1 year';
}

if('undefined'.localeCompare(jsonDictionary['attributes']) != 0)
    attributes(jsonDictionary['attributes']);

// top of the words displaying
function setTopFreq(){
    // for correct hyphenation add space for each world
    jsonDictionary['attributes']['freqTop'] = jsonDictionary['attributes']['freqTop'].map(function(field){return " "+field})
    $("#freqTop").html((jsonDictionary['attributes']['freqTop'].slice(0, parseInt(sessionStorage['moreFreq'], 10)+20).join()));
    sessionStorage['moreFreq'] = parseInt(sessionStorage['moreFreq'], 10) + 20;
    if(parseInt(sessionStorage['moreFreq'], 10) == 100){
        $('#moreFreq').prop('disabled', true);
        $("#Reset").prop("disabled",false);
        }
}


//---------------------------form closing---------------------------//

function closeSave() {
       document.getElementById('Close').click();
   };

//-------------------------fields validation-------------------------//

$(function(){
    for(var group in jsonDictionary['fields'])
        for(var el in jsonDictionary['fields'][group])
            if(jsonDictionary['fields'][group][el]['type'] == 'date'){
                $("[id='"+el+0+"']").datepicker({
                  dateFormat:"dd-mm-yy",
                  beforeShow:function(input,inst) {
                      $('#'+inst.id).datepicker("option","maxDate",$("[id='"+el+1+"']").val());
                  }
                  });
                $("[id='"+el+1+"']").datepicker({
                    dateFormat:"dd-mm-yy",
                    beforeShow:function(input,inst) {
                      $("[id='"+inst.id+"']").datepicker("option","minDate",$("[id='"+el+0+"']").val());
                  }
                });
          }


$("#Choose").change(function () {
      //var fPath = $(this).val();
      //var slashPos = fPath.lastIndexOf("\\");
      //sessionStorage["fName"] = fPath.slice(slashPos+1);

      var inputFile = document.getElementById('Choose').files;
      var files = ''
      for(var key in Object.keys(inputFile))
          files = files + inputFile[key]['name'] + '\n'
      var text = $("#file-name").text(files)
      text.html(text.html().replace(/\n/g,'<br/>'));
      sessionStorage["fName"] = files

      //$("#file-name").html(sessionStorage["fName"]);
      $("#message").html('');
})
});

function setFileName(){
    if(sessionStorage["finalName"] != ''){
        //$("#file-name").html(sessionStorage["finalName"]);
        var text = $("#file-name").text(sessionStorage["finalName"])
        text.html(text.html().replace(/\n/g,'<br/>'));
    }
    else {
        //$("#file-name").html(sessionStorage["fName"]);
        var text = $("#file-name").text(sessionStorage["fName"])
        text.html(text.html().replace(/\n/g,'<br/>'));
    }
    $('#Choose').val('');
}
setFileName();

function setFinalFileNameLocalStorage() {
            sessionStorage["finalName"] =  sessionStorage["fName"]
          };

function clearFileNameLocalStorage() {
            sessionStorage.removeItem("fName");
            sessionStorage.removeItem("finalName");
            sessionStorage.removeItem("relative");
            sessionStorage.removeItem("density");
            sessionStorage.removeItem("dynamic");
          };
function clearChartStorage() {
            sessionStorage.removeItem("density");
            sessionStorage.removeItem("relative");
            sessionStorage.removeItem("dynamic");
          };

function saveFile() {
    $('#FileName').val($('#FileName')[0].value.trim())
    if($('#FileName')[0].checkValidity() == false){
            $('#saveForm').find(':submit').click();}
    else{
    $.ajax({
            type: "POST",
            url: '/saveSubset',
            data: $('#saveForm').serialize(),
            beforeSend: setLoad(),
            success:
               function(response, status, xhr){
                         if (response.redirect) {
                              window.location.href = response.redirect;
                            }
                         else{
                             $('#Close').click();
                             var ct = xhr.getResponseHeader("content-type") || "";
                             if (ct.indexOf('html') > -1){
                                document.write(response);
                                }
                             else{
                                //download.bind(true, "csv", $('#FileName').val());
                                var blob = new Blob([response]);
                                var link = document.createElement('a');
                                link.href = window.URL.createObjectURL(blob);
                                link.download = $('#FileName').val();
                                link.click();
                               }
                         }
                         },
            complete:
                function(jqXHR, textStatus){
                    var ct = jqXHR.getResponseHeader("content-type") || "";
                    if (textStatus == 'success' && ct.indexOf('html') == -1){
                        delTempFiles();
                        setFileName();
                        hideLoad();
                        }
                    },
            error: function(response, error) {
                document.getElementById('message').innerHTML = 'error of saving file';
                $('html, body').animate({scrollTop: 0}, 600);
                hideLoad();
                    }
            });
                    }}

function delTempFiles(){
    $.ajax({
                type: "POST",
                url: '/delTempFiles',
                error: function(error) {
                    document.getElementById('message').innerHTML =  'error of deleting temp files';
                    $('html, body').animate({scrollTop: 0}, 600);
                    hideLoad();
                        }
                });
                        }

$('#ReferringTo').change(function significanceTop() {
                         $.ajax({
                                 type: "POST",
                                 url: '/significanceTop',
                                 data: $('#topTermsForm').serialize(),
                                 beforeSend: setLoad(),
                                 success: function(response, status, xhr){
                                     if (response.redirect) {
                                          window.location.href = response.redirect;
                                        }
                                     else{
                                         var ct = xhr.getResponseHeader("content-type") || "";
                                         if (ct.indexOf('html') > -1)
                                            document.write(response);
                                         else {
                                           if(response['SignificanceTop'] == 'error'){
                                                document.getElementById('message').innerHTML = 'not find regularExpression.csv';
                                                $('html, body').animate({scrollTop: 0}, 600);
                                                disableButtons({'message': 'not find regularExpression.csv'})
                                                hideLoad()
                                           }
                                           else{
                                               // for correct hyphenation add space for each world
                                               response['SignificanceTop'] = response['SignificanceTop'].map(function(field){return " "+field})
                                               $("#significanceTop").html(response['SignificanceTop'].join());
                                               hideLoad();
                                               setFileName();
                                           }
                                           }
                                       }
                                     },
                                 error: function(error) {
                                     document.getElementById('message').innerHTML = 'error dynamic plotting of significance top';
                                     $('html, body').animate({scrollTop: 0}, 600);
                                     hideLoad();
                                             }
                                 });
                                         })


function sleep(ms) {
    ms += new Date().getTime();
    while (new Date() < ms){}
}


function filtering() {
    $(':input').attr('title', '');
    $(':input').attr('data-original-title', '');
    var com = checkComAtTt(jsonDictionary)
    var validate = checkValidation(jsonDictionary)
    if(!validate || !com[0]){
        //$('#'+com[1]).val('error')
        //$('#filterForm').find(':submit').click();
        $('.error_field:first').tooltip({placement: 'bottom'});
        $('.error_field:not(:first)').tooltip({placement: 'top'});
        $('.error_field:first').tooltip('show');
        //sleep(1000)
        //$('#'+com[1]).val(com[2])
        return;
    }
    $.ajax({
         type: "POST",
         url: '/filtering?ReferringTo='+$('#ReferringTo').val(),
         beforeSend: setLoad(),
         data: $('#filterForm').serialize(),
         success: function(response, status, xhr){
             if (response.redirect) {
                 window.location.href = response.redirect;
               }
             else{
                 var ct = xhr.getResponseHeader("content-type") || "";
                 if (ct.indexOf('html') > -1)
                    document.write(response);
                 else {
                       jsonDictionary = response;
                       if (jsonDictionary['attributes']['freqTop'] == 'error' || jsonDictionary['attributes']['SignificanceTop'] == 'error' || jsonDictionary['freqTop'] == 'error'){
                           document.getElementById('message').innerHTML = 'not find regularExpression.csv';
                           $('html, body').animate({scrollTop: 0}, 600);
                           disableButtons({'message': 'not find regularExpression.csv'})
                           hideLoad();
                       }
                       else{
                            setMessage();
                            disableButtons(jsonDictionary);
                            statInfo(jsonDictionary['statInfo']);
                            categoricFieldsAJAX(jsonDictionary['categoric']);
                            attributesAJAX(jsonDictionary['attributes'], Object.keys(jsonDictionary['categoric']));
                            dynamicChart = updateDynamicPlot(dynamicChart, jsonDictionary['plot']['dynamic bugs']['dynamic bugs']);
                            distributionChart = updateDistributionPlot(distributionChart, jsonDictionary);
                            $('html, body').animate({scrollTop: 0}, 600);
                            $("#Reset").prop("disabled",false);
                            setFileName();
                            hideLoad();
                       }
                  }
              }
             },
         error: function(error) {
             document.getElementById('message').innerHTML = 'error of dynamic filtering';
             $('html, body').animate({scrollTop: 0}, 600);
             hideLoad();
                     }
         });
    }

function reset1() {
    $.ajax({
            type: "POST",
            url: '/resetFilter',
            beforeSend: function resetForm(){ setLoad(); $("#filterForm")[0].reset();},
            success: function(response, status, xhr){
                if (response.redirect) {
                    window.location.href = response.redirect;
                }
                else{
                    var ct = xhr.getResponseHeader("content-type") || "";
                    if (ct.indexOf('html') > -1)
                    document.write(response);
                    else {
                    jsonDictionary = response;
                    setMessage();
                    disableButtons(jsonDictionary);
                    statInfo(jsonDictionary['statInfo']);
                    categoricFieldsAJAX(jsonDictionary['categoric']);
                    attributesAJAX(jsonDictionary['attributes'], Object.keys(jsonDictionary['categoric']));
                    dynamicChart = updateDynamicPlot(dynamicChart, jsonDictionary['plot']['dynamic bugs']['dynamic bugs']);
                    distributionChart = updateDistributionPlot(distributionChart, jsonDictionary);
                    //$("#Reset").prop("disabled",true);
                    hideLoad();
                    setFileName();
                    clearChartStorage();
                    filtering();
                    }
                }
                    },
            error: function(error) {
                document.getElementById('message').innerHTML = 'error of dynamic reset filter';
                $('html, body').animate({scrollTop: 0}, 600);
                hideLoad();
                        }
            });
                    }

// processing animation
function hideLoad() {
        if(!jsonDictionary['isTrain']){
            $("#Train").prop("disabled",true);
        }
         $("#load").removeAttr("style").hide();
         $('#loadDiv').removeClass("disabledfilter");
      }
function setLoad() {
         $("#load").show();
         $('#loadDiv').addClass('disabledfilter');
         }

// date fields validation
function checkValidation(jsonDictionary){
    var fields = [];
    var invalid_values = [];
    var datePattern = /^[0-9]{2}-[0-9]{2}-[0-9]{4}$/;
    for( var group in jsonDictionary['fields'])
        for(var el in jsonDictionary['fields'][group])
                if(['text', 'text2', 'text1', 'date'].includes(jsonDictionary['fields'][group][el]['type'])){
                    if(jsonDictionary['fields'][group][el]['type'] == 'date'){
                        // check that left hand less than right hand
                        $("[id='"+el+0+"']").val($("[id='"+el+0+"']").val().trim())
                        $("[id='"+el+1+"']").val($("[id='"+el+1+"']").val().trim())
                        if($("[id='"+el+0+"']").val() != '' && $("[id='"+el+1+"']").val() != ''){
                            if((new Date($("[id='"+el+0+"']").val().split("-")[2], $("[id='"+el+0+"']").val().split("-")[1], $("[id='"+el+0+"']").val().split("-")[0])).isDate() && 
                            (new Date($("[id='"+el+1+"']").val().split("-")[2], $("[id='"+el+1+"']").val().split("-")[1], $("[id='"+el+1+"']").val().split("-")[0])).isDate()){
                                if($("[id='"+el+0+"']").val() > $("[id='"+el+1+"']").val()){
                                    // for get boostrap message we insert text to number field
                                    //$("[id='"+el+0+"']").val('error')
                                    $("[id='"+el+0+"']").removeClass('input-custom').addClass('error_field')
                                    $("[id='"+el+1+"']").removeClass('input-custom').addClass('error_field')
                                    document.getElementById(el+0).setAttribute('data-original-title', 'Start value should be less than end value');
                                    document.getElementById(el+1).setAttribute('data-original-title', 'Start value should be less than end value');
                                    invalid_values.push(el+0, el+1);
                                }
                                else{
                                    $("[id='"+el+0+"']").removeClass('error_field').addClass('input-custom');
                                    $("[id='"+el+1+"']").removeClass('error_field').addClass('input-custom');
                                }
                            }
                            else{
                                document.getElementById(el+0).setAttribute('data-original-title', 'Invalid value');
                                $("[id='"+el+0+"']").removeClass('input-custom').addClass('error_field')
    
                                // set error message for tooltip
                                document.getElementById(el+1).setAttribute('data-original-title', 'Invalid value');
                                $("[id='"+el+1+"']").removeClass('input-custom').addClass('error_field')
    
                                invalid_values.push(el+0, el+1);
                            }
                            
                        }
                        else{
                             if ($("[id='"+el+0+"']").val() != "" && 
                            !((new Date($("[id='"+el+0+"']").val().split("-")[2], $("[id='"+el+0+"']").val().split("-")[1], $("[id='"+el+0+"']").val().split("-")[0])).isDate())){
                            $("[id='"+el+0+"']").removeClass('input-custom').addClass('error_field');
                                document.getElementById(el+0).setAttribute('data-original-title', 'Invalid value');
                                invalid_values.push(el+0, el+1);
                             }
                             else if ($("[id='"+el+1+"']").val() != "" && 
                             !((new Date($("[id='"+el+1+"']").val().split("-")[2], $("[id='"+el+1+"']").val().split("-")[1], $("[id='"+el+1+"']").val().split("-")[0])).isDate())){
                                $("[id='"+el+1+"']").removeClass('input-custom').addClass('error_field');
                                document.getElementById(el+1).setAttribute('data-original-title', 'Invalid value');
                                invalid_values.push(el+0, el+1);
                             }
                             else{
                                $("[id='"+el+0+"']").removeClass('error_field').addClass('input-custom');
                                $("[id='"+el+1+"']").removeClass('error_field').addClass('input-custom');
                             }
                        }
                        fields.push(el+0, el+1);
                    }
                    else{
                        $("[id='"+el+"']").val($("[id='"+el+"']").val().trim())
                        fields.push(el);
                    }
                }
    fields.forEach(function(item, i, arr){
        if (!$("[id='"+item+"']")[0].checkValidity() && invalid_values.indexOf(item) == -1){
            $("[id='"+item+"']").removeClass('input-custom').addClass('error_field')
            document.getElementById(item).setAttribute('data-original-title', 'Invalid value');
            invalid_values.push(item)
        }
        else if (invalid_values.indexOf(item) == -1){
            $("[id='"+item+"']").removeClass('error_field').addClass('input-custom');
            $("[id='"+item+"']").attr('data-original-title', '');
        }
        document.getElementById(item).setAttribute('data-toggle', 'tooltip');

    })

    var bool_fields = fields.map(function(field){return $("[id='"+field+"']")[0].checkValidity() && invalid_values.indexOf(field) == -1})
    return bool_fields.reduce(function(sum, current){return sum && current}, true)
}

Date.prototype.isDate = function(){
    return (this !== "Invalid Date" && !isNaN(this)) ? true : false;
}


function validateForLoadFile(){
    if($('#Choose')[0].checkValidity() == false){
        hideLoad()
        return
        }
}

function checkComAtTt(jsonDictionary){
    var fields = [];
    var final = []
    var invalid_values = [];
    var f = false
    var id = false
    for( var group in jsonDictionary['fields'])
        for(var el in jsonDictionary['fields'][group])
                if(jsonDictionary['fields'][group][el]['type'] == 'number'){
                    $("[id='"+el+0+"']").val($("[id='"+el+0+"']").val().trim())
                    $("[id='"+el+1+"']").val($("[id='"+el+1+"']").val().trim())
                    // check that left value less than right value
                    if($("[id='"+el+0+"']").val() != '' && $("[id='"+el+1+"']").val() != ''){
                        if(!isNaN(parseInt($("[id='"+el+0+"']").val(), 10)) && !isNaN(parseInt($("[id='"+el+1+"']").val(),10))){
                            if(Number($("[id='"+el+0+"']").val()) > Number($("[id='"+el+1+"']").val())){
                                if(f == false){
                                    f = $("[id='"+el+0+"']").val()
                                    id = el+0
                                }
                                // to get boostrap message we need to insert text to number field
                                // set error message for tooltip
                                document.getElementById(el+0).setAttribute('data-original-title', 'Start value should be less than end value');
                                $("[id='"+el+0+"']").removeClass('input-custom').addClass('error_field')

                                // set error message for tooltip
                                document.getElementById(el+1).setAttribute('data-original-title', 'Start value should be less than end value');
                                $("[id='"+el+1+"']").removeClass('input-custom').addClass('error_field')


                                invalid_values.push(el+0, el+1);
                            }
                            else{
                                $("[id='"+el+0+"']").removeClass('error_field').addClass('input-custom');
                                $("[id='"+el+1+"']").removeClass('error_field').addClass('input-custom');
                            }
                        }
                        else{
                                document.getElementById(el+0).setAttribute('data-original-title', 'Invalid value');
                                $("[id='"+el+0+"']").removeClass('input-custom').addClass('error_field')

                                // set error message for tooltip
                                document.getElementById(el+1).setAttribute('data-original-title', 'Invalid value');
                                $("[id='"+el+1+"']").removeClass('input-custom').addClass('error_field')

                                invalid_values.push(el+0, el+1);
                        }
                    }
                    else{
                         if ($("[id='"+el+0+"']").val() != "" && $("[id='"+el+0+"']").val() != "0" && !Number($("[id='"+el+0+"']").val()) ){
                            $("[id='"+el+0+"']").removeClass('input-custom').addClass('error_field');
                            document.getElementById(el+0).setAttribute('data-original-title', 'Invalid value');
                            invalid_values.push(el+0, el+1);
                         }
                         else if ($("[id='"+el+1+"']").val() != "" && $("[id='"+el+1+"']").val() != "0" && !Number($("[id='"+el+1+"']").val())){
                            $("[id='"+el+1+"']").removeClass('input-custom').addClass('error_field');
                            document.getElementById(el+1).setAttribute('data-original-title', 'Invalid value');
                            invalid_values.push(el+0, el+1);
                         }
                         else{
                            $("[id='"+el+0+"']").removeClass('error_field').addClass('input-custom');
                            $("[id='"+el+1+"']").removeClass('error_field').addClass('input-custom');
                         }
                    }
                    
                    fields.push(el+0, el+1)
                }
    fields.forEach(function(item, i, arr){
        if (!$("[id='"+item+"']")[0].checkValidity() && invalid_values.indexOf(item) == -1){
            $("[id='"+item+"']").removeClass('input-custom').addClass('error_field')
            document.getElementById(item).setAttribute('data-original-title', "Invalid value");
            invalid_values.push(item)
        }
        else if (invalid_values.indexOf(item) == -1){
            $("[id='"+item+"']").removeClass('error_field').addClass('input-custom');
            $("[id='"+item+"']").attr('data-original-title', '');
        }
        document.getElementById(item).setAttribute('data-toggle', 'tooltip');
    })
    var bool_fields = fields.map(function(field){return $("[id='"+field+"']").val() >= 0 && invalid_values.indexOf(field) == -1})
    final.push(bool_fields.reduce(function(sum, current){return sum && current}, true))
    final.push(id)
    final.push(f)
    return final
}


function training_model(){
    $.ajax({
        type: "POST",
        url: '/training_model',
        beforeSend: setLoad(),
        success: function(response, status, xhr){
            if (response.redirect) {
                 window.location.href = response.redirect;
               }
            else{
                jsonDictionary = response;
                setMessage();
                if (!jsonDictionary['isTrain']){
                    $("#Train").prop("disabled",true);
                }
                lock_mode(jsonDictionary['single_mod'], jsonDictionary['multiple_mod']);
                hideLoad();
                $("#menu-single-descr-mode").removeClass('disabled');
                disableButtons(jsonDictionary);
                statInfo(jsonDictionary['statInfo']);
                categoricFieldsAJAX(jsonDictionary['categoric']);
                attributesAJAX(jsonDictionary['attributes'], Object.keys(jsonDictionary['categoric']));
                dynamicChart = updateDynamicPlot(dynamicChart, jsonDictionary['plot']['dynamic bugs']['dynamic bugs']);
                distributionChart = updateDistributionPlot(distributionChart, jsonDictionary);
                //$("#Reset").prop("disabled",true);
                setFileName();
                clearChartStorage();
                optimize_message(jsonDictionary['message']);
            }
        },
        error: function(error) {
            document.getElementById('message').innerHTML =  'error of training model';
            $('html, body').animate({scrollTop: 0}, 600);
            hideLoad();
                }
    })
}


function multiple_files(){
    var inputFile = document.getElementById('Choose').files;
    var mas = []
    for(var key in inputFile)
        mas.push(inputFile[key]['name'])
    $("#file-name").html(mas)
    }


function check_size_files(){
    var inputFile = document.getElementById('Choose').files;
    for(var key in inputFile){
        if(inputFile[key]['size'] > sessionStorage['file_size']){
            $("#file-name").html(inputFile[key]['name'] + ' size is bigger than maximum file size, maximum size is equal to '+sessionStorage['file_size']/(1000*1000)+' mb')
            hideLoad()
            return false
        }
    }
    /*
    if(inputFile['length'] > 0)
        setLoad();
    */
    }

for( var group in jsonDictionary['fields']){
    for(var el in jsonDictionary['fields'][group]){
        if(jsonDictionary['fields'][group][el]['type'] == 'date' || jsonDictionary['fields'][group][el]['type'] == 'number'){
            if (jsonDictionary['fields'][group][el]['type'] == 'date'){
                $("[id='"+el+0+"']").on("change", function(){
                    $(this).removeClass('error_field').addClass('input-custom');
                })

                $("[id='"+el+1+"']").on("change", function(){
                    $(this).removeClass('error_field').addClass('input-custom');
                })

                $("[id='"+el+0+"']").on("click", function(){
                    $(this).removeClass('error_field').addClass('input-custom');
                })

                $("[id='"+el+1+"']").on("click", function(){
                    $(this).removeClass('error_field').addClass('input-custom');
                })
            }

            $("[id='"+el+0+"']").on("input", function(){
                $(this).removeClass('error_field').addClass('input-custom');
            })

            $("[id='"+el+1+"']").on("input", function(){
                $(this).removeClass('error_field').addClass('input-custom');
            })
        }
        else{
            $("[id='"+el+"']").on("input", function(){
                $(this).removeClass('error_field').addClass('input-custom');
            })
        }
    }
}
    