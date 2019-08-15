/*-- get data from HTML and parse this to dictionary --*/
var jsonFromHTML = document.getElementById("json").innerHTML;
var cleanJsonFromHTML1 = jsonFromHTML.replace(/"/g,'');
var cleanJsonFromHTML = cleanJsonFromHTML1.replace(/&#34;/g,'"');
var jsonDictionary = JSON.parse(cleanJsonFromHTML);


// open murkup only if inner == 0
// if version is OS disable settings mod if version is inner
if('undefined'.localeCompare(jsonDictionary['inner']) != 0){
    if(jsonDictionary['inner'] == '1'){
        $("#setting").addClass('disabledfilter');

    }
}


// set default name for resolution charts
$('#resolution1').text('resolution1 Pie Chart')
$('#resolution2').text('resolution2 Pie Chart')
hideLoad()

/*-- put data from dictionary to HTML --*/
var user = document.getElementById('username');
    user.innerHTML = jsonDictionary['username'];
//--------------------------------------//

$("#Submit").prop("disabled",true);
$("#Save").prop("disabled",true);
$("#save").prop("disabled",true);
$("#Priority_Histogram").addClass("disabledfilter");
$("#resolution2").addClass("disabledfilter");
$("#resolution22").addClass("disabledfilter");
$("#resolution1").addClass("disabledfilter");
$("#resolution11").addClass("disabledfilter");
$("#area_hist1").addClass("disabledfilter");
$("#ttr_hist1").addClass("disabledfilter");

$("#Choose").click(function () {
    $("#Submit").prop("disabled",false);
   });
if('file uploaded successfully'.localeCompare(jsonDictionary['message']) == 0){
    $("#save").prop("disabled",false);
    $("#Priority_Histogram").removeClass("disabledfilter");
    $("#resolution2").removeClass("disabledfilter");
    $("#resolution22").removeClass("disabledfilter");
    $("#resolution1").removeClass("disabledfilter");
    $("#resolution11").removeClass("disabledfilter");
    $("#area_hist1").removeClass("disabledfilter");
    $("#ttr_hist1").removeClass("disabledfilter");
}


  /*-- TTR Histogram --*/
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
                scaleLabel: {
                   display: true,
                   labelString: 'probability'
                         },
                ticks:{
                    beginAtZero:true,
                    max:100
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
var wont_fix_hist = document.getElementById('resolution1').getContext('2d');
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
var reject_hist = document.getElementById('resolution2').getContext('2d');
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
                    max:100
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


//-------------------------------------------------------------------------------------------//

var idMessage = document.getElementById('message');

    if('undefined'.localeCompare(jsonDictionary['message']) == 0)
        idMessage.innerHTML = ''
    else
        optimize_message(jsonDictionary['message']);


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

//-------------------------------------------------------------------------------------------//


/*-- clear dict --*/
function replace(val){
    if(Array.isArray(val))
        var val = val.join()
    return val.toString().replace(new RegExp('&amp;', 'g'),'&').replace(new RegExp('&gt;', 'g'),'>').replace(new RegExp('&lt;', 'g'),'<').replace(new RegExp('&lt;=', 'g'),'<=').replace(new RegExp('&gt;=', 'g'),'>=').replace(new RegExp('&gt;=', 'g'),'>=').replace(new RegExp("&#39;", 'g'),"'");
}


//----------------------------------------------------------------//

/*-- create table --*/

function add_tabble(id , dict){
    var test = Object.keys(dict[Object.keys(dict)[0]])
    // insert head
    var tbody = document.getElementById(id).getElementsByTagName("tbody")[0];
    var row = document.createElement("tr")
    var td = document.createElement("th")
    td.appendChild(document.createTextNode('Issue_key'))
    row.appendChild(td);
    for(i=0;i<test.length;i++){
        var td = document.createElement("TH")
        td.appendChild(document.createTextNode(replace([test[i]])))
        row.appendChild(td)
    }
    tbody.appendChild(row);
    // insert rows
    for(key in dict){
        var row_dict = dict[key]
        var row = document.createElement("tr")
        var td = document.createElement("td")
        td.appendChild(document.createTextNode(key))
        row.appendChild(td);
        for(i=0;i<test.length;i++){
            var td = document.createElement("TD")
            td.appendChild(document.createTextNode(replace(row_dict[test[i]])))
            row.appendChild(td);
        }
        tbody.appendChild(row);
    }
  }

if('undefined'.localeCompare(jsonDictionary['table']) != 0)
        add_tabble('table', jsonDictionary['table']);

//---------------------------------------------------------------------------//

function closeSave() {
       document.getElementById('Close').click();
   };


if('undefined'.localeCompare(jsonDictionary['plot']) != 0){
    plot_charts()
    }


function plot_charts(){
    for (var el in jsonDictionary['plot']){
        if (el == 'ttr')
            ttr_hist_bar = updateChart(ttr_hist_bar, jsonDictionary['plot'][el]);
        if (el == 'area_of_testing')
            area_hist_bar = updateChart(area_hist_bar, jsonDictionary['plot'][el]);
        if (el == 'resolution_pie'){
            wont_fix_hist_pie = updateChart(wont_fix_hist_pie, jsonDictionary['plot'][el][Object.keys(jsonDictionary['plot'][el])[0]]);
            $('#resolution11').text(replaceForCategoric(Object.keys(jsonDictionary['plot']['resolution_pie'])[0] + ' Pie Chart'))
            reject_hist_pie = updateChart(reject_hist_pie, jsonDictionary['plot'][el][Object.keys(jsonDictionary['plot'][el])[1]]);
            $('#resolution22').text(replaceForCategoric(Object.keys(jsonDictionary['plot'][el])[1] + ' Pie Chart'))
        }
    }
}


function updateChart(chart, response){
    chart.data.labels = Object.keys(response).map(function(el){return replace(el);});
    chart.data.datasets[0].data = Object.values(response);
    chart.update();
    return chart;
}


// loading process
function hideLoad() {
         $("#load").removeAttr("style").hide();
         $('#loadDiv').removeClass("disabledfilter");
      }
function setLoad() {
         $("#load").show();
         $('#loadDiv').addClass('disabledfilter');
         }


function saveFile() {
    $('#FileName').val($('#FileName')[0].value.trim())
    if($('#FileName')[0].checkValidity() == false){
            $('#saveForm').find(':submit').click();}
    else{
    $.ajax({
            type: "POST",
            url: '/save_multiple_subset',
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
                                var blob = new Blob([response]);
                                var link = document.createElement('a');
                                link.href = window.URL.createObjectURL(blob);
                                link.download = $('#FileName').val();
                                link.click();
                                hideLoad();
                               }
                           }
                         },
            complete:
                function(jqXHR, textStatus){
                    var ct = jqXHR.getResponseHeader("content-type") || "";
                    if (textStatus == 'success' && ct.indexOf('html') == -1){
                        delTempFiles();
                        // setFileName();
                        hideLoad();
                        }
                    },
            error: function(response, error) {
                optimize_message('error of saving file');
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
                    optimize_message('error of deleting temp files');
                    $('html, body').animate({scrollTop: 0}, 600);
                    hideLoad();
                        }
                });
                        }


function validateForLoadFile(){
    if($('#Choose')[0].checkValidity() == false)return;
    setLoad();
}


// del data from sessionStorage after logout
function clearFileNameLocalStorage() {
            sessionStorage.removeItem("fName");
            sessionStorage.removeItem("finalName");
          };


// set name of file
$("#Choose").change(function () {
      var fPath = $(this).val();
      var slashPos = fPath.lastIndexOf("\\");
      sessionStorage["fName"] = fPath.slice(slashPos+1);
      $("#file-name").html(sessionStorage["fName"]);
      $("#message").html('');
})


// if we submit data that set finalName
function setFinalFileNameLocalStorage() {
        sessionStorage["finalName"] =  sessionStorage["fName"]
      };


function setFileName(){
    if(sessionStorage["finalName"] != ''){
        $("#file-name").html(sessionStorage["finalName"]);
    }
    else $("#file-name").html(sessionStorage["fName"]);
    $('#Choose').val('');
}
setFileName();


// unlock single mod and multiple mod for open source version
if(jsonDictionary['single_mod'] == true)
    $("#menu-single-descr-mode").removeClass('disabled');

if(jsonDictionary['multiple_mod'] == true)
    $("#menu-multiple-descr-mode").removeClass('disabled');


function replaceForCategoric(val){
    if(Array.isArray(val))
            var val = val.join()
    //use toString() for case when val not str
    return val.toString().replace(new RegExp('&amp;', 'g'),'&').replace(new RegExp('&gt;', 'g'),'>').replace(new RegExp('&lt;', 'g'),'<').replace(new RegExp('&lt;=', 'g'),'<=').replace(new RegExp('&gt;=', 'g'),'>=').replace(new RegExp('&gt;=', 'g'),'>=').replace(new RegExp("&#39;", 'g'),"'");
}


// set max file size
sessionStorage['file_size'] = jsonDictionary['file_size']

function check_size_files(){
    var inputFile = document.getElementById('Choose').files;
    for(var key in inputFile){
        if(inputFile[key]['size'] > sessionStorage['file_size']){
            $("#file-name").html(inputFile[key]['name'] + ' size is bigger than maximum file size, maximum size is equal to '+sessionStorage['file_size']/(1000*1000)+' mb')
            return false
        }
    }
    if(inputFile['length'] > 0)
        setLoad();
    }