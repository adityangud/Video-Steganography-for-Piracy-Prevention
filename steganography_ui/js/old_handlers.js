function fileUploadHandler(){
    $('#fileupload'+num_uploads).fileupload({
        dataType: 'json',
        add: function(e, data){
            console.log(data.files[0].name);
            console.log("added");
            data.context = $('#upload_button'+num_uploads).click(function (){
                                data.submit();
                            });

        },
        done: function(e, data){
            data.context.removeClass('glyphicon-upload');
            data.context.addClass('glyphicon-ok');
            $('#fileupload'+num_uploads).replaceWith(data.result.name);
            num_uploads = num_uploads + 1;

            $.post("/", {'page': 'uploads', 'num_uploads': num_uploads}, function(data, textstatus, xhrstuff){
                data = JSON.parse(data);
                $('#replaceable_content').append(data.html);
                fileUploadHandler();
            });
        },
        progressall: function(e, data){
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('.progress-bar').css('width', progress + '%');
            //$($('.progress-bar')[0]).style.width = progress + '%';
            //$('.progress-bar>.sr-only').text(progress+'% Complete');
        },
    });
};

function archiveHandler(){
    $('#archiveTable').on('click','tr', function(){
        if($(this).hasClass('selected_compare')){
            $(this).removeClass('selected_compare');
            $(this).css('background-color', 'white');
        }
        else{
            $(this).addClass('selected_compare');
            $(this).css('background-color', '#1DBDB0');
        }
    });
};

function onNavClick(){
    var page = this.id;
    $('li.active').removeClass('active');
    $(this).parent().addClass('active');

    
    $('#replaceable_content').children().remove();

    $.post("/", {'page': page, 'num_uploads': num_uploads}, function(data, textstatus, xhrstuff){
        data = JSON.parse(data);
        $('#replaceable_content').append(data.html);
        console.log("asjasjdda" + data.name);
        // call specific function depending on it
        if(data.name == 'uploads'){
            fileUploadHandler();
        }
        if(data.name == 'archives'){
            archiveHandler();
        }
    });
    
};

function onOperationSelected(){
    // for compare.html when a particular operation is selected
    console.log("calling onOperationSelected for ");
    console.log($(this));
    var transformation = $(this).val().trim(); 
    if(transformation == "Transform") return;
    var row = $(this).closest('tr');
    var children = row.children('td');
    var filenames = [];
    
    for(var i=0; i < children.length; i++){
        var filename = $(children[i]).attr('filename');
        filenames.push(filename);
    }
    
    var to_send = {'filenames': filenames.join(','), 'transformation': transformation, 'num_selects': $('select').length};

    $.post('/transform', to_send, function(data, textstatus, xhrstuff){
        var data = JSON.parse(data);
        $(data.html).insertAfter(row);
        var latest_select = $('select').length - 1;
        $('#selectpicker'+latest_select).selectpicker();
        $('#selectpicker'+latest_select).on('change', onOperationSelected);

    });

}

function compareFiles(source){
    var files_to_compare = "";
    if(source == "archive_page"){
        var rows_selected = $('.selected_compare');
        var file_compare_str = [];
        for(var i=0; i < rows_selected.length; i++){
            file_compare_str[i] = $($(rows_selected[i]).children()[0]).text();
        }

        files_to_compare = file_compare_str.join(',');
    }
    else{
        // in compare.html
        files_to_compare = $('#files_to_compare').val()
    }
    var data = {'page': 'compare', 'compare': files_to_compare, 'num_selects': $('select').length};

    $.post('/', data, function(data, textstatus, xhrstuff){
        var data = JSON.parse(data);
        $('#replaceable_content').children().remove();
        $('#replaceable_content').append(data.html);

        $('.sidebar_navigation>.active').removeClass('active');
        $('#compare').addClass('active');

        var latest_select = $('select').length - 1;
        $('#selectpicker'+latest_select).selectpicker();
        $('#selectpicker'+latest_select).on('change', onOperationSelected);
    });
};


function onLoad(){
    num_uploads=0;
    console.log("loaded");
    $('.sidebar_navigation#nav_overview').on('click', onNavOverview);
    $('.sidebar_navigation#nav_uploads').on('click', onNavUploads);
    $('.sidebar_navigation#nav_archives').on('click', onNavArchives);
    $('.sidebar_navigation#nav_compare').on('click', onNavCompare);
};
