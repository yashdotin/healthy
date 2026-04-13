let breathingInterval = null;
let breathingSeconds = 30;

let quizScore = 0;

let focusScore = 0;

let memoryPattern = [];
let memoryIndex = 0;
let memoryScore = 0;
let memoryLevel = 1;
let memoryAcceptInput = false;
let memoryRunTimer = null;

document.addEventListener("DOMContentLoaded", () => {
    initGameTabs();
});

function initGameTabs() {
    const tabs = document.querySelectorAll(".game-tab");
    const panels = document.querySelectorAll(".game-panel");

    if (!tabs.length || !panels.length) return;

    tabs.forEach((tab) => {
        tab.addEventListener("click", () => {
            tabs.forEach((t) => t.classList.remove("active"));
            panels.forEach((p) => p.classList.remove("active"));

            tab.classList.add("active");
            const panel = document.getElementById(tab.dataset.game);
            if (panel) panel.classList.add("active");

            if (tab.dataset.game === "reflexGame") {
                moveTarget();
            }
        });
    });

    const focusStage = document.getElementById("focusStage");
    if (focusStage) {
        const target = document.getElementById("focusTarget");
        if (target) {
            target.style.left = "24px";
            target.style.top = "24px";
        }
    }
}

function startBreathing() {
    const orb = document.getElementById("breathOrb");
    const text = document.getElementById("breathText");
    const timer = document.getElementById("breathTimer");

    if (!orb || !text || !timer) return;

    clearInterval(breathingInterval);
    breathingSeconds = 30;
    timer.textContent = breathingSeconds;
    text.textContent = "Inhale";
    orb.classList.add("active");

    breathingInterval = setInterval(() => {
        breathingSeconds -= 1;
        timer.textContent = breathingSeconds;

        const phase = breathingSeconds % 8;
        if (phase === 0 || phase === 1 || phase === 2 || phase === 3) {
            text.textContent = "Inhale";
        } else {
            text.textContent = "Exhale";
        }

        if (breathingSeconds <= 0) {
            clearInterval(breathingInterval);
            orb.classList.remove("active");
            text.textContent = "Done";
            timer.textContent = "30";
            setTimeout(() => {
                text.textContent = "Breathe";
            }, 1200);
        }
    }, 1000);
}

function answerQuiz(correct) {
    const scoreEl = document.getElementById("quizScore");
    const feedback = document.getElementById("quizFeedback");

    if (!scoreEl || !feedback) return;

    if (correct) {
        quizScore += 1;
        feedback.textContent = "Correct. Small health habits really matter.";
        feedback.style.color = "#86efac";
    } else {
        feedback.textContent = "Not quite. Try again and keep the habit that supports health.";
        feedback.style.color = "#fecaca";
    }

    scoreEl.textContent = quizScore;
}

function moveTarget() {
    const target = document.getElementById("focusTarget");
    const stage = document.getElementById("focusStage");

    if (!target || !stage) return;

    const maxX = Math.max(0, stage.clientWidth - 72);
    const maxY = Math.max(0, stage.clientHeight - 72);

    const x = Math.floor(Math.random() * Math.max(maxX, 1));
    const y = Math.floor(Math.random() * Math.max(maxY, 1));

    target.style.left = `${x}px`;
    target.style.top = `${y}px`;
}

function hitTarget() {
    const scoreEl = document.getElementById("focusScore");
    if (!scoreEl) return;

    focusScore += 1;
    scoreEl.textContent = focusScore;
    moveTarget();
}

function startMemoryGame() {
    const status = document.getElementById("memoryStatus");
    const patternText = document.getElementById("memoryPattern");
    const levelEl = document.getElementById("memoryLevel");
    const scoreEl = document.getElementById("memoryScore");

    if (!status || !patternText || !levelEl || !scoreEl) return;

    clearTimeout(memoryRunTimer);
    memoryPattern = [];
    memoryIndex = 0;
    memoryAcceptInput = false;

    const colors = ["cyan", "pink", "violet", "lime"];
    const patternLength = 3 + memoryLevel;

    for (let i = 0; i < patternLength; i++) {
        memoryPattern.push(colors[Math.floor(Math.random() * colors.length)]);
    }

    levelEl.textContent = memoryLevel;
    scoreEl.textContent = memoryScore;
    patternText.textContent = "Watch closely...";
    status.textContent = "Memorize the sequence";

    let i = 0;
    const interval = setInterval(() => {
        patternText.textContent = memoryPattern.slice(0, i + 1).map(c => c.toUpperCase()).join(" • ");
        i += 1;

        if (i >= memoryPattern.length) {
            clearInterval(interval);
            memoryRunTimer = setTimeout(() => {
                memoryAcceptInput = true;
                patternText.textContent = "Your turn";
                status.textContent = "Tap the colors in the correct order";
            }, 700);
        }
    }, 650);
}

function pickMemoryColor(color) {
    const status = document.getElementById("memoryStatus");
    const patternText = document.getElementById("memoryPattern");
    const scoreEl = document.getElementById("memoryScore");
    const levelEl = document.getElementById("memoryLevel");

    if (!status || !patternText || !scoreEl || !levelEl) return;
    if (!memoryAcceptInput || !memoryPattern.length) {
        status.textContent = "Press Start Memory Game first.";
        return;
    }

    if (memoryPattern[memoryIndex] === color) {
        memoryIndex += 1;
        status.textContent = `Good. ${memoryIndex} of ${memoryPattern.length}`;

        if (memoryIndex >= memoryPattern.length) {
            memoryScore += 1;
            memoryLevel += 1;
            scoreEl.textContent = memoryScore;
            levelEl.textContent = memoryLevel;
            patternText.textContent = "Great job!";
            status.textContent = "Level cleared. Starting next one...";
            memoryAcceptInput = false;
            setTimeout(() => startMemoryGame(), 1000);
        }
    } else {
        patternText.textContent = "Wrong sequence";
        status.textContent = "Try again. Tap Start Memory Game.";
        memoryAcceptInput = false;
    }
}

function setHiddenValue(name, value) {
    const el = document.getElementsByName(name)[0];
    if (el) el.value = value;
}

function prepareHeartForm() {
    const form = document.querySelector(".heart-form");
    if (!form) return true;

    const cp = form.querySelector('[name="cp"]')?.value ?? "0";
    const restecg = form.querySelector('[name="restecg"]')?.value ?? "0";
    const thal = form.querySelector('[name="thal"]')?.value ?? "0";

    ["cp_1", "cp_2", "cp_3", "restecg_1", "restecg_2", "thal_1", "thal_2", "thal_3"].forEach((name) => setHiddenValue(name, 0));

    if (cp === "1") setHiddenValue("cp_1", 1);
    if (cp === "2") setHiddenValue("cp_2", 1);
    if (cp === "3") setHiddenValue("cp_3", 1);

    if (restecg === "1") setHiddenValue("restecg_1", 1);
    if (restecg === "2") setHiddenValue("restecg_2", 1);

    if (thal === "1") setHiddenValue("thal_1", 1);
    if (thal === "2") setHiddenValue("thal_2", 1);
    if (thal === "3") setHiddenValue("thal_3", 1);

    return true;
}

function resetStressHiddenFields() {
    const hiddenFields = document.querySelectorAll('input[type="hidden"][data-auto="stress"]');
    hiddenFields.forEach((input) => {
        input.value = 0;
    });
}

function setStressOneHot(prefix, selectedValue) {
    const key = `${prefix}_${selectedValue}`;
    const field = document.getElementsByName(key)[0];
    if (field) field.value = 1;
}

function prepareStressForm() {
    const form = document.querySelector(".stress-form");
    if (!form) return true;

    resetStressHiddenFields();

    const fields = [
        "Choose your gender",
        "What is your course?",
        "Your current year of Study",
        "What is your CGPA?",
        "Marital status",
        "Do you have Depression?",
        "Do you have Anxiety?",
        "Do you have Panic attack?",
        "Did you seek any specialist for a treatment?"
    ];

    fields.forEach((name) => {
        const select = form.querySelector(`[name="${name}"]`);
        if (select) {
            setStressOneHot(name, select.value);
        }
    });

    return true;
}