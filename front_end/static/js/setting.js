/*-- get data from HTML and parse this to dictionary --*/
var jsonFromHTML = document.getElementById("json").innerHTML;
var cleanJsonFromHTML1 = jsonFromHTML.replace(/"/g,'');
var cleanJsonFromHTML = cleanJsonFromHTML1.replace(/&#34;/g,'"');
// jsonDictionary is global variable which is used and overriding in many functions
var jsonDictionary = JSON.parse(cleanJsonFromHTML);
var form_data = new FormData()

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
    text.html(text.html().replace(/"/g, ''));
    text.html(text.html().replace('&amp;#39;', "'"));
    text.html(text.html().replace('&amp;#39;', "'"));
    text.html(text.html().replace(/^(?:')/, ""));
    text.html(text.html().replace(/(?:'<br>)$/, ""));
}

/*Tooltips*/
$('#i_mandatory_fields').tooltip({
    title : 'Defect attributes which have to be presented in uploaded file(s). Immutable section.',
    placement: 'top'
});
$('#i_special_fields').tooltip({
    title : 'Additional defect attributes.',
    placement: 'top'
});
$('#i_refering_to').tooltip({
    title : 'Significance top elements.',
    placement: 'top'
});
$('#i_resolution_settings_for_sm').tooltip({
    title : 'Defect resolutions those values are used to build Pie Charts based on specified values. Takes only one value for each Resolution.',
    placement: 'top'
});
$('#i_table_settings_for_mm').tooltip({
    title : 'Predictions table mandatory elements on Multiple Description Mode.',
    placement: 'top'
});
$('#i_area_of_testing_fields').tooltip({
    title : 'Mark up settings.',
    placement: 'top'
});


$('#referring_to').select2({width:'100%'});
$('#logging_level').select2({width:'100%'});

// Disable default action on ENTER keypress
document.addEventListener('keypress', function(event) {
    if (event.keyCode == 13) {
        event.preventDefault();
    }
});

function data_type_tooltip(cell){
    switch(cell.getValue()){
        case 'String': return 'string type, full string search'
        case 'Substring': return 'string type, substring search'
        case 'Substring_array': return 'string type, exact match of all array elements'
        case 'Numeric': return 'float type, exact match'
        case 'Date': return 'date type, exact match'
        case 'Categorical': return 'string type, isin search'
        case 'Boolean': return 'boolean type, exact match'
        
    }
}

function convert_fields(defect_attributes){
    result = []
    for (field in defect_attributes){
        if (field != 'ttr'){
            result.push({"gui_name": defect_attributes[field]["name"], "xml_name": field, "type":defect_attributes[field]["type"]})
        }
    }
    return result
}

function convert_area_fields(defect_attributes){
    result = []
    for (field in defect_attributes){
        if (field != 'Other'){
            result.push(defect_attributes[field])
        }
    }
    return result
}

function mandatory_fields_table(data){
        return new Tabulator('#mandatory_attributes', {
        data: convert_fields(data['config_data']['mandatory_attributes']),
        height:"311px",
        layout: 'fitColumns',
        columns: [
            { title: 'GUI name', field: 'gui_name' },
            { title: 'XML name', field: 'xml_name' },
            { title: 'type', field: 'type', 
                tooltip:function(cell){
                    switch(cell.getValue()){
                        case 'String': return 'string type, full string search'
                        case 'Substring': return 'string type, substring search'
                        case 'Substring_array': return 'string type, exact match of all array elements'
                        case 'Numeric': return 'float type, exact match'
                        case 'Date': return 'date type, exact match'
                        case 'Categorical': return 'string type, isin search'
                        case 'Boolean': return 'boolean type, exact match'
            }
        } }
        ]
    });
}

var mandatory_fields = mandatory_fields_table(jsonDictionary)


function multiple_mod_fields_table(data){
        return new Tabulator('#multiple_mode_attributes', {
        data: getDataMultipleModFields(data['config_data']['multiple_mode_attributes']),
        layout: 'fitColumns',
        width: "50%",
        columns: [{ title: 'GUI name', field: 'gui_name' }]

    });
}


function getDataMultipleModFields(multiple_mode_fields){
    table_multiple_mod_fields = []
    if (multiple_mode_fields){
        var i = 0
        multiple_mode_fields.forEach(function(item_mm){
            table_multiple_mod_fields[i] = {}
            table_multiple_mod_fields[i]['gui_name'] = item_mm;
            table_multiple_mod_fields[i]['1'] = 1; // tabulator works with only 2 values
            i++;
        })
    }
    return table_multiple_mod_fields
}


var multiple_mode_fields = multiple_mod_fields_table(jsonDictionary)

var validateTabulator = function (value){
    if (value)
        return true
    else
        return false
}

function areaOfTestingTable(data){
    return new Tabulator('#mark_up_attributes', {
        layout: 'fitColumns',
        addRowPos:"bottom",
        data: convert_area_fields(data['config_data']['mark_up_attributes']),
        columns: [
            { formatter:'buttonCross', width:40, align:"center",sorter:"string", headerSort:false, cellClick:function(e, cell){cell.getRow().delete()}},
            { title: 'Name', field: 'gui_name', editable:true, editor:"input"},
            { formatter: function(cell, formatterParams, onRendered){
                onRendered(function(){
                    tag = $(cell.getElement()).find('textarea').tagify({duplicates:true, delimiters: "\\|"})
                    function addTag(){
                        var result = ""
                        $(cell.getElement()).find('tag').each(function(i, item){
                            result += item.textContent + '|'
                        })
                        result = result.split("|")
                        result.forEach(function(item, i, arr){
                            if (arr.lastIndexOf(item) != i)
                                arr.splice(i, 1)
                        })
                        result.splice(result.length-1, 1)
                        result = result.join("|")
                        cell.setValue(result)
                        tag = $(cell.getElement()).find('textarea').tagify({duplicates:true, delimiters: "\\|"})
                        $(cell.getElement()).find('tags').click()
                        tag.on('add', addTag)
                        cell.getRow().normalizeHeight();
                        $(cell.getElement()).find('tags').on("input", function(){cell.getRow().normalizeHeight();})
                        $(cell.getElement()).find('tags').on("change", function(){cell.getRow().normalizeHeight();})
                    }
                    tag.on('add', addTag)
                })
                if(cell.getValue()){
                    return '<textarea>'+cell.getValue()+'</textarea>'
                }
                else{
                    return '<textarea></textarea>'
                }
            }, title: 'Area of testing', field:'name', editor:true, variableHeight:true
        }]
    });
}

var area_of_testing_fields = areaOfTestingTable(jsonDictionary)

function convert_set_models(set_models){
    var result = []
    for (key in set_models){
        obj = {'name':key, 'is_choose':set_models[key]}
        result.push(obj)
    }
    return result
}

function export_models(name){
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        if (xhr.readyState == 4){
            if (xhr.status == 200){
                var arrayBuffer = xhr.response;
                var byteArray = new Uint8Array(arrayBuffer)
                var blob = new Blob([arrayBuffer], {type: "application/zip"});
                var link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.download = name+".zip"
                link.click();
                return
            }
            else if (xhr.status == 302){
                optimize_message("The model set has not been uploaded yet.");
                $('html, body').animate({scrollTop: 0}, 600);
            }
        }
    }
    xhr.open('POST', '/export_models');
    xhr.responseType = 'arraybuffer';
    xhr.send(name);  
}

function set_models_table(){
    return new Tabulator('#set_models', {
        layout: 'fitColumns',
        addRowPos:"bottom",
        data: convert_set_models(jsonDictionary['set_models']),
        columns: [
            { formatter:'buttonCross', width:40, align:"center",sorter:"string", headerSort:false, cellClick:function(e, cell){
                var files = form_data.getAll("file");
                var i = 0
                for (var i=0; i<files.length; i++){
                    if (files[i].filename == cell.getValue()){
                        break
                    }
                }
                if (i < files.length){
                    files.splice(i, 1);
                    form_data.delete("file[]");
                    $.each(files, function(i, v) {
                        form_data.append("file[]", v);
                    });
                }
                cell.getRow().delete()
            }},
            { title: 'Name', field: 'name', editable:false, editor:"input", formatter: function(cell, formatterParams, onRendered){
                var names = $('#set_models').find('[tabulator-field="name"]:not(:first)')
                if (names.length != 0){
                    for (var i=0; i<names.length; i++){
                        if (names[i].textContent == cell.getValue()){
                            $(names[i]).css("border", "1px solid red")
                            $(cell.getElement()).css("border", "1px solid red")
                        }
                    }
                }
                return cell.getValue()
            }},
            { title: 'Choose', field:'is_choose', headerSort:false, formatter: function(cell, formatterParams, onRendered){
                onRendered(function(){
                        //set the value of the radio buttons
                        if($(cell.getElement()).find('input').val()=='true'){
                            $(cell.getElement()).find('input').prop("checked", true);
                            form_data.delete('selected_models')
                            form_data.append('selected_models', cell.getRow().getCell("name").getValue());
                        }

                        $(cell.getElement()).find('input').on('click', function(e){
                            if($(this).val() == 'true'){
                                $(this).val('false')
                                $(this).prop('checked', false);
                            }
                            else{
                                $("#set_models").find("input[value='true']").val(false)
                                $(this).val(true)
                                $(this).prop('checked', true);
                                form_data.delete('selected_models')
                                form_data.append('selected_models', cell.getRow().getCell("name").getValue());
                            }
                        });
                    }
                )
                //create and style radio buttons
                var radio = $("<form style='margin-bottom:0;'><input name='rag-radio' type='radio' value='"+cell.getValue()+"'></form>");
            
                return radio.html();
            }, editable:true
        },
        {title: "Export", headerSort:false, formatter: function(cell, formatterParams, onRendered){
            var button = $("<form style='margin-bottom:0;'><button type='button' name='export' class='btn'>Export</button></form>")
            onRendered(function(){
                $(cell.getElement()).find('button').on("click", function(){
                    export_models(cell.getRow().getCell("name").getValue())
                })
            })
            return button.html()
        }}]
    });
}

function get_set_models(){
    var names = $('#set_models').find('[tabulator-field="name"]:not(:first)')
    var choose = $('#set_models').find('[tabulator-field="is_choose"]:not(:first)').find('input')
    var set_models = []
    var isCorrectSetModels = true
    for(var i=0; i<names.length; i++){
        if(names[i].textContent.trim() != ''){
            obj = {'name': names[i].textContent, 'choose':choose[i].value}
            set_models.push(obj)
        }
        else{
            if (names[i]){
                $(names[i]).css("border", "1px solid red")
                $(names[i]).on("input", function(){ 
                    $(this).css("border", "") 
                })
                isCorrectSetModels = false
            }
        }
    }
    if (isCorrectSetModels)
        if (set_models.length != 0)
            return set_models
        else
            return [{}]
    else return false
}

var set_models = set_models_table();

function getAreaOfTesting(){
    var gui_names = $('#mark_up_attributes').find('[tabulator-field="gui_name"]:not(:first)')
    var names = $('#mark_up_attributes').find('[tabulator-field="name"]:not(:first)')
    var areaOfTesting = [] 
    var isCorrectAreas = true
    for(var i=0; i<gui_names.length; i++){
        if(gui_names[i].textContent.trim() != ''){
            if (validateTabulator(gui_names[i].textContent)){
                var namesStr = collectTagsInString(i)
                if (namesStr != ''){
                    var isValid = true
                    namesStr.split("|").forEach(function(val, ind, arr){
                        if (!validateTabulator(val))
                            isValid = false
                    })
                    if(isValid){
                        obj = {'gui_name': gui_names[i].textContent, 'name':collectTagsInString(i)}
                        areaOfTesting.push(obj)
                    }
                    else{
                        $(names[i]).css("border", "1px solid red")
                        $(names[i]).on("input", function(){ 
                            $(this).css("border", "") 
                        })
                        isCorrectAreas = false
                    }
                }
                else{
                    $(names[i]).css("border", "1px solid red")
                    $(names[i]).on("input", function(){ 
                        $(this).css("border", "") 
                    })
                    isCorrectAreas = false
                }
            }
            else{
                $(gui_names[i]).css("border", "1px solid red")
                $(gui_names[i]).on("input", function(){ 
                    $(this).css("border", "") 
                })
                isCorrectAreas = false
            }
        }
        else{
            if (names[i]){
                $(gui_names[i]).css("border", "1px solid red")
                $(gui_names[i]).on("input", function(){ 
                    $(this).css("border", "") 
                })
                isCorrectAreas = false
            }
        }
    }
    if (isCorrectAreas)
        if (areaOfTesting.length != 0)
            return areaOfTesting
        else
            return [{}]
    else return false
}

function collectTagsInString(index){
    var result = ""
    var names = $('[tabulator-field="name"]:not(:first)').find('tags')
    $(names[index]).find('tag').each(function(index, item){
        result+=item.textContent+'|'
    })
    return result.slice(0, -1)
}

function special_fields_table(data){
        return new Tabulator('#special_attributes', {
        layout: 'fitColumns',
        data:convert_fields(data['config_data']['special_attributes']),
        //pagination: 'local',
        //paginationSize: 4,
        addRowPos:"bottom",
        columns: [
            {formatter:'buttonCross', width:40, align:"center",sorter:"string", headerSort:false, cellClick:function(e, cell){cell.getRow().delete()}},
            { title: 'GUI name', field: 'gui_name', editable:true, editor:"input"},
            { title: 'XML name', field: 'xml_name', editor:true},           
            { title: 'type', field: 'type', editor:"select", editorParams:{values:jsonDictionary['data_types']},
                tooltip:function(cell){
                    switch(cell.getValue()){
                        case 'String': return 'string type, full string search'
                        case 'Substring': return 'string type, substring search'
                        case 'Substring_array': return 'string type, exact match of all array elements'
                        case 'Numeric': return 'float type, exact match'
                        case 'Date': return 'date type, exact match'
                        case 'Categorical': return 'string type, isin search'
                        case 'Boolean': return 'boolean type, exact match'
                }
            }}
        ]
        });
}
var special_fields = special_fields_table(jsonDictionary)

function getSpecialFields(){
    var gui_names = $('#special_attributes').find('[tabulator-field="gui_name"]:not(:first)')
    var xml_names = $('#special_attributes').find('[tabulator-field="xml_name"]:not(:first)')
    var types = $('#special_attributes').find('[tabulator-field="type"]:not(:first)')
    var special = [] 
    var isCorrectSpecial = true
    for(var i=0; i<gui_names.length; i++){
        if(gui_names[i].textContent.trim() != ''){
            if (validateTabulator(gui_names[i].textContent)){
                if (xml_names[i].textContent.trim() != ''){
                    var isValid = true
                    if (!validateTabulator(xml_names[i].textContent))
                        isValid = false
                    if(isValid){
                        obj = {'gui_name': gui_names[i].textContent, 'xml_name':xml_names[i].textContent, "type":types[i].textContent}
                        special.push(obj)
                    }
                    else{
                        $(xml_names[i]).css("border", "1px solid red")
                        $(xml_names[i]).on("input", function(){ 
                            $(this).css("border", "") 
                        })
                        isCorrectSpecial = false
                    }
                }
                else{
                    $(xml_names[i]).css("border", "1px solid red")
                    $(xml_names[i]).on("input", function(){ 
                        $(this).css("border", "") 
                    })
                    isCorrectSpecial = false
                }
            }
            else{
                $(gui_names[i]).css("border", "1px solid red")
                $(gui_names[i]).on("input", function(){ 
                    $(this).css("border", "") 
                })
                isCorrectSpecial = false
            }
        }
        else{
            if (gui_names[i]){
                $(gui_names[i]).css("border", "1px solid red")
                    $(gui_names[i]).on("input", function(){ 
                        $(this).css("border", "") 
                    })
                    isCorrectSpecial = false
            }
        }
    }
    if (isCorrectSpecial)
        if (special.length != 0)
            return special
        else
            return [{}]
    else return false
}

function get_data(){
    return Object.assign({}, {'mandatory_attributes': JSON.stringify(mandatory_fields.getData())},
                             {'special_attributes': JSON.stringify(getSpecialFields())}, 
                             {'mark_up_attributes': JSON.stringify(getAreaOfTesting())},
                             {'set_models': JSON.stringify(set_models.getData())},
                                {'referring_to': $('#referring_to').val(),
                                'logging_level': $('#logging_level').val(),
                                'resolution1name': $('#resolution1name').val(),
                                'resolution1value': $('#resolution1value').val(),
                                'resolution2name': $('#resolution2name').val(),
                                'resolution2value': $('#resolution2value').val(),
                                'multiple_mode_attributes': jsonDictionary['config_data']['multiple_mode_attributes']})
}

$("#add_row").click(function(){
    special_fields.addRow({})
});

$("#add_row_areas").click(function(){
    area_of_testing_fields.addRow({})
});

$("#add_row_model").click(function(){
    $('#input_file').click();
});

$('#input_file').change(function(){
    var fPath = $(this).val();
    var slashPos = fPath.lastIndexOf("\\");
    var name = fPath.slice(slashPos+1).split('.')[0];
    if(name){
        set_models.addRow({name: name, is_choose: 'false'})
    }
    form_data.append("file[]", $(this)[0].files[$(this)[0].files.length-1])
});

$(document).ready(function() {
    $('#referring_to').select2({width:'100%'});
    $('#logging_level').select2({width:'100%'});
});


// add categorical fields
for(i=0;i<jsonDictionary['referring_to'].length;i++){
    $("[id='referring_to']").append($("<option></option>").attr("value",jsonDictionary['referring_to'][i]).text(jsonDictionary['referring_to'][i]));
}

for(i=0;i<jsonDictionary['logging_level'].length;i++){
    $("[id='logging_level']").append($("<option></option>").attr("value",jsonDictionary['logging_level'][i]).text(jsonDictionary['logging_level'][i]));
}


function is_null(fields){
    for (key in fields){
        if (fields[key] == null){
            return true
        }
    }
    return false
}

function checkResolution(){
     if ($('#resolution1name').val() == $('#resolution2name').val()){
         if ($('#resolution1value').val() == $('#resolution2value').val()){
             return false;
         }
     }
     return true;
}

function upload_models(){
    form_data.append("set_models", JSON.stringify(get_set_models()))
    $.ajax({
        type:'POST',
        url: '/upload_models',
        data: form_data,
        processData: false,
        contentType: false,
        success: function(response, status, xhr){
            if (response.redirect) {
                lock_mode(response.single_mod, response.multiple_mod)
                window.location = response.redirect;
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
                        $('html, body').animate({scrollTop: 0}, 600);
                    }
                }
                lock_mode(response['single_mod'], response['multiple_mod'])
            }
        }  
    })
}

// AJAX for sent setting data
$('#submit_settings').click(function significanceTop() {
    data = get_data()
    if(!checkValidation() || !getAreaOfTesting() || !getSpecialFields() || !checkResolution()){
        if (!getSpecialFields()){
            optimize_message("Please correctly fill in all required Special fields.")
            $('html, body').animate({scrollTop: 0}, 600);
            return
        }
        else if (!getAreaOfTesting()){
            optimize_message("Please correctly fill in all required Area of Testing fields.")
            $('html, body').animate({scrollTop: 0}, 600);
            return
        }else if (!checkResolution()){
            optimize_message("There are the same values in the first and in the second Resolution Pie Charts.")
            $('html, body').animate({scrollTop: 0}, 600);
            return
        }
        $('#setting_form').find(':submit').click();
        return;
    }
    $.ajax({
            type: "POST",
            url: '/set_config',
            beforeSend: setLoad(),
            data: data,
            success: function(response, status, xhr){
               hideLoad();
               var ct = xhr.getResponseHeader("content-type") || "";
                if (ct.indexOf('html') > -1)
                    document.write(response);
                else {
                    if('undefined'.localeCompare(response['error']) != 0){
                        optimize_message(response['error']);
                        $("#menu-multiple-descr-mode").addClass('disabled');
                        $("#menu-single-descr-mode").addClass('disabled');
                        $("#menu-analysis-train-link").addClass('disabled');
                        $('html, body').animate({scrollTop: 0}, 600);
                    }
                    //lock_mode(response['single_mod'], response['multiple_mod'])
                    //set_data(response['data'])
                    }
                    upload_models()
                }
                
        })})



$('#reset_settings').click(function resetSettings() {
    location.reload()    
});


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
        if(el == 'special_attributes'){
            for (index = 0; index < data['special_attributes'].length; ++index)
                special_fields.addRow(Object.assign({}, replaceForCategoric(data['special_attributes'][index])))
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

$('#mark_up_attributes').find('[tabulator-field="gui_name"]:not(:first)').on("blur", function(){
    $(this).trigger("keydown", {
        keyCode: 27
    });
})
