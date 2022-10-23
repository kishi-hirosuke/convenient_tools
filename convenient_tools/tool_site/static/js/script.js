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

    const process_area = $('.header_right_content_1');
    const process_pulldown = $('.header_right_process_pulldown');
    const contact_area = $('.header_right_content_2');
    const contact_pulldown = $('.header_right_contact_pulldown');

    //process_hover
    process_area.hover(function(){
        set_process_hover=setTimeout(function(){
            process_pulldown.slideDown(300);
        },200);
    },
    function(){
        process_pulldown.slideUp(300);
        clearTimeout(set_process_hover);
    });
    //contact_hover
    contact_area.hover(function(){
        set_contact_hover = setTimeout(function(){
            contact_pulldown.slideDown(300);
        },200);
    },
    function(){
        contact_pulldown.slideUp(300);
        clearTimeout(set_contact_hover);
    });
});