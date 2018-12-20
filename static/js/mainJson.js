/*******************************************************************************
* Copyright 2016-2018 Exactpro (Exactpro Systems Limited)
* 
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
* 
*     http://www.apache.org/licenses/LICENSE-2.0
* 
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
******************************************************************************/

var jsonFromHTML = document.getElementById("json").innerHTML;
var cleanJsonFromHTML1 = jsonFromHTML.replace(/"/g,'');
var cleanJsonFromHTML = cleanJsonFromHTML1.replace(/&#34;/g,'"');
var jsonDictionary = JSON.parse(cleanJsonFromHTML);

var successMas = [
                 'file uploaded successfully',
                 'data filtered',
                 'filter dropped',
                 'file saved',
                 'chart builded']

function setMessage(){
    var idMessage = document.getElementById('message');
    idMessage.innerHTML = '';
    if('undefined'.localeCompare(jsonDictionary['message']) != 0)
        idMessage.innerHTML = jsonDictionary['message'];
    if('undefined'.localeCompare(jsonDictionary['plot']) != 0)
        if(jsonDictionary['plot']['dynamic bugs'] == 'error'){
            idMessage.innerHTML = 'CUMULATIVE CHART OF DEFECT SUBMISSION: dataset is small for this period ';
            document.getElementById('period').value = '1 weak';
            $('html, body').animate({scrollTop: 0}, 600);
            }
    if(!successMas.includes(jsonDictionary['message']))
        $('html, body').animate({scrollTop: 0}, 600);

    }
setMessage();

sessionStorage['markup'] = 'no';
setTrain();
$("#Submit").prop("disabled",false);
$("#Apply").prop("disabled",true);
$("#Train").prop("disabled",true);
$("#Save").prop("disabled",true);
$("#Reset").prop("disabled",true);
$("#Build").prop("disabled",true);
$("#murkup").prop("disabled",false);
$("#attributes-block").addClass("disabledfilter");
$("#distrChart").addClass("disabledfilter");
$("#statInfoBlock").addClass("disabledfilter");
$("#dynamicChartBlock").addClass("disabledfilter");
$("#topTerm").addClass('disabledfilter');
$("#load").removeAttr("style").hide();
$("#areasDiv").addClass('disabledfilter');

function checkSingleMod(){
if(jsonDictionary['singleMod']==true){
    $("#menu-single-descr-mode").removeClass('disabled');
    }
    }
checkSingleMod();

function disableButtons(jsonDictionary){
    if('file uploaded successfully'.localeCompare(jsonDictionary['message']) == 0){
        $("#Apply").prop("disabled",false);
        $("#Build").prop("disabled",false);
        $("#Save").prop("disabled",false);
        //$("#Train").prop("disabled",false);
        $("#attributes-block").removeClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#statInfoBlock").removeClass("disabledfilter");
        $("#dynamicChartBlock").removeClass("disabledfilter");
        $("#topTerm").removeClass('disabledfilter');
    }
    if('data filtered'.localeCompare(jsonDictionary['message']) == 0){
        $("#Apply").prop("disabled",false);
        $("#Build").prop("disabled",false);
        $("#Save").prop("disabled",false);
        $("#Reset").prop("disabled",false);
        //$("#Train").prop("disabled",false);
        $("#attributes-block").removeClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#statInfoBlock").removeClass("disabledfilter");
        $("#dynamicChartBlock").removeClass("disabledfilter");
        $("#topTerm").removeClass('disabledfilter');
    }
    if('filter dropped'.localeCompare(jsonDictionary['message']) == 0){
        $("#Apply").prop("disabled",false);
        $("#Build").prop("disabled",false);
        $("#Save").prop("disabled",false);
        $("#Reset").prop("disabled",true);
        //$("#Train").prop("disabled",false);
        $("#attributes-block").removeClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#statInfoBlock").removeClass("disabledfilter");
        $("#dynamicChartBlock").removeClass("disabledfilter");
        $("#topTerm").removeClass('disabledfilter');
    }
    if('file saved'.localeCompare(jsonDictionary['message']) == 0){
        $("#Apply").prop("disabled",false);
        $("#Build").prop("disabled",false);
        $("#Save").prop("disabled",false);
        $("#Reset").prop("disabled",false);
        //$("#Train").prop("disabled",false);
        $("#attributes-block").removeClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#statInfoBlock").removeClass("disabledfilter");
        $("#dynamicChartBlock").removeClass("disabledfilter");
        $("#topTerm").removeClass('disabledfilter');
    }
    if('chart builded'.localeCompare(jsonDictionary['message']) == 0){
        $("#Apply").prop("disabled",false);
        $("#Build").prop("disabled",false);
        $("#Save").prop("disabled",false);
        $("#Reset").prop("disabled",false);
        //$("#Train").prop("disabled",false);
        $("#attributes-block").removeClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#statInfoBlock").removeClass("disabledfilter");
        $("#dynamicChartBlock").removeClass("disabledfilter");
        $("#topTerm").removeClass('disabledfilter');
    }
    if('there are no rows corresponding to the condition'.localeCompare(jsonDictionary['message']) == 0){
        $("#Apply").prop("disabled",false);
        $("#Build").prop("disabled",false);
        $("#Save").prop("disabled",false);
        //$("#Train").prop("disabled",false);
        $("#attributes-block").removeClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#statInfoBlock").removeClass("disabledfilter");
        $("#dynamicChartBlock").removeClass("disabledfilter");
        $("#topTerm").removeClass('disabledfilter');
        $("#filterForm")[0].reset();
    }
    if('please use .csv file extension'.localeCompare(jsonDictionary['message']) == 0){
        $("#Apply").prop("disabled",false);
        $("#Build").prop("disabled",false);
        $("#Save").prop("disabled",false);
        $("#Reset").prop("disabled",false);
        //$("#Train").prop("disabled",false);
        $("#attributes-block").removeClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#statInfoBlock").removeClass("disabledfilter");
        $("#dynamicChartBlock").removeClass("disabledfilter");
        $("#topTerm").removeClass('disabledfilter');
    }
    if('incorrect file format. Please use only xml'.localeCompare(jsonDictionary['message']) == 0){
        $("#Submit").prop("disabled",false);
        $("#Apply").prop("disabled",true);
        $("#Save").prop("disabled",true);
        $("#Reset").prop("disabled",true);
        $("#Build").prop("disabled",true);
        $("#murkup").prop("disabled",true);
        //$("#Train").prop("disabled",true);
        $("#attributes-block").addClass("disabledfilter");
        $("#distrChart").addClass("disabledfilter");
        $("#statInfoBlock").addClass("disabledfilter");
        $("#dynamicChartBlock").addClass("disabledfilter");
        $("#topTerm").addClass('disabledfilter');
    }
    if('please use Xmax and StepSize value in the array [0,maxValue from stat info]'.localeCompare(jsonDictionary['message']) == 0){
        $("#Apply").prop("disabled",false);
        $("#Build").prop("disabled",false);
        $("#Save").prop("disabled",false);
        $("#Reset").prop("disabled",false);
        //$("#Train").prop("disabled",false);
        $("#attributes-block").removeClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#statInfoBlock").removeClass("disabledfilter");
        $("#dynamicChartBlock").removeClass("disabledfilter");
        $("#topTerm").removeClass('disabledfilter');
    }
    if('incorrect value for Xmax or StepSize'.localeCompare(jsonDictionary['message']) == 0){
        $("#Apply").prop("disabled",false);
        $("#Build").prop("disabled",false);
        $("#Save").prop("disabled",false);
        $("#Reset").prop("disabled",false);
        //$("#Train").prop("disabled",false);
        $("#attributes-block").removeClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#statInfoBlock").removeClass("disabledfilter");
        $("#dynamicChartBlock").removeClass("disabledfilter");
        $("#topTerm").removeClass('disabledfilter');
    }
    if('you are cannot to build frequency density chart for data with one value'.localeCompare(jsonDictionary['message']) == 0){
        $("#Apply").prop("disabled",false);
        $("#Build").prop("disabled",false);
        $("#Save").prop("disabled",false);
        $("#Reset").prop("disabled",false);
        //$("#Train").prop("disabled",false);
        $("#attributes-block").removeClass("disabledfilter");
        $("#distrChart").removeClass("disabledfilter");
        $("#statInfoBlock").removeClass("disabledfilter");
        $("#dynamicChartBlock").removeClass("disabledfilter");
        $("#topTerm").removeClass('disabledfilter');
    }
}
disableButtons(jsonDictionary);

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

function setStepSize(stepSize){
    if(stepSize == ''){
        return null;
    }
    else return parseInt(stepSize);
}

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
                            type:'linear',
                            position:'bottom',

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
                                                          type:'linear',
                                                          position:'bottom',

                                                          }
                                                         ]
                                                      },
                                                        elements: { point: { radius: 1 } }
                                                  }
                                              });
                                              return myChart;
                              }

function chooseThickness(type){
    if('undefined'.localeCompare(sessionStorage[type]) == 0 || sessionStorage[type] == '')
        return 1;
    else return sessionStorage[type];
}

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

                            },{}
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
                                    ticks:{
                                           stepSize: setStepSizeY(yLine, 0),
                                           beginAtZero:true
                                           }
                                    }],
                            xAxes:[{
                            type:'linear',
                            position:'bottom',
                                ticks:{
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
                            yAxes:[{
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

function get_line_thickness(){
    if($("#y").find(":selected").text() == 'Relative Frequency'){
        if($("#DistributionThickness").val() == ''){
            sessionStorage["relative"] = '';
        }else{
            sessionStorage["relative"] = $("#DistributionThickness").val();
        }
    }
    if($("#y").find(":selected").text() == 'Frequency density'){
            if($("#DistributionThickness").val() == ''){
                sessionStorage["density"] = '';
            }else{
                sessionStorage["density"] = $("#DistributionThickness").val();
            }
        }
    if($("#LineWidthPeriod").val() == ''){
                    sessionStorage["dynamic"] = '';
                }
    else{
        sessionStorage["dynamic"] = $("#LineWidthPeriod").val();
        }
}

$('#period').change(function ajaxDynamic() {
    $.ajax({
            type: "POST",
            url: get_periodAJAX('/buildChart/onlyDynamic/'),
            beforeSend: setLoad(),
            success: function(response, status, xhr){
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
                    },
            error: function(error) {
                document.getElementById('message').innerHTML = 'error dynamic plotting of charts';
                $('html, body').animate({scrollTop: 0}, 600);
                hideLoad();
                        }
            });
                    })

function ajaxXDistribution() {
    $.ajax({
            type: "POST",
            url: '/buildChart/onlyDistribution/',
            data: $('#distrChart').serialize(),
            beforeSend: setLoad(),
            success: function(response, status, xhr){
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
                    },
            error: function(error) {
                document.getElementById('message').innerHTML = 'error dynamic plotting of charts';
                $('html, body').animate({scrollTop: 0}, 600);
                hideLoad();
                        }
            });
                    }

$('#x').change(function(){ajaxXDistribution()})
$('#y').change(function(){ajaxXDistribution()})
$('#scale').change(function(){ajaxXDistribution()})
$('#stepSize').change(function(){ajaxXDistribution()})

function redraw(block,id){
 $('#'+id).remove();
 $('#'+block).after("<canvas id="+id+"></canvas>");
}

function updateDynamicPlot(dynamicChart, jsonDictionary){
    get_line_thickness();
    dynamicChart.data.labels = jsonDictionary[0];
    dynamicChart.data.datasets[0].data = jsonDictionary[1];
    dynamicChart.options.scales.yAxes[0].ticks.stepSize = setStepSizeY(jsonDictionary[1], 0);
    dynamicChart.update();
    return dynamicChart;
}

function updateDistributionPlot(distributionChart, jsonDictionary){
    get_line_thickness();
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
            distributionChart.data.datasets[1].labels = jsonDictionary['plot']['Frequency density']['histogram'][0];
            distributionChart.data.datasets[1].data = plot(jsonDictionary['plot']['Frequency density']['histogram'][0],jsonDictionary['plot']['Frequency density']['histogram'][1]);
            distributionChart.data.datasets[1].steppedLine = true;
            distributionChart.data.datasets[1].borderColor = ["rgb(54, 162, 235)"];
            distributionChart.data.datasets[1].backgroundColor = ["rgba(54, 162, 235, 0.3)"];
            distributionChart.data.datasets[1].borderWidth = chooseThickness('density');
            distributionChart.options.scales.yAxes[0].ticks.stepSize = setStepSizeY(jsonDictionary['plot']['Frequency density']['line'][1], jsonDictionary['plot']['Frequency density']['histogram'][1]);
            distributionChart.options.scales.xAxes[0].ticks.max = findMax(jsonDictionary['plot']['Frequency density']['line'][0], jsonDictionary['plot']['Frequency density']['histogram'][0], jsonDictionary['plot']['scale']);
            distributionChart.options.scales.xAxes[0].ticks.stepSize = setStepSize(jsonDictionary['plot']['stepSize']);
            distributionChart.options.elements.point.radius = 0.5;
            distributionChart.update();
            return distributionChart;
        }
        }
}

$('#LineWidthPeriod').change(function(){
    if($('#LineWidthPeriod')[0].checkValidity() == false){
        $('#dynamicChart').find(':submit').click();}
    else{
        get_line_thickness();
        dynamicChart.data.datasets[0].borderWidth = chooseThickness('dynamic');
        dynamicChart.update();
    }})
$('#DistributionThickness').change(function(){
    if($('#DistributionThickness')[0].checkValidity() == false){
        $('#distrChart').find(':submit').click();}
    else{
        get_line_thickness();
        if($("#y").find(":selected").text() == 'Relative Frequency'){
            distributionChart.data.datasets[0].borderWidth = chooseThickness('relative');
            distributionChart.update();}
        else {
            distributionChart.data.datasets[0].borderWidth = chooseThickness('density');
            distributionChart.data.datasets[1].borderWidth = chooseThickness('density');
            distributionChart.update();
            }
        }
    })

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

function addOption(name, mas){
    var trigger = 0;
    for(i=0;i<mas.length;i++){
        if(mas[i] != 'null'){
            trigger = 1;
            $(name).append($("<option></option>").attr("value",(replaceForCategoric(mas[i]))).text((replaceForCategoric(mas[i]))));
            }
    }
    if(trigger == 0){
        document.getElementById('DEV_resolution').style.display = 'none';
    }
}

function forEach(mas){
    for(key in mas){
        addOption('#'+key,mas[key]);
    }
}

function categoricFields(jsonDictionary){
    var categorical = jsonDictionary;
    forEach(categorical);
}

if('undefined'.localeCompare(jsonDictionary['categoric']) != 0)
        categoricFields(jsonDictionary['categoric']);

function addOptionAJAX(name, mas){
    var trigger = 0;
    for(i=0;i<mas.length;i++){
        if(mas[i] != 'null'){
            trigger = 1;
            $(name).append($("<option></option>").attr("value",(replaceForCategoric(mas[i]))).text((replaceForCategoric(mas[i]))));
            }
    }
    if(trigger == 0){
        document.getElementById('DEV_resolution').style.display = 'none';
    }
}

function forEachAJAX(mas){
    for(key in mas){
        if(key == 'ReferringTo')
            $('#ReferringTo').find('option').remove().end();
        else removeOptionsAJAX(document.getElementById(key));
        addOptionAJAX('#'+key,mas[key]);
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
    return val.replace('&gt;','>').replace('&lt;','<').replace('&lt;=','<=').replace('&gt;=','>=').replace('&gt;=','>=').replace("&#39;","'");
}

function attributes(attrib){
    var attributes = attrib;
    for(key in attributes){
          if(key == 'Issue_key')
            var issue_key = document.getElementById('Issue_key1').value = attributes[key]
          if(key == 'Summary')
            var issue_key = document.getElementById('Summary').value = attributes[key]
          if(key == 'Components')
                  var issue_key = document.getElementById('Components').value = attributes[key]
          if(key == 'Labels')
            var issue_key = document.getElementById('Labels').value = attributes[key]
          if(key == 'Description')
            var issue_key = document.getElementById('Description').value = attributes[key]
          if(key == 'Status'){
            var issue_key = document.getElementById('Status').value = attributes[key]
            }
          if(key == 'Project_name')
            var issue_key = document.getElementById('Project_name').value = attributes[key]
          if(key == 'Priority')
            var issue_key = document.getElementById('Priority').value = attributes[key]
          if(key == 'Resolution')
            var issue_key = document.getElementById('Resolution').value = attributes[key]
          if(key == 'Comments1')
            var issue_key = document.getElementById('Comments1').value = replace(attributes[key])
          if(key == 'Comments2')
            var issue_key = document.getElementById('Comments_start').value = attributes[key]
          if(key == 'Comments3')
            var issue_key = document.getElementById('Comments3').value = replace(attributes[key])
          if(key == 'Comments4')
            var issue_key = document.getElementById('Comments_end').value = attributes[key]
          if(key == 'Attachments1')
            var issue_key = document.getElementById('Attachments1').value = replace(attributes[key])
          if(key == 'Attachments2')
            var issue_key = document.getElementById('Attachments_start').value = attributes[key]
          if(key == 'Attachments3')
            var issue_key = document.getElementById('Attachments3').value = replace(attributes[key])
          if(key == 'Attachments4')
            var issue_key = document.getElementById('Attachments_end').value = attributes[key]
          if(key == 'DEV_resolution')
            var issue_key = document.getElementById('DEV_resolution').value = attributes[key]
          if(key == 'Date_created1')
            var issue_key = document.getElementById('Date_created1').value = replace(attributes[key])
          if(key == 'Date_created2')
            var issue_key = document.getElementById('Date_created_start').value = attributes[key]
          if(key == 'Date_created3')
            var issue_key = document.getElementById('Date_created3').value = replace(attributes[key])
          if(key == 'Date_created4')
            var issue_key = document.getElementById('Date_created_end').value = attributes[key]
          if(key == 'Date_resolved1')
            var issue_key = document.getElementById('Date_resolved1').value = replace(attributes[key])
          if(key == 'Date_resolved2')
            var issue_key = document.getElementById('Date_resolved_start').value = attributes[key]
          if(key == 'Date_resolved3')
            var issue_key = document.getElementById('Date_resolved3').value = replace(attributes[key])
          if(key == 'Date_resolved4')
            var issue_key = document.getElementById('Date_resolved_end').value = attributes[key]
          if(key == 'TTR1')
            var issue_key = document.getElementById('TTR1').value = replace(attributes[key])
          if(key == 'TTR2')
            var issue_key = document.getElementById('TTR_start').value = attributes[key]
          if(key == 'TTR3')
            var issue_key = document.getElementById('TTR3').value = replace(attributes[key])
          if(key == 'TTR4')
            var issue_key = document.getElementById('TTR_end').value = attributes[key]
          if(key == 'Version')
            var issue_key = document.getElementById('Version').value = attributes[key]
          if(key == 'SignificanceTop')
            $("#significanceTop").html(attributes[key].join());
          if(key == 'ReferringTo')
            $('#ReferringTo').val((replaceForCategoric(attrib[key])));
          if(key == 'freqTop'){
            sessionStorage['moreFreq'] = 0;
            $('#moreFreq').prop('disabled', false);
            setTopFreq();
          }
          }
    if($("#y").find(":selected").text() == 'Relative Frequency'){
        if('undefined'.localeCompare(sessionStorage["relative"]) == 0)
            document.getElementById('DistributionThickness').value = '1'
        else
            document.getElementById('DistributionThickness').value = sessionStorage["relative"];}
    else{
        if('undefined'.localeCompare(sessionStorage["density"]) == 0)
            document.getElementById('DistributionThickness').value = '1'
        else
            document.getElementById('DistributionThickness').value = sessionStorage["density"];
    }
    if('undefined'.localeCompare(sessionStorage["dynamic"]) == 0)
        $("#LineWidthPeriod").val("1").change();
    else
        $("#LineWidthPeriod").val(sessionStorage["dynamic"]).change();
}

function attributesAJAX(attrib){
    for(key in attrib){
        if(key == 'Status')
            $('#Status').val(attrib[key]);
        if(key == 'Project_name')
            $('#Project_name').val(attrib[key]);
        if(key == 'Priority')
            $('#Priority').val((attrib[key]));
        if(key == 'Resolution')
            $('#Resolution').val(attrib[key]);
        if(key == 'SignificanceTop')
            $('#SignificanceTop').val(attrib[key]);
        if(key == 'ReferringTo'){
            $('#ReferringTo').val((replaceForCategoric(attrib[key])));
            }
        if(key == 'freqTop'){
          sessionStorage['moreFreq'] = 0;
          $('#moreFreq').prop('disabled', false);
          setTopFreq();
                  }}
    $("#period").val('1 week');
    $("#LineWidthPeriod").val('1');
    $("#DistributionThickness").val('1');
    $("#y").val('Relative Frequency');
    $("#x").val('ttr');

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

function setTopFreq(){
    $("#freqTop").html((jsonDictionary['attributes']['freqTop'].slice(0, parseInt(sessionStorage['moreFreq'], 10)+20).join()));
    sessionStorage['moreFreq'] = parseInt(sessionStorage['moreFreq'], 10) + 20;
    if(parseInt(sessionStorage['moreFreq'], 10) == 100){
        $('#moreFreq').prop('disabled', true);
        $("#Reset").prop("disabled",false);
        }
}

function closeSave() {
       document.getElementById('Close').click();
   };

      $( function() {
        $( "#Date_created_start" ).datepicker({
            dateFormat:"dd-mm-yy",
            beforeShow:function(input,inst) {
                $('#'+inst.id).datepicker("option","maxDate",$("#Date_created_end").val());
            }
        });
          $( "#Date_created_end" ).datepicker({
              dateFormat:"dd-mm-yy",
              beforeShow:function(input,inst) {
                $('#'+inst.id).datepicker("option","minDate",$("#Date_created_start").val());
            }
          });
          $( "#Date_resolved_start" ).datepicker({
            dateFormat:"dd-mm-yy",
             beforeShow:function(input,inst) {
                  $('#'+inst.id).datepicker("option","maxDate",$("#Date_resolved_end").val());
            }
        });
          $( "#Date_resolved_end" ).datepicker({
            dateFormat:"dd-mm-yy",
              beforeShow:function(input,inst) {
                      $('#'+inst.id).datepicker("option","minDate",$("#Date_resolved_start").val());
            }
        });
          $("#Choose").change(function () {
              var fPath = $(this).val();
              var slashPos = fPath.lastIndexOf("\\");
              sessionStorage["fName"] = fPath.slice(slashPos+1);
              $("#file-name").html(sessionStorage["fName"]);
              $("#message").html('');
          })
      } );

function setFileName(){
    if(sessionStorage["finalName"] != ''){
        $("#file-name").html(sessionStorage["finalName"]);
    }
    else $("#file-name").html(sessionStorage["fName"]);
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
                         var ct = xhr.getResponseHeader("content-type") || "";
                         if (ct.indexOf('html') > -1){
                            document.write(response);
                            }
                         else{
                            var blob = new Blob([response]);
                            var link = document.createElement('a');
                            link.href = window.URL.createObjectURL(blob);
                            link.download = $('#FileName').val();
                            link.click();
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
                                     var ct = xhr.getResponseHeader("content-type") || "";
                                     if (ct.indexOf('html') > -1)
                                        document.write(response);
                                     else {
                                       $("#significanceTop").html(response['SignificanceTop'].join());
                                       hideLoad();
                                       setFileName();
                                       }
                                     },
                                 error: function(error) {
                                     document.getElementById('message').innerHTML = 'error dynamic plotting of significance top';
                                     $('html, body').animate({scrollTop: 0}, 600);
                                     hideLoad();
                                             }
                                 });
                                         })

function filtering() {
    if(!(checkComAtTt() && checkValidation())){
        $('#filterForm').find(':submit').click();
        return;
        }
    $.ajax({
         type: "POST",
         url: '/filtering?ReferringTo='+$('#ReferringTo').val(),
         beforeSend: setLoad(),
         data: $('#filterForm').serialize(),
         success: function(response, status, xhr){
             var ct = xhr.getResponseHeader("content-type") || "";
             if (ct.indexOf('html') > -1)
                document.write(response);
             else {
               jsonDictionary = response;
               console.log(jsonDictionary);
               setMessage();
               disableButtons(jsonDictionary);
               statInfo(jsonDictionary['statInfo']);
               categoricFieldsAJAX(jsonDictionary['categoric']);
               attributesAJAX(jsonDictionary['attributes']);
               dynamicChart = updateDynamicPlot(dynamicChart, jsonDictionary['plot']['dynamic bugs']['dynamic bugs']);
               distributionChart = updateDistributionPlot(distributionChart, jsonDictionary);
               $("#Reset").prop("disabled",false);
               hideLoad();
               setFileName();
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
             var ct = xhr.getResponseHeader("content-type") || "";
             if (ct.indexOf('html') > -1)
                document.write(response);
             else {
               jsonDictionary = response;
               setMessage();
               disableButtons(jsonDictionary);
               statInfo(jsonDictionary['statInfo']);
               categoricFieldsAJAX(jsonDictionary['categoric']);
               attributesAJAX(jsonDictionary['attributes']);
               dynamicChart = updateDynamicPlot(dynamicChart, jsonDictionary['plot']['dynamic bugs']['dynamic bugs']);
               distributionChart = updateDistributionPlot(distributionChart, jsonDictionary);
               hideLoad();
               setFileName();
             }
                 },
         error: function(error) {
             document.getElementById('message').innerHTML = 'error of dynamic reset filter';
             $('html, body').animate({scrollTop: 0}, 600);
             hideLoad();
                     }
         });
                 }

function hideLoad() {
         $("#load").removeAttr("style").hide();
         $('#loadDiv').removeClass("disabledfilter");
      }
function setLoad() {
         $("#load").show();
         $('#loadDiv').addClass('disabledfilter');
         }

function checkValidation(){
    return ($('#Issue_key1')[0].checkValidity() && $('#Components')[0].checkValidity() && $('#Labels')[0].checkValidity() && $('#Version')[0].checkValidity() && $('#Date_created_start')[0].checkValidity() && $('#Date_created_end')[0].checkValidity() && $('#Date_resolved_start')[0].checkValidity() && $('#Date_resolved_end')[0].checkValidity());
}

function validateForLoadFile(){
    if($('#Choose')[0].checkValidity() == false || $('#areas')[0].checkValidity() == false)return;
    setLoad();
}

function checkComAtTt(){
    if($('#Comments_start').val() != '' && ($('#Comments_start').val() > 1000 || $('#Comments_start').val() < 0)) return false;
    if($('#Comments_end').val() != '' && ($('#Comments_end').val() > 1000 || $('#Comments_end').val() < 0)) return false;
    if($('#Attachments_start').val() != '' && ($('#Attachments_start').val() > 1000 || $('#Attachments_start').val() < 0)) return false;
    if($('#Attachments_end').val() != '' && ($('#Attachments_end').val() > 1000 || $('#Attachments_end').val() < 0)) return false;
    if($('#TTR_start').val() != '' && ($('#TTR_start').val() > 4000 || $('#TTR_start').val() < 0)) return false;
    if($('#TTR_end').val() != '' && ($('#TTR_end').val() > 4000 || $('#TTR_end').val() < 0)) return false;
    return true;
}

$('#murkup').change(function setAreas(){
    if($('#murkup').val()=='yes'){
        $("#areasDiv").removeClass('disabledfilter');
        $("#areas").prop('required',true);
        sessionStorage['markup'] = $('#murkup').val();
        setTrain();
        }
    else {
        $("#areasDiv").addClass('disabledfilter');
        $("#areas").prop('required',false);
        sessionStorage['markup'] = $('#murkup').val();
        setTrain();
    }
})

function setTrain(){
    if(sessionStorage['markup'] == 'yes')
        $("#Train").prop("disabled",false);
    else $("#Train").prop("disabled",true);
}

function trainingModel(){
    $.ajax({
        type: "POST",
        url: '/trainingModel',
        beforeSend: setLoad(),
        success: function(response, status, xhr){
            jsonDictionary = response;
            setMessage();
            hideLoad();
            checkSingleMod();
        },
        error: function(error) {
            document.getElementById('message').innerHTML =  'error of training model';
            $('html, body').animate({scrollTop: 0}, 600);
            hideLoad();
                }
    })
}
