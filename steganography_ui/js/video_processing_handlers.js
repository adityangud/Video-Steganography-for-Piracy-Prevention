function videoUploadHandler(){
    $('#videoUpload').fileupload({
        dataType: 'json',
        add: function(e, data){
            console.log(data.files[0].name);
            console.log("added");
            data.context = $('#video_upload_button').click(function() {
                data.submit();
            });
        },
        done: function(e, data){
            data.context.removeClass('glyphicon-upload');
            data.context.addClass('glyphicon-ok');
            console.log(data);
            $('#video_upload_div').replaceWith(data.result.html);
        },
        progressall: function(e, data){
            var progress = parseInt(data.loaded /  data.total * 100, 10);
            $('.progress-bar').css('width', progress + '%');
        },
    });
};

function onNavVideoProcessing(){
    console.log("navigated to video processing");
    $.post('/video_processing/', {}, function(data, textstatus, xhrstuff){
        data = JSON.parse(data);
        $('#replaceable_content').children().remove();
        $('#replaceable_content').append(data.html);
        videoUploadHandler();
    });
};

