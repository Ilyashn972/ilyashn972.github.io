const storyText = document.getElementById("story-text");
const imageElement = document.getElementById("illustration");
const audioElement = document.getElementById("story-audio");

let config;
let currentParagraph = 0;
let animationFrameId;

async function loadConfig() {
    const response = await fetch("config.json");
    config = await response.json();

    audioElement.src = config.audio;
    storyText.textContent = "Press space to start the story...";

    document.body.addEventListener("keydown", (event) => {
        if (event.code === "Space") {
            event.preventDefault(); // Prevent scrolling
            if (audioElement.paused) {
                startPlayback();
            } else {
                pausePlayback();
            }
        }
    });
}

function startPlayback() {
    audioElement.play();
    animationFrameId = requestAnimationFrame(checkTime);
}

function pausePlayback() {
    audioElement.pause();
    cancelAnimationFrame(animationFrameId);
}

function checkTime() {
    if (currentParagraph >= config.paragraphs.length) {
        cancelAnimationFrame(animationFrameId);
        return;
    }

    const now = audioElement.currentTime;
    const para = config.paragraphs[currentParagraph];

    if (now >= para.timestamp) {
        displayParagraph(para);
        currentParagraph++;
    }

    animationFrameId = requestAnimationFrame(checkTime);
}

function displayParagraph(paragraph) {
    storyText.innerHTML = paragraph.lines.join("<br/>");
    imageElement.src = paragraph.image;
}

loadConfig();