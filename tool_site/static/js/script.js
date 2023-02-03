// console.log('test');
// document.getElementById("btn").addEventListener("click", function() {
//     console.log('ボタンをクリック');

//     const loader = document.querySelector("#loader");
//     setTimeout(() => {
//         loader.style.visibility = "visible";
//     }, 1000);
//     console.log('ロード中');
//     setTimeout(() => {
//         loader.style.visibility = "hidden";
//     }, 5000);
//     console.log('ロード終了');
// });

// const header_about_link = document.getElementById('header_about_link');

// header_about_link.addEventListener('mouseover', function(){
//     header_about_link.style.width = '220px';
// }, false);
// header_about_link.addEventListener('mouseleave', function(){
//     header_about_link.style.width = '200px';
// });


//header_pulldown
$(function() {

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
    const account_slide = $('.header_account_contents');
    const cc = $('.container');

    var click = true
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