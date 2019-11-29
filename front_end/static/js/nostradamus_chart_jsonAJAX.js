/*-- get data from HTML and parse this to dictionary --*/
var jsonFromHTML = document.getElementById("json").innerHTML;
var cleanJsonFromHTML1 = jsonFromHTML.replace(/"/g,'');
var cleanJsonFromHTML = cleanJsonFromHTML1.replace(/&#34;/g,'"');
var jsonDictionary = JSON.parse(cleanJsonFromHTML);


// set default name for resolution chartsF
$('#resolution1').text('resolution1 Pie Chart')
$('#resolution2').text('resolution2 Pie Chart')


function optimize_message(message){
    var array = message.split(" ");

    var arrays = [], size = 6;
    while (array.length > 0)
        arrays.push(array.splice(0, size).join(" "));

    var files = ''
    for(var key in Object.keys(arrays))
        files = files + arrays[key] + '\n'
    var text = $("#warning").text(files);
    //text.html(text.html().replace(/\n/g,'<br/>'));
}

function ResetFilters() {
    var dropDownResolution = document.getElementById("Resolution");
    var dropDownPriority = document.getElementById("Priority");
    var dropDownTesting_areas = document.getElementById("Testing_areas");
    dropDownResolution.selectedIndex = 0;
    dropDownPriority.selectedIndex = 0;
    dropDownTesting_areas.selectedIndex = 0;
    //dropDownResolution.va
    //$('#descr').highlightWithinTextarea({highlight: null});
    $("#warning").html('');
    //$('select.highlight').change();
}

/*-- put data from dictionary to HTML --*/
if('undefined'.localeCompare(jsonDictionary['username']) == 0){
    $('#username').html('unknown user');
}
else $('#username').html(jsonDictionary['username'])//;

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
    $("#highlight_div").addClass("disabledfilter");
    $("#load").removeAttr("style").hide();
}
setDisable();

function resetDisable(inner){
    $("#descr_btn").prop("disabled",false);
    $("#advice").removeClass("disabledfilter");
    $("#Recommendations").removeClass("disabledfilter");
    $("#Priority_Histogram").removeClass("disabledfilter");
    $("#wontReject").removeClass("disabledfilter");
    $("#wontRejectCanv").removeClass("disabledfilter");
    $("#Area_Histogram").removeClass("disabledfilter");
    $("#highlight_div").removeClass("disabledfilter");
    $("#load").removeClass("style").hide();
    if(inner == '0'){
        $("#labPrior").addClass("disabledfilter");
        $("#descr_btn").addClass("disabledfilter");
        }
}

  /*-- Priority Histogram --*/
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

           xAxes: [{
                 scaleLabel: {
                   display: true,
                   labelString: 'probability'
                 },
                 ticks: {
                   autoSkip: false,
                   autoSkipPadding: 20
                 }
               }],
           yAxes: [{
                    scaleLabel: {
                      display: true,
                      labelString: 'priority'
                    }
                  }]

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

  /*-- TTR Histogram --*/
var ttr_hist = document.getElementById('ttr_hist').getContext('2d');
   var ttr_hist_bar = new Chart(ttr_hist, {
    type: 'bar',
    data: {
           labels: ['0-30','31-90','91-180','>180'],
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
                scaleLabel: {
                           display: true,
                           labelString: 'probability'
                                 },
                ticks:{
                    beginAtZero:true,
                    max:1
                }
            }
                  ],
                  xAxes: [{
                       scaleLabel: {
                              display: true,
                              labelString: 'days range'
                                    },
                       ticks: {
                         autoSkip: false,
                         autoSkipPadding: 20
                       }
                     }]
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

    /*-- Wont FIX Hist --*/
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
    /*-- Reject Hist --*/
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
    /*-- Area Histogram --*/
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
                scaleLabel: {
                       display: true,
                       labelString: 'probability'
                             },
                ticks:{
                    beginAtZero:true,
                    max:1
                }
            }
                  ],
                  xAxes: [{
                       scaleLabel: {
                              display: true,
                              labelString: 'area'
                                    },
                       ticks: {
                         autoSkip: false,
                         autoSkipPadding: 20
                       }
                     }]
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


function predict(){
    if(!$('#descr')[0].checkValidity()){
        $('#predictionForm').find(':submit').click();
        $("#descr_btn").prop("disabled",true);
        return;
    }
    else{
    $.ajax({
        type: "POST",
        url: '/single_description_mode/predict',
        beforeSend: setLoad(),
        data: $('#descr').serialize(),
        success: function(response, status, xhr){
            if (response.redirect) {
                window.location.href = response.redirect;
            }
            else{
                var ct = xhr.getResponseHeader("content-type") || "";
                if (ct.indexOf('html') > -1){
                    document.write(response);
                }
                else {
                    if('undefined'.localeCompare(response['error']) != 0){
                        optimize_message(response['error']);
                        hideLoad();
                        setDisable()
                    }
                    else{
                        if('undefined'.localeCompare(response['prio']) != 0)
                            priority_hist_horiz_bar = updateChart(priority_hist_horiz_bar, response['prio']);
                        if('undefined'.localeCompare(response['ttr']) != 0)
                            ttr_hist_bar = updateChart(ttr_hist_bar, response['ttr']);
                        //wont_fix_hist_pie = updateChart(wont_fix_hist_pie, response['wontfix']);
                        //reject_hist_pie = updateChart(reject_hist_pie, response['reject']);
                        if('undefined'.localeCompare(response['resolution_pie']) != 0){
                            wont_fix_hist_pie = updateChart(wont_fix_hist_pie, response['resolution_pie'][Object.keys(response['resolution_pie'])[0]]);
                            $('#resolution1').text(replaceForCategoric(Object.keys(response['resolution_pie'])[0]+' Pie Chart'))
                            reject_hist_pie = updateChart(reject_hist_pie, response['resolution_pie'][Object.keys(response['resolution_pie'])[1]]);
                            $('#resolution2').text(replaceForCategoric(Object.keys(response['resolution_pie'])[1]+' Pie Chart'))
                        }
                        if('undefined'.localeCompare(response['areas']) != 0)
                            area_hist_bar = updateChart(area_hist_bar, response['areas']);
                        if('undefined'.localeCompare(response['recom']) != 0)
                            $('#recom').val(response['recom']);
                        resetDisable(0);
                        if('undefined'.localeCompare(response['single_mod']) != 0 && 'undefined'.localeCompare(response['multiple_mod']) != 0)
                            lock_mode(response['single_mod'], response['multiple_mod'])
                        if('undefined'.localeCompare(response['descr']) != 0)
                            $('#descr').val(response['descr']);
                        hideLoad();

                    }
                }
            }
            /*$("#descr").removeClass("hwt-content");
            $("#descr").removeClass("hwt-input");*/
        },
        error: function(error) {
        $('#descr').val('error of dynamic prediction');
        $('html, body').animate({scrollTop: 0}, 600);
        hideLoad();
        }
    });
}};


function updateChart(chart, response){
    chart.data.labels = Object.keys(response);
    chart.data.datasets[0].data = Object.values(response);
    chart.update();
    return chart;
}



$('select.highlight').on("change", function selectHighlightChange(){
    $.ajax({
        type: "POST",
        url: '/single_description_mode/highlight',
        beforeSend: setLoad(),
        data: 'field=' + $(this).serialize() + '&descr=' + $('#descr').val(),
        success: function(response, status, xhr){
            if (response.redirect) {
                window.location.href = response.redirect;
            }
            else{
                var ct = xhr.getResponseHeader("content-type") || "";
                if (ct.indexOf('html') > -1)
                    document.write(response);
                else {
                    if('undefined'.localeCompare(response['error']) != 0){
                            optimize_message(response['error']);
                            hideLoad();
                            }
                    else{
                        highlight_terms(response['highlight_terms'])
                        $('html, body').animate({scrollTop: 0}, 600);
                        hideLoad();
                    }
                    }
            }
            },
        error: function(error) {
            $('#descr').val('error of highlighting of terms for '+field);
            $('html, body').animate({scrollTop: 0}, 600);
            hideLoad();
                    }
        });
        });





// processing animation
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


// unlock single mod and multiple mod for open source version
function lock_mode(single_mad, multiple_mod){
    if(single_mad == true)
        $("#menu-single-descr-mode").removeClass('disabled');

    if(multiple_mod == true)
        $("#menu-multiple-descr-mode").removeClass('disabled');
}
lock_mode(jsonDictionary['single_mod'], jsonDictionary['multiple_mod'])


// add caregoriv fields
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
    $('#us-priority').find('option').remove();
    addOption("[id=us-priority]",mas['Priority']);
}

function categoricFields(jsonDictionary){
    forEach(jsonDictionary);
}


function replaceForCategoric(val){
    if(Array.isArray(val))
            var val = val.join()
    //use toString() for case when val not str
    return val.toString().replace(new RegExp('&amp;', 'g'),'&').replace(new RegExp('&gt;', 'g'),'>').replace(new RegExp('&lt;', 'g'),'<').replace(new RegExp('&lt;=', 'g'),'<=').replace(new RegExp('&gt;=', 'g'),'>=').replace(new RegExp('&gt;=', 'g'),'>=').replace(new RegExp("&#39;", 'g'),"'");
}

categoricFields(jsonDictionary['categoric'])

var highlight = []
// highlight terms
function highlight_terms(data){
    var colors = {'Resolution':'red', 'Testing_areas':'blue', 'Priority':'yellow'}
    if(data['terms'].length == 0){
        for(var i=0;i<highlight.length;i++){
            if(highlight[i]['className'] == colors[data['field']['name']]){
                highlight.splice(i, 1)
                i--;
            }
        }
        }
    else{
        if(highlight.length == 0){
            for (var i = 0; i< data['terms'].length; i++){
                highlight[i] = {'highlight': new RegExp('\\b('+data['terms'][i]+')', 'gmi'),
                                'className': colors[data['field']['name']]
                                }
            }
        }
        else{
            for(var i=0;i<highlight.length;i++){
                if(highlight[i]['className'] == colors[data['field']['name']]){
                    for (var i = 0; i< data['terms'].length; i++){
                        highlight.push({'highlight': new RegExp('\\b('+data['terms'][i]+')', 'gmi'),
                                        'className': colors[data['field']['name']]
                                        })
                    }
                    $('#descr').highlightWithinTextarea({
                                                        highlight: highlight
                                                            });
                    return;
                }
            }

                for (var i = 0; i< data['terms'].length; i++){
                    highlight.push({'highlight': new RegExp('\\b('+data['terms'][i]+')', 'gmi'),
                                    'className': colors[data['field']['name']]
                                    })
                }
            }
        }
    $('#descr').highlightWithinTextarea({
                                         highlight: highlight
                                             });
    }


function clearSingleDescriptionModePage(){
    location.reload()
}


$('#descr').on("input", function(){
    ResetFilters()
    priority_hist_horiz_bar.data.datasets[0].data = [0,0,0,0];
    priority_hist_horiz_bar.update()
    ttr_hist_bar.data.datasets[0].data = [0,0,0,0];
    ttr_hist_bar.update()
    wont_fix_hist_pie.data.datasets[0].data = [0];
    wont_fix_hist_pie.update();
    $('#resolution1').text(null)
    reject_hist_pie.data.datasets[0].data = [0];
    reject_hist_pie.update()
    $('#resolution2').text(null)
    area_hist_bar.data.datasets[0].data = [0,0,0,0];
    area_hist_bar.update()
    $('#recom').val("");
    $('#descr').highlightWithinTextarea('destroy');
    setDisable();
})

