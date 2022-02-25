window.onload = hydrate;

function hydrate() {
    const homeMovementButton = document.querySelector('#home-movement');
    homeMovementButton.addEventListener('click', homeMovement);

    async function homeMovement() {
            const response = await fetch('/api/movement/home', { method: 'POST' });
            if (response.status !== 201) {
                alert('Failed to home!');
            }
    }
}
