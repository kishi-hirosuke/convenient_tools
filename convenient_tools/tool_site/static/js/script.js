console.log('test');
document.getElementById("btn").addEventListener("click", function() {
    console.log('ボタンをクリック');

    const loader = document.querySelector("#loader");
    setTimeout(() => {
        loader.style.visibility = "visible";
    }, 1000);
    console.log('ロード中');
    setTimeout(() => {
        loader.style.visibility = "hidden";
    }, 5000);
    console.log('ロード終了');
});

