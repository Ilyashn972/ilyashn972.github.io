const storyText = document.getElementById("story-text");
const imageElement = document.getElementById("illustration");
const audioElement = document.getElementById("story-audio");

let config;
let paragraphIndex = 0;
let lineIndex = 0;

async function loadConfig() {
    const response = await fetch("config.json");
    config = await response.json();
    storyText.textContent = "Click anywhere to start the story...";
    document.body.addEventListener("click", startStory, { once: true });
}

function startStory() {
    playParagraph(paragraphIndex);
}

function playParagraph(index) {
    if (index >= config.paragraphs.length) {
        storyText.textContent = "The End.";
        imageElement.src = "../../local_image.jpg";
        return;
    }

    const para = config.paragraphs[index];
    lineIndex = 0;
    imageElement.src = para.image;
    audioElement.src = para.audio;
    audioElement.play();
    
    showNextLine(para);
}

function showNextLine(paragraph) {

    if (lineIndex >= paragraph.lines.length) {
        paragraphIndex++;
        setTimeout(() => playParagraph(paragraphIndex), 750); // Small pause between paragraphs
        return;
    }

    storyText.textContent = paragraph.lines[lineIndex];
    lineIndex++;
    setTimeout(() => showNextLine(paragraph), paragraph.lineDuration);
}

loadConfig();

