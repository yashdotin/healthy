let box = document.getElementById("box");
let score = 0;

function moveBox() {
    let x = Math.random() * 300;
    let y = Math.random() * 200;

    box.style.left = x + "px";
    box.style.top = y + "px";
}

function hitBox() {
    score++;
    document.getElementById("score").innerText = score;
    moveBox();
}