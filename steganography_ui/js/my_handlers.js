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

            $.post("/uploads/", {'num_uploads': num_uploads}, function(data, textstatus, xhrstuff){
                data = JSON.parse(data);
                $('#replaceable_content').append(data.html);
                fileUploadHandler();
            });
        },
        progressall: function(e, data){
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('.progress-bar').css('width', progress + '%');
        },
        replaceFileInput: false,
    });
};


function onNavOverview(){
    console.log("navigated to Overview");
    $.post('/overview/', {}, function(data, textstatus, xhrstuff){
        console.log(data);
        data = JSON.parse(data);
        $('#replaceable_content').children().remove();
        $('#replaceable_content').append(data.html);

        $('.carousel').carousel({
            interval: false
        });

        var last_slide_num = localStorage.getItem('current_slide');
        if (last_slide_num == null) last_slide_num = 0;
        else last_slide_num = parseInt(last_slide_num);

        console.log('last slide num was ' + last_slide_num);
        $('.carousel').carousel(last_slide_num);

        $('#overview_carousel_id').on('slide.bs.carousel', function () {

              var slide_num = $('.item.active').attr('id');
              slide_num = parseInt(slide_num.split('stegoSlide')[1])
              slide_num = slide_num + 1;
              localStorage.setItem('current_slide', slide_num);
              console.log("changed slide_num to " + slide_num);
        })
    });
}

function onNavUploads(){
    console.log("navigated to uploads");

    $.post('/uploads/', {'num_uploads': num_uploads}, function(data, textstatus, xhrstuff){
        data = JSON.parse(data);
        $('#replaceable_content').children().remove();
        $('#replaceable_content').append(data.html);

        fileUploadHandler();
    });
}


function onOperationSelected(){
    // for compare.html when a particular operation is selected

    var transformation = $(this).val().trim(); 
    if(transformation == "Transform") return;
    var row = $(this).closest('tr');
    var children = row.children('td');
    var filenames = [];

    var docs = [];
    
    for(var i=0; i < children.length - 1; i++){
        var filename = $(children[i]).attr('filename');
        var compatiable = $(children[i]).attr('compatiable');
        if(compatiable == "True") compatiable = true;
        else compatiable = false;

        docs.push({'name':filename, 'compatiable': compatiable});
    }
    
    var to_send = {'documents': JSON.stringify(docs), 'transformation': transformation, 'num_selects': $('select').length};

    $.post('/transform/', to_send, function(data, textstatus, xhrstuff){
        var data = JSON.parse(data);
        $(data.html).insertAfter(row);
        var latest_select = $('select').length - 1;
        $('#selectpicker'+latest_select).selectpicker();
        $('#selectpicker'+latest_select).on('change', onOperationSelected);

    });

}



function compareFiles(files_to_compare){
    console.log("Compareing files" + files_to_compare);

    files_to_compare = files_to_compare.trim();
    if(files_to_compare == '') return;

    data = {'files': files_to_compare, 'num_selects': $('select').length};

    $.post('/comparefiles/', data, function(data, textstatus, xhrstuff){
        var data = JSON.parse(data);
        console.log(data);

        $('#replaceable_content').children().remove();
        $('#replaceable_content').append(data.html);

        $('.sidebar_navigation>.active').removeClass('active');
        $('#compare').addClass('active');

        var latest_select = $('select').length - 1;
        $('#selectpicker' + latest_select).selectpicker();
        $('#selectpicker' + latest_select).on('change', onOperationSelected);
    });
}

function onNavArchives(){
    console.log("navigated to archives");

    $.post('/archives/', {}, function(data, textstatus, xhrstuff){
        data = JSON.parse(data);
        $('#replaceable_content').children().remove();
        $('#replaceable_content').append(data.html);

        $('#archiveTable').on('click', 'tr', function(){
            if($(this).hasClass('selected_compare')){
                $(this).removeClass('selected_compare');
                $(this).css('background-color', 'white');
            }
            else{
                $(this).addClass('selected_compare');
                $(this).css('background-color', '#1DBDB0');
            }
        });

        $('#archiveCompareBtn').on('click', function(){
            console.log("Clicked");

            var files_to_compare = "";
            var rows_selected = $('.selected_compare');
            var file_compare_str = [];

            for(var i=0; i < rows_selected.length; i++)
                file_compare_str[i] = $($(rows_selected[i]).children()[0]).text();

            files_to_compare = file_compare_str.join(',');

            compareFiles(files_to_compare);
        });

    });

}
function onNavCompare(){
    console.log("navigated to compare");
    $.post('/compare/', {}, function(data, textstatus, xhrstuff){
        data = JSON.parse(data);
        $('#replaceable_content').children().remove();
        $('#replaceable_content').append(data.html);

        $('#compareBtn').on('click', function(){
            $('#modalArchiveList').modal('show');

            $('#compareModalTable').on('click', 'tr', function(){
                if($(this).hasClass('selected_compare')){
                    $(this).removeClass('selected_compare');
                    $(this).css('background-color', 'white');
                }
                else{
                    $(this).addClass('selected_compare');
                    $(this).css('background-color', '#1DBDB0');
                }
            });

        });
    });

}

function onModalFileCompare(){

    var files_to_compare = "";
    var rows_selected = $('.selected_compare');
    var file_compare_str = [];

    for(var i=0; i < rows_selected.length; i++)
        file_compare_str[i] = $($(rows_selected[i]).children()[0]).text();

    files_to_compare = file_compare_str.join(',');
    console.log(files_to_compare);

    //$('#modalArchiveList').modal('hide');

    compareFiles(files_to_compare);
};

function onNavJoiner(){

    console.log("navigated to joiner");
    $.post('/joiner/', {}, function(data, textstatus, xhrstuff){
        data = JSON.parse(data);
        $('#replaceable_content').children().remove();
        $('#replaceable_content').append(data.html);
    });
};

function onNavSplitter(){
    console.log("navigated to splitter");
    $.post('/splitter/', {}, function(data, textstatus, xhrstuff){
        data = JSON.parse(data);
        $('#replaceable_content').children().remove();
        $('#replaceable_content').append(data.html);
    });
};

function onNavEmbedder(){
    console.log("navigated to embedder");
    $.post('/embedder/', {}, function(data, textstatus, xhrstuff){
        data = JSON.parse(data);
        $('#replaceable_content').children().remove();
        $('#replaceable_content').append(data.html);

    });

};

function onNavDetector(){
    console.log("navigated to detector");
    $.post('/detector/', {}, function(data, textstatus, xhrstuff){
        data = JSON.parse(data);
        $('#replaceable_content').children().remove();
        $('#replaceable_content').append(data.html);

    });

};


function onLoad(){
    num_uploads=0;
    localStorage.setItem('current_slide', 0);
    console.log("loaded");
    $('.sidebar_navigation#nav_overview').on('click', onNavOverview);
    $('.sidebar_navigation#nav_uploads').on('click', onNavUploads);
    $('.sidebar_navigation#nav_archives').on('click', onNavArchives);
    $('.sidebar_navigation#nav_compare').on('click', onNavCompare);

    $('.sidebar_navigation#nav_video_processing').on('click', onNavVideoProcessing);
    $('.sidebar_navigation#nav_joiner').on('click', onNavJoiner);
    $('.sidebar_navigation#nav_splitter').on('click', onNavSplitter);
    $('.sidebar_navigation#nav_embedder').on('click', onNavEmbedder);
    $('.sidebar_navigation#nav_detector').on('click', onNavDetector);
};
