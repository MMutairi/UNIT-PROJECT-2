
document.addEventListener("DOMContentLoaded", function () {
    const video = document.getElementById("homeBackgroundVideo");

    if (!video) {
        return;
    }

    video.play().catch(function () {
        console.error("Homepage background video failed to play.");
    });
});
