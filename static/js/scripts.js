window.setTimeout(function() {
    $(".alert-dismissible").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove(); 
    });
}, 3000);