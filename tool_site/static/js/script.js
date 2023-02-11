
//header_pulldown
$(function() {

    //burger btn
    const menu_burger = $('.burger_btn');
    const menu_modal = $('.menu_modal');
    const header = $('header');
    var burger_click = true;
    menu_burger.on('click',function(){
        if(burger_click) {
            burger_click = false;
            setTimeout(function() {
                burger_click = true;
            }, 500);
            menu_burger.toggleClass('close');
            menu_modal.toggleClass('active');
            header.toggleClass('active');
        };
    });

    //header
    const tools_area = $('.header_right_slide');
    const tools_pulldown = $('.header_right_tools_pulldown');

    //tools_hover
    tools_area.hover(function(){
        set_tools_hover=setTimeout(function(){
            tools_pulldown.slideDown(200);
        },250);
    },
    function(){
        tools_pulldown.slideUp(200);
        clearTimeout(set_tools_hover);
    });

    const account_area = $('.account_icon');
    const account_slide = $('.account_modal');
    const cc = $('.container');

    var click = true;
    account_area.on('click', function(){
        if(click) {
            click = false;
            setTimeout(function() {
                click = true;
            }, 300);
            account_slide.toggleClass('active');
            // account_slide.slideToggle(500);
        };
        if(account_slide.hasClass('active')) {
            cc.on('click', function() {
                account_slide.toggleClass('active');
            });
        }
    });
    // body.on('click', function() {
    //     if(account_slide.hasClass('active')) {
    //         account_slide.removeClass('active');
    //     }
    // });

});