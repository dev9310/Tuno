// document.getElementsByClassName("active");
const currentTime = document.querySelector(".current-time");
const totalTime = document.querySelector(".total-time");
const progressBar = document.getElementsByClassName("progress-bar");
const player_title = document.getElementsByClassName('track-title')
const player_artist = document.getElementsByClassName('track-artist')
const audio = document.getElementById("aud");
const playBtn = document.querySelector(".play-btn");
const pauseBtn = document.querySelector(".pause");
const player_div = document.querySelector('.music-card')



// Play/Pause Functionality
const progressBarCont = document.getElementById("progress-bar-cont");

progressBarCont.addEventListener("click", (event) => {
    const progressBarWidth = progressBarCont.offsetWidth;
    const clickPosition = event.offsetX;

    if (aud.currentTime == 0) {
        play();
    }
    aud.currentTime =
        (aud.duration *
            Math.round((clickPosition / progressBarWidth) * 100)) /
        100;
});

function play() {

    totalTime.textContent = convertToTime(aud.duration);

    if (audio.paused) {
        audio.play();
        playBtn.classList.add("visually-hidden");
        pauseBtn.classList.remove("visually-hidden");

        aud.addEventListener("timeupdate", () => {
            var percentage = Number(aud.currentTime / aud.duration) * 100;
            progressBar[0].style.width = `${percentage}%`;
            currentTime.textContent = convertToTime(aud.currentTime);
        });
    } else {
        audio.pause();
        playBtn.classList.remove("visually-hidden");
        pauseBtn.classList.add("visually-hidden");
    }
}

function convertToTime(floatValue) {
    const totalSeconds = Math.round(floatValue); // Round to the nearest second
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;


    // Format minutes and seconds to always have 2 digits
    const formattedMinutes = String(minutes).padStart(2, "0");
    const formattedSeconds = String(seconds).padStart(2, "0");

    return `${formattedMinutes}:${formattedSeconds}`;
}

function clickedSong(song_detail) {
    document.querySelector('.track-title').textContent = song_detail.title;
    document.querySelector('.track-artist').textContent = song_detail.singer;
    document.querySelector('.track-img').setAttribute('src', song_detail.image);
    progressBar[0].style.width = `0%`;
    document.querySelector('#aud').setAttribute('src', song_detail.audio_source);


}

// Simulated song loader
document.addEventListener("DOMContentLoaded", () => {
    const loaders = document.querySelectorAll(".loader");
    loaders.forEach((loader, index) => {
        loader.addEventListener("click", () => {
            // Highlight the selected song
            loaders.forEach((l) => l.classList.remove("active"));
            loaders.forEach((l) =>
                l.children[3].classList.add("visually-hidden")
            );
            loaders.forEach((l) =>
                l.children[2].classList.remove("visually-hidden")
            );

            const divId = parseInt(loader.getAttribute('id'), 10);
            const song_detail = songs.find(song => song.id === divId);
            clickedSong(song_detail);
            play();
            // if (aud.paused) {
            //     aud.play();
            //     playBtn.classList.add("visually-hidden");
            //     pauseBtn.classList.remove("visually-hidden");

            // } else {
            //     aud.pause();
            //     playBtn.classList.remove("visually-hidden");
            //     pauseBtn.classList.add("visually-hidden");

            // }
            player_div.classList.remove("visually-hidden");
            loader.classList.add("active");
            loader.children[3].classList.remove("visually-hidden");
            loader.children[2].classList.add("visually-hidden");

            // Simulate loading
            const loadingDiv = loader.querySelector(".loading");
            loadingDiv.classList.remove("hidden");
            setTimeout(() => {
                loadingDiv.classList.add("hidden");
            }, 2000); // Simulate a 2-second load time
        });
    });
});