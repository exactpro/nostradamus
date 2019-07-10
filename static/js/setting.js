/*******************************************************************************
* Copyright 2016-2019 Exactpro (Exactpro Systems Limited)
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
// jsonDictionary is global variable which is used and overriding in many functions
var jsonDictionary = JSON.parse(cleanJsonFromHTML);
console.log(jsonDictionary);


hideLoad()


if('undefined'.localeCompare(jsonDictionary['error']) != 0){
    optimize_message(jsonDictionary['error']);
    }


function optimize_message(message){
    var array = message.split(" ");

    var arrays = [], size = 6;
    while (array.length > 0)
        arrays.push(array.splice(0, size).join(" "));

    var files = ''
    for(var key in Object.keys(arrays))
        files = files + arrays[key] + '\n'
    var text = $("#warning").text(files)
    text.html(text.html().replace(/\n/g,'<br/>'));
}

/*Tooltips*/
$('#i_mandatory_fields').tooltip({
    title : 'Section with mandatory fields settings. These fields must be presented in the uploaded file. It is immutable setting',
    placement: 'top'
});
$('#i_special_fields').tooltip({
    title : 'Section with special fields settings - additional fields that added for user needs. It is mutable setting',
    placement: 'top'
});
$('#i_refering_to').tooltip({
    title : 'Significance top settings. Choose values for building significance top',
    placement: 'top'
});
$('#i_resolution_settings_for_sm').tooltip({
    title : 'It is setting for single mode. You need to set only two resolutions: \nXML Element Name - field from XML file \nValue - resolution value for XML field',
    placement: 'top'
});
$('#i_table_settings_for_mm').tooltip({
    title : 'Mandatory fields for multiple mode',
    placement: 'top'
});


function data_type_tooltip(cell){
    switch(cell.getValue()){
        case 'text': return 'string type, with full line search'
        case 'text1': return 'string type, with substring search'
        case 'text2': return 'string type, with multiple substring search'
        case 'number': return 'float type, with full match search'
        case 'date': return 'date type, with full match search'
        case 'categorical': return 'string type, with isin search'
        case 'bool': return 'boolean type, with full match search'
        
    }
}


function mandatory_fields_table(data){
        return new Tabulator('#mandatory_fields', {
        data: data['mandatory_fields'],
        height:"311px",
        layout: 'fitColumns',
        columns: [
            { title: 'GUI name', field: 'gui_name' },
            { title: 'XML name', field: 'xml_name' },
            { title: 'type', field: 'type', 
                tooltip:function(cell){
                    switch(cell.getValue()){
                        case 'text': return 'string type, with full line search'
                        case 'text1': return 'string type, with substring search'
                        case 'text2': return 'string type, with multiple substring search'
                        case 'number': return 'float type, with full match search'
                        case 'date': return 'date type, with full match search'
                        case 'categorical': return 'string type, with isin search'
                        case 'bool': return 'boolean type, with full match search'
            }
        } }
        ]
    });
}

var mandatory_fields = mandatory_fields_table(jsonDictionary)



        //column definition in the columns array
        

function special_fields_table(data){
        return new Tabulator('#special_fields', {
        layout: 'fitColumns',
        //pagination: 'local',
        //paginationSize: 4,
        addRowPos:"bottom",
        columns: [
            {formatter:'buttonCross', width:40, align:"center",sorter:"string", headerSort:false, cellClick:function(e, cell){cell.getRow().delete()}},
            { title: 'GUI name', field: 'gui_name', editor:true, validator:["required", "regex:[a-zA-Z]+"]},
            { title: 'XML name', field: 'xml_name', editor:true, validator:["required", "maxLength:30"] },           
            { title: 'type', field: 'type', editor:"select", editorParams:{values:jsonDictionary['data_types']}, validator: "required",
                tooltip:function(cell){
                    switch(cell.getValue()){
                        case 'text': return 'string type, with full line search'
                        case 'text1': return 'string type, with substring search'
                        case 'text2': return 'string type, with multiple substring search'
                        case 'number': return 'float type, with full match search'
                        case 'date': return 'date type, with full match search'
                        case 'categorical': return 'string type, with isin search'
                        case 'bool': return 'boolean type, with full match search'
                }
            }}
        ]
        });
}
var special_fields = special_fields_table(jsonDictionary)


function get_data(){
    return Object.assign({}, {'mandatory_fields': JSON.stringify(mandatory_fields.getData())},
                             {'special_fields': JSON.stringify(special_fields.getData())}, 
                                {'referring_to': $('#referring_to').val(),
                                'resolution1name': $('#resolution1name').val(),
                                'resolution1value': $('#resolution1value').val(),
                                'resolution2name': $('#resolution2name').val(),
                                'resolution2value': $('#resolution2value').val(),
                                'multiple_mod_fields': $('#multiple_mod_fields').val()}) 
}


$("#add_row").click(function(){
    special_fields.addRow({})
});


$(document).ready(function() {
    $('#referring_to').select2({width:'50%'});
});


// add categorical fields
for(i=0;i<jsonDictionary['referring_to'].length;i++){
    $("[id='referring_to']").append($("<option></option>").attr("value",jsonDictionary['referring_to'][i]).text(jsonDictionary['referring_to'][i]));
}


// AJAX for sent setting data
$('#submit_settings').click(function significanceTop() {
    if(!checkValidation()){
        $('#setting_form').find(':submit').click();
        return;
        }
    $.ajax({
            type: "POST",
            url: '/set_config',
            beforeSend: setLoad(),
            data: get_data(),
            success: function(response, status, xhr){
                hideLoad();
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
                            $("#menu-multiple-descr-mode").addClass('disabled');
                            $("#menu-single-descr-mode").addClass('disabled');
                            $("#menu-analysis-train-link").addClass('disabled');
                        }
                        //lock_mode(response['single_mod'], response['multiple_mod'])
                        //set_data(response['data'])
                        }
                    }
                }            
        })})


function checkValidation(){
    var inputs = document.getElementsByTagName('input');
    var fields = []
    for (index = 0; index < inputs.length; ++index) {
        fields.push(inputs[index])
    }
    var bool_fields = fields.map(function(field){return field.checkValidity()})
    return bool_fields.reduce(function(sum, current){return sum && current}, true)
}


function hideLoad(){
    $("#load").removeAttr("style").hide();
    $('#loadDiv').removeClass("disabledfilter");
}


function setLoad(){
    $("#load").show();
    $('#loadDiv').addClass('disabledfilter');
    }


function set_data(data){
    for(el in data){
        if(el == 'special_fields'){
            for (index = 0; index < data['special_fields'].length; ++index)
                special_fields.addRow(Object.assign({}, replaceForCategoric(data['special_fields'][index])))
            continue;
        }
        if(el == 'resolution'){
            // if one resolution and mas of values that
            if(Object.keys(data['resolution']).length == 1){
                $('#resolution1name').val(replaceForCategoric(Object.keys(data['resolution'])[0]))
                $('#resolution2name').val(replaceForCategoric(Object.keys(data['resolution'])[0]))
                $('#resolution1value').val(replaceForCategoric(data['resolution'][Object.keys(data['resolution'])[0]][0]))
                $('#resolution2value').val(replaceForCategoric(data['resolution'][Object.keys(data['resolution'])[0]][1]))
            }
            // if two resolution with one value
            else{
                var count = 1
                for(el in data['resolution']){
                    $('#resolution'+count+'name').val(replaceForCategoric(el))
                    $('#resolution'+count+'value').val(replaceForCategoric(data['resolution'][el]))
                    count = count + 1
                }
            }
            continue;
        }
        if(Array.isArray(data[el])){
            $("[id='"+el+"']").val(replaceForCategoric(data[el])).trigger('change')
            continue;
        }
        
        else
            $("[id='"+el+"']").val(replaceForCategoric(data[el]))
        
        }
    }
    

set_data(jsonDictionary['config_data'])


function replaceForCategoric(val){
    if(Array.isArray(val))
        return val.map(function(field){return replaceForCategoric(field)})
    // check that val is dictionary
    
    if(typeof val==='object' && val!==null && !(val instanceof Array) && !(val instanceof Date)){
        var row = val
        Object.keys(row).map(function(key, index) {
            key = replaceForCategoric(key)
            row[key] = replaceForCategoric(row[key])
            });
        return row
    }
    //use toString() for case when val not str
    return val.replace(new RegExp('&amp;', 'g'),'&').replace(new RegExp('&gt;', 'g'),'>').replace(new RegExp('&lt;', 'g'),'<').replace(new RegExp('&lt;=', 'g'),'<=').replace(new RegExp('&gt;=', 'g'),'>=').replace(new RegExp('&gt;=', 'g'),'>=').replace(new RegExp("&#39;", 'g'),"'");
}


function lock_mode(single_mad, multiple_mod){
    if(single_mad == true)
        $("#menu-single-descr-mode").removeClass('disabled');
    
    if(multiple_mod == true)
        $("#menu-multiple-descr-mode").removeClass('disabled');
}


if('undefined'.localeCompare(jsonDictionary['single_mod']) != 0 && 'undefined'.localeCompare(jsonDictionary['multiple_mod']) != 0){
    lock_mode(jsonDictionary['single_mod'], jsonDictionary['multiple_mod'])
    $("#menu-analysis-train-link").removeClass('disabled');
}
