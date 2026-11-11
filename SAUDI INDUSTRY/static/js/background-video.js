const backgroundVideos = document.querySelectorAll(
    "[data-background-video]"
);

if (backgroundVideos.length) {
    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    );

    function updateBackgroundVideos() {
        backgroundVideos.forEach((video) => {
            if (reducedMotion.matches) {
                video.pause();
                return;
            }

            video.play().catch((error) => {
                console.error(
                    "Background video failed to play.",
                    error
                );
            });
        });
    }

    updateBackgroundVideos();
    reducedMotion.addEventListener(
        "change",
        updateBackgroundVideos
    );
}
