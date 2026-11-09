document.addEventListener("DOMContentLoaded", function () {
    const video = document.getElementById("homeBackgroundVideo");
    const toggle = document.getElementById("videoToggle");

    if (!video || !toggle) {
        return;
    }

    function updateButton() {
        const paused = video.paused;

        toggle.textContent = paused
            ? "Play video"
            : "Pause video";

        toggle.setAttribute(
            "aria-label",
            paused ? "Play background video" : "Pause background video"
        );
    }

    function playVideo() {
        video.play()
            .then(updateButton)
            .catch(updateButton);
    }

    toggle.addEventListener("click", function () {
        if (video.paused) {
            playVideo();
        } else {
            video.pause();
            updateButton();
        }
    });

    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    if (!reducedMotion) {
        playVideo();
    } else {
        updateButton();
    }
});
