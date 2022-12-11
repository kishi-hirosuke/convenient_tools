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

    const tools_area = $('.header_right_content_1');
    const tools_pulldown = $('.header_right_tools_pulldown');
    const contact_area = $('.header_right_content_2');
    const contact_pulldown = $('.header_right_contact_pulldown');

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
});