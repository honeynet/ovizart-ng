/* __author__='ggercek' */
$(function() {

    function openUploadPage(){
        window.location='/newAnalysis';
    }

    function initButtons() {
        $('#btn-browse').on('click', function(){
            window.location='/';
        });

        $('#btn-new').on('click', function(){
            window.location='/new';
        });

        $('#btn-download').on('click', function(){
            //window.location='/new';
            alert('Not yet implemented.');
        });

        $('#btn-delete').on('click', function(){
            // window.location='/
            $("#analysisTable").attr("action", "/delete/");
            $('#analysisTable').submit();
        });
    }



    // Initialize page
    initButtons();
});