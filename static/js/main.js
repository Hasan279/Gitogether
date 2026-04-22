// Auto dismiss flash messages after 4 seconds
document.addEventListener('DOMContentLoaded', () => {
    const flashes = document.querySelectorAll('#flash-container .alert');
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.style.transition = 'opacity 0.4s ease';
            flash.style.opacity = '0';
            setTimeout(() => flash.remove(), 400);
        }, 4000);
    });
});

// Confirm before any delete/deactivate form submission
document.querySelectorAll('form[data-confirm]').forEach(form => {
    form.addEventListener('submit', e => {
        if (!confirm(form.dataset.confirm)) {
            e.preventDefault();
        }
    });
});

// Active nav link highlight
document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    document.querySelectorAll('.navbar a').forEach(link => {
        if (link.getAttribute('href') === path) {
            link.classList.add('active-link');
        }
    });
});