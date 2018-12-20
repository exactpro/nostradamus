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

if('undefined'.localeCompare(jsonDictionary['username']) == 0){
    $('#username').html('unknown user');
}
else $('#username').html(jsonDictionary['username'])//;

$('#descr').val('');

if('undefined'.localeCompare(jsonDictionary['recom']) == 0){
    $('#recom').val('');
}
else $('#recom').val(jsonDictionary['recom']);

function setDisable(){
    $("#descr_btn").prop("disabled",true);
    $("#advice").addClass("disabledfilter");
    $("#Recommendations").addClass("disabledfilter");
    $("#Priority_Histogram").addClass("disabledfilter");
    $("#wontReject").addClass("disabledfilter");
    $("#wontRejectCanv").addClass("disabledfilter");
    $("#Area_Histogram").addClass("disabledfilter");
    $("#load").removeAttr("style").hide();
}
setDisable();

function resetDisable(){
    $("#descr_btn").prop("disabled",false);
    $("#advice").removeClass("disabledfilter");
    $("#Recommendations").removeClass("disabledfilter");
    $("#Priority_Histogram").removeClass("disabledfilter");
    $("#wontReject").removeClass("disabledfilter");
    $("#wontRejectCanv").removeClass("disabledfilter");
    $("#Area_Histogram").removeClass("disabledfilter");
    $("#load").removeClass("style").hide();
}

var priority_hist = document.getElementById('priority_hist').getContext('2d');
  var priority_hist_horiz_bar = new Chart(priority_hist, {
    type: 'horizontalBar',
    data: {
        labels: ['Critical','High','Medium','Low'],
        datasets: [{
                data: [0,0,0,0],
            backgroundColor:["rgba(255, 99, 132, 0.3)","rgba(255, 159, 64, 0.3)","rgba(54, 162, 235, 0.3)","rgba(201, 203, 207, 0.3)"],
            borderColor:["rgb(255, 99, 132)","rgb(255, 159, 64)","rgb(54, 162, 235)","rgb(201, 203, 207)"],
            borderWidth:1
        }]
    },
    options:{
        scales:{
            xAxes:[{
                ticks:{
                    beginAtZero:true,
                    max:1
                }
            }
                  ]
        },
        legend: {
            display: false
        },
        title: {
            display: true,
            text: '',
            fontSize: 18,
            fontStyle: 'normal'
        }
    }
  });

var ttr_hist = document.getElementById('ttr_hist').getContext('2d');
   var ttr_hist_bar = new Chart(ttr_hist, {
    type: 'bar',
    data: {
           labels: ['0-30','30-90','90-180','>180'],
           datasets: [{
                data: [0,0,0,0],
            backgroundColor:["rgba(201, 203, 207, 0.3)","rgba(54, 162, 235, 0.3)","rgba(255, 159, 64, 0.3)","rgba(255, 99, 132, 0.3)"],
            borderColor:["rgb(201, 203, 207)","rgb(54, 162, 235)","rgb(255, 159, 64)","rgb(255, 99, 132)"],
            borderWidth:1
        }]
    },
    options:{
        scales:{
            yAxes:[{
                ticks:{
                    beginAtZero:true,
                    max:1
                }
            }
                  ]
        },
        legend: {
            display: false
        },
        title: {
            display: true,
            text: '',
            fontSize: 18,
            fontStyle: 'normal'
        }
    }
  });

var wont_fix_hist = document.getElementById('wont_fix_hist').getContext('2d');
    var wont_fix_hist_pie = new Chart(wont_fix_hist, {
    type: 'doughnut',
    data: {
        labels: [0],
        datasets: [{
            data: [0],
            label: "Wont Fix Histogram",
            backgroundColor:["rgba(255, 99, 132, 0.3)","rgba(75, 192, 192, 0.2)"],
            borderColor:["rgb(255, 99, 132)","rgb(75, 192, 192)"],
            borderWidth:1
        }]
    },
    options: {
      title: {
            display: true,
            text: '',
            fontSize: 18,
            fontStyle: 'normal'
        },
      legend: {
        position: 'right'
      }
    }
});

var reject_hist = document.getElementById('reject_hist').getContext('2d');
    var reject_hist_pie = new Chart(reject_hist, {
    type: 'doughnut',
    data: {
        labels: [0],
        datasets: [{
            data: [0],
            label: "Reject Histogram",
            backgroundColor:["rgba(75, 192, 192, 0.2)","rgba(255, 99, 132, 0.3)"],
            borderColor:["rgb(75, 192, 192)","rgb(255, 99, 132)"],
            borderWidth:1
        }]
    },
    options: {
      title: {
            display: true,
            text: '',
            fontSize: 18,
            fontStyle: 'normal'
        },
      legend: {
        position: 'right'
      }
    }
});

var area_hist = document.getElementById('area_hist').getContext('2d');
   var area_hist_bar = new Chart(area_hist, {
    type: 'bar',
    data: {
        labels: [0],
        datasets: [{
            data: [0],
            backgroundColor:"rgba(54, 162, 235, 0.3)",
            borderColor:"rgb(54, 162, 235)",
            borderWidth:1
        }]
    },
    options:{
        scales:{
            yAxes:[{
                ticks:{
                    beginAtZero:true,
                    max:1
                }
            }
                  ]
        },
        legend: {
            display: false
        },
        title: {
            display: true,
            text: '',
            fontSize: 18,
            fontStyle: 'normal'
        }
    }
  });

$('#descr').change(function getResult(){
                       if(!$('#descr')[0].checkValidity()){
                            $('#predictionForm').find(':submit').click();
                            $("#descr_btn").prop("disabled",true);
                            return;
                            }
                       else{
                            $.ajax({
                                type: "POST",
                                url: '/result',
                                beforeSend: setLoad(),
                                data: $('#descr').serialize(),
                                success: function(response, status, xhr){
                                    var ct = xhr.getResponseHeader("content-type") || "";
                                    console.log(response);
                                    if (ct.indexOf('html') > -1)
                                        document.write(response);
                                    else {
                                         priority_hist_horiz_bar = updateChart(priority_hist_horiz_bar, response['prio']);
                                         console.log(response['ttr']);
                                         ttr_hist_bar = updateChart(ttr_hist_bar, response['ttr']);
                                         wont_fix_hist_pie = updateChart(wont_fix_hist_pie, response['wontfix']);
                                         reject_hist_pie = updateChart(reject_hist_pie, response['reject']);
                                         area_hist_bar = updateChart(area_hist_bar, response['areas']);
                                         $('#recom').val(response['recom']);
                                         resetDisable();
                                         hideLoad();
                                        }
                                    },
                                error: function(error) {
                                    $('#descr').val('error of dynamic prediction');
                                    $('html, body').animate({scrollTop: 0}, 600);
                                    hideLoad();
                                            }
                                });
                   }});

function updateChart(chart, response){
    chart.data.labels = Object.keys(response);
    chart.data.datasets[0].data = Object.values(response);
    chart.update();
    return chart;
}

function updateTTRChart(chart, response){
    var keys = [];
    var vals = [];
    for(key in response){
        console.log(key);
        console.log(response[key]);
        keys.push(key);
        vals.push(response[key]);
        };
    newKeys = [keys[0], keys[2], keys[1], keys[3]];
    newVals = [vals[0], vals[2], vals[1], vals[3]];
    chart.data.labels = newKeys;
    chart.data.datasets[0].data = newVals;
    chart.update();
    return chart;
}

function hideLoad() {
         $("#load").removeAttr("style").hide();
         $('#loadDiv').removeClass("disabledfilter");
      }
function setLoad() {
         $("#load").show();
         $('#loadDiv').addClass('disabledfilter');
         }

function validatePreSubmit(){
    return $('#us-priority')[0].checkValidity() && $('#descr')[0].checkValidity();
}
