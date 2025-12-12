let nukeCountdown;
let rickrollVideoPreloaded = false;

function openNukeModal() {
    const modal = document.getElementById('nukeModal');
    const giveUpBtn = document.getElementById('giveUpButton');
    const countdownText = document.getElementById('countdownText');
    const video = document.getElementById('rickrollVideo');
    
    modal.style.display = 'flex';
    giveUpBtn.disabled = true;
    giveUpBtn.classList.remove('active');
    
    if (!rickrollVideoPreloaded && video) {
        video.load();
        rickrollVideoPreloaded = true;
    }
    
    let seconds = 5;
    countdownText.textContent = `Available in ${seconds} seconds...`;
    
    nukeCountdown = setInterval(() => {
        seconds--;
        if (seconds > 0) {
            countdownText.textContent = `Available in ${seconds} second${seconds !== 1 ? 's' : ''}...`;
        } else {
            countdownText.textContent = 'Click if you dare...';
            giveUpBtn.disabled = false;
            giveUpBtn.classList.add('active');
            clearInterval(nukeCountdown);
        }
    }, 1000);
}

function closeNukeModal() {
    const modal = document.getElementById('nukeModal');
    modal.style.display = 'none';
    clearInterval(nukeCountdown);
}

function activateRickRoll() {
    const modal = document.getElementById('nukeModal');
    const container = document.getElementById('rickrollContainer');
    const video = document.getElementById('rickrollVideo');
    
    modal.style.display = 'none';
    clearInterval(nukeCountdown);
    
    container.style.display = 'block';
    
    if (video) {
        video.play();
    }

    const escapeHandler = function(e) {
        if (e.key === 'Escape') {
            container.style.display = 'none';
            if (video) {
                video.pause();
                video.currentTime = 0;
            }
            document.removeEventListener('keydown', escapeHandler);
        }
    };
    
    document.addEventListener('keydown', escapeHandler);
}

window.addEventListener('click', function(event) {
    const modal = document.getElementById('nukeModal');
    if (event.target === modal) {
        closeNukeModal();
    }
});
