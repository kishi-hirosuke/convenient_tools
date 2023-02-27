
//header_pulldown
$(function() {

    // const account_area = $('.account_icon');
    // const account_slide = $('.account_modal');
    // const cc = $('.container');

    // var click = true;
    // account_area.on('click', function(){
    //     if(click) {
    //         click = false;
    //         setTimeout(function() {
    //             click = true;
    //         }, 300);
    //         account_slide.toggleClass('active');
    //         // account_slide.slideToggle(500);
    //     };
    //     if(account_slide.hasClass('active')) {
    //         cc.on('click', function() {
    //             account_slide.toggleClass('active');
    //         });
    //     };
    // });

    //error_message_delete
    const close_btn = $('.close_icon');
    const submit_btn = $('.submit_icon');

    close_btn.on('click', function() {
        $(this).parent().css('display', 'none');
    });
    submit_btn.on('click', function() {
        $('.error_alert').css('display', 'none');
    });

});