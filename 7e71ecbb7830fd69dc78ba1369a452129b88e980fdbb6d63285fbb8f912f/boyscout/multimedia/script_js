const storyText = document.getElementById("story-text");
const imageElement = document.getElementById("illustration");
const audioElement = document.getElementById("story-audio");
const playButton = document.getElementById("play-button");

let config;
let currentParagraph = 0;

async function loadConfig() {
    const response = await fetch("config.json");
    config = await response.json();

    audioElement.src = config.audio;

    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('autoplay') === 'true') {
        startPlayback();
    } else {
        playButton.style.display = 'block';
        playButton.addEventListener('click', startPlayback);
    }
}

function startPlayback() {
    playButton.style.display = 'none';
    audioElement.play();
    requestAnimationFrame(checkTime);
}

function checkTime() {
    if (currentParagraph >= config.paragraphs.length) return;

    const now = audioElement.currentTime;
    const para = config.paragraphs[currentParagraph];

    if (now >= para.timestamp) {
        displayParagraph(para);
        currentParagraph++;
    }

    requestAnimationFrame(checkTime);
}

function displayParagraph(paragraph) {
    storyText.innerHTML = paragraph.lines.join("<br/>");
    imageElement.src = paragraph.image;
}

loadConfig();
