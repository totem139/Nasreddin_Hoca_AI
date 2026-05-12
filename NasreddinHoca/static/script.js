const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");
const musicVolumeSlider = document.getElementById("musicVolume");
const volumeValue = document.getElementById("volumeValue");

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});

function addMessage(text, sender) {
    const msg = document.createElement("div");
    msg.classList.add("message", sender);
    msg.textContent = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// --- MOD DEĞİŞTİRME BUTONLARI ---
const mod1 = document.getElementById("mod1");
const mod2 = document.getElementById("mod2");

let activeMode = 1;
mod1.addEventListener("click", () => changeMode(1));
mod2.addEventListener("click", () => changeMode(2));

const hocaImg = document.getElementById("hoca-img");
function updateHocaImage(mode) {
    if(mode === 1) hocaImg.src = "/static/images/normal_hoca.png";
    else hocaImg.src = "/static/images/kuran_hoca.png";
}

async function changeMode(mode) {
    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: `/mod ${mode}` })
        });
        const data = await response.json();
        addMessage(data.reply, "bot");

        activeMode = mode;
        document.body.classList.remove("mode-normal", "mode-kuran");
        if (mode === 1) document.body.classList.add("mode-normal");
        else document.body.classList.add("mode-kuran");

        mod1.classList.toggle("active", mode === 1);
        mod2.classList.toggle("active", mode === 2);
        playMusicForMode(mode);
        updateHocaImage(mode);
    } catch (error) {
        addMessage("⚠️ Mod değiştirilemedi!", "bot");
        console.error(error);
    }
}

// 🎶 MÜZİK KONTROLÜ
const normalMusic = document.getElementById("normalMusic");
const kuranMusic = document.getElementById("kuranMusic");

normalMusic.volume = musicVolumeSlider.value;
kuranMusic.volume = musicVolumeSlider.value;

musicVolumeSlider.addEventListener("input", () => {
    normalMusic.volume = musicVolumeSlider.value;
    kuranMusic.volume = musicVolumeSlider.value;
    volumeValue.textContent = Math.round(musicVolumeSlider.value * 100) + "%";
});

function playMusicForMode(mode) {
    if (!isMusicOn) return;
    normalMusic.pause();
    kuranMusic.pause();
    normalMusic.currentTime = 0;
    kuranMusic.currentTime = 0;
    if (mode === 1) normalMusic.play();
    else if (mode === 2) kuranMusic.play();
}

// 🎧 MÜZİK KONTROL BUTONU
const toggleMusicBtn = document.getElementById("toggleMusic");
let isMusicOn = true;

toggleMusicBtn.addEventListener("click", () => {
    isMusicOn = !isMusicOn;
    if (isMusicOn) {
        toggleMusicBtn.textContent = "🔊 Müzik Kapat";
        playMusicForMode(activeMode);
    } else {
        toggleMusicBtn.textContent = "🔇 Müzik Aç";
        normalMusic.pause();
        kuranMusic.pause();
    }
});

// --- Hoca sesli okusun ---
let hocaSpeakingEnabled = true;
let voices = [];

function loadVoices() {
    voices = speechSynthesis.getVoices();
}
loadVoices();
speechSynthesis.onvoiceschanged = loadVoices;

function speakHoca(text) {
    if (!hocaSpeakingEnabled) return;

    // Dil tespiti
    let lang = "tr-TR"; // default Türkçe
    if (/arap[açc]a/i.test(text)) lang = "ar-SA";
    else if (/türkçe/i.test(text)) lang = "tr-TR";

    // Uygun sesi seç
    let selectedVoice = voices.find(v => v.lang.startsWith(lang)) || null;

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang;
    if (selectedVoice) utterance.voice = selectedVoice;
    utterance.pitch = 0.9;
    utterance.rate = 1;
    utterance.volume = 1;

    speechSynthesis.speak(utterance);
}

// Konuşmayı aç/kapat butonu
document.getElementById("stopSpeech").addEventListener("click", () => {
    if (hocaSpeakingEnabled) {
        hocaSpeakingEnabled = false;
        speechSynthesis.cancel();
        document.getElementById("stopSpeech").textContent = "🗣️ Konuşmayı Aç";
    } else {
        hocaSpeakingEnabled = true;
        document.getElementById("stopSpeech").textContent = "🔇 Konuşmayı Kapat";
    }
});

async function sendMessage() {
    const text = userInput.value.trim();
    if (text === "") return;

    addMessage(text, "user");
    userInput.value = "";

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();
        addMessage(data.reply, "bot");
        speakHoca(data.reply);
    } catch (error) {
        addMessage("⚠️ Sunucuya bağlanılamadı!", "bot");
        console.error(error);
    }
}