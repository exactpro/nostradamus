/*******************************************************************************
* Copyright 2009-2018 Exactpro (Exactpro Systems Limited)
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

/*-- get data from HTML and parse this to dictionary --*/
var jsonFromHTML = document.getElementById("json").innerHTML;
var cleanJsonFromHTML1 = jsonFromHTML.replace(/"/g,'');
var cleanJsonFromHTML = cleanJsonFromHTML1.replace(/&#34;/g,'"');
var jsonDictionary = JSON.parse(cleanJsonFromHTML);
console.log(jsonDictionary);

/*-- put data from dictionary to HTML --*/
var user = document.getElementById('username');
    user.innerHTML = jsonDictionary['username'];
//--------------------------------------//



$("#Submit").prop("disabled",true);
$("#Save").prop("disabled",true);

$("#Choose").click(function () {
    $("#Submit").prop("disabled",false);
   });
if('file uploaded successfully'.localeCompare(jsonDictionary['message']) == 0){
    $("#Save").prop("disabled",false);
}
if('please use .csv file extension'.localeCompare(jsonDictionary['message']) == 0){
    $("#Save").prop("disabled",false);
}




function fix_plot(data){
    /*-- Wont FIX Hist --*/
    var wont_fix_hist = document.getElementById('wont_fix').getContext('2d');
    var wont_fix_hist_pie = new Chart(wont_fix_hist, {
    type: 'doughnut',
    data: {
        labels: Object.keys(data),
        datasets: [{
            data: Object.values(data),
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
        position: 'left'
      }
    }
});
}
function reject_plot(data){
    /*-- Reject Hist --*/
    var reject_hist = document.getElementById('reject').getContext('2d');
    var wont_fix_hist_pie = new Chart(reject_hist, {
    type: 'doughnut',
    data: {
        labels: Object.keys(data),
        datasets: [{
            data: Object.values(data),
            label: "Reject Histogram",
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
}

function ttr_plot(data){
        var ttr_hist = document.getElementById('ttr').getContext('2d');
        var ttr_hist_bar = new Chart(ttr_hist, {
         type: 'bar',
         data: {
                labels: ['0-30','30-90','90-180','>180'],
                datasets: [{
                     data: [data['0-30'],data['30-90'],data['90-180'],data['&gt;180']],
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
                         max:100
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
}

function chartRouter(){
    var plot = jsonDictionary['plot'];
    if('undefined'.localeCompare(plot) != 0){
        ttr_plot(plot['ttr']);
        fix_plot(plot['wontfix']);
        reject_plot(plot['reject']);
    }
    if('undefined'.localeCompare(plot) == 0){
       fix_plot({'Fix': 50, 'Wont Fix': 50});
       reject_plot({'Reject': 50, 'Not reject': 50});
       ttr_plot({'&gt;180': 50, '90-180': 50, '30-90': 50, '0-30': 50})
    }
}

chartRouter();

//-------------------------------------------------------------------------------------------//


var idMessage = document.getElementById('message');

    if('undefined'.localeCompare(jsonDictionary['message']) == 0)
        idMessage.innerHTML = ''
    else
        idMessage.innerHTML = jsonDictionary['message'];

//-------------------------------------------------------------------------------------------//




function replace(val){
    if(val.match(/&gt;/g) != null){
       var newVal =  val.replace(/&gt;/g,'>');
       return newVal
        }
    if(val.match(/&lt;/g) != null){
       var newVal =  val.replace(/&lt;/g,'>');
       return newVal
        }
    else return val
}
//----------------------------------------------------------------//



function addRow(id , dict){
    var tbody = document.getElementById(id).getElementsByTagName("tbody")[0];
    for(key in dict){
        var mas = dict[key]
        var row = document.createElement("tr")
        var td = document.createElement("td")
        td.appendChild(document.createTextNode(key))
        row.appendChild(td);
        for(i=0;i<mas.length;i++){
            var td = document.createElement("TD")
            td.appendChild(document.createTextNode(replace(mas[i])))
            row.appendChild(td);
            }
        tbody.appendChild(row);
    }
  }

if('undefined'.localeCompare(jsonDictionary['table']) != 0)
        addRow('table', jsonDictionary['table']);

//---------------------------------------------------------------------------//

//--------------------------- -----------------------------------------//


var main = function() { 
    $('.icon-menu').click(function() { 
        $('.menu').animate({ 
            right: '-35px' 
        }, 200); 
    });



    $('.icon-close').click(function() { 
        $('.menu').animate({ 
            right: '-350px' 
        }, 200); 
    });
};

$(document).ready(main); 

//----------------------------------------------------------------------------------------//



function closeSave() {
       document.getElementById('Close').click();
   };

//-------------------------------------------------------------------------------------------------------------------//
