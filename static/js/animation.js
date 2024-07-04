document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;

    for (let i = 0; i < 50; i++) {
        const raindrop = document.createElement('div');
        raindrop.className = 'raindrop';
        raindrop.style.left = `${Math.random() * 100}vw`;
        raindrop.style.animationDuration = `${Math.random() * 3 + 2}s`;
        raindrop.style.animationDelay = `${Math.random() * 5}s`;
        body.appendChild(raindrop);
    }
});
