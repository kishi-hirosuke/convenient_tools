
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
    const close_btn = $('.sample_box');
    const submit_btn = $('.submit_icon');

    close_btn.on('click', function() {
        $(this).css('display', 'none');
    });
    submit_btn.on('click', function() {
        $('.error_alert').css('display', 'none');
    });

    // //sample
    const sample_box = $('.sample_box');
    const sample_erea = $('.sample_erea');
    const sample_btn = $('.sample_btn');
    const sample_close = $('.sample_close');

    sample_btn.on('click', function() {
        sample_box.css('display', 'block');
        sample_erea.css('display', 'block');
    });


    //drag_and_drop
    // const file = $('.file_form').val();
    // const plus_icon = $('.plus_icon');
    // const file_items = $('.file_label');

    // function file_empty() {
    //     if (file.length == 0) {
    //         plus_icon.css('display', 'block');
    //     }else {
    //         file_items.append('<li>' + file + '<li>');
    //         plus_icon.css('display', 'none');
    //     };
    // };

    // file_empty();

    // function file_empty() {
    //     console.log(file.length);
    //     console.log(file);
    // };

    // file_empty();

});