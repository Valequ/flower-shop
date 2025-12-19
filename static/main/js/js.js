function togglePayment() {
    const payment = document.querySelector('.payment-method');
    payment.classList.toggle('open');
}

function selectPayment(method) {
    document.getElementById('paymentLabel').textContent = method;
    document.querySelector('.payment-method').classList.remove('open');
    localStorage.setItem('paymentMethod', method);
}

// бургер
document.addEventListener('DOMContentLoaded', function() {
    const burgerBtn = document.getElementById('burger-btn');
    const navMenu = document.getElementById('nav-menu');

    burgerBtn.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        burgerBtn.classList.toggle('active');
        
        document.body.classList.toggle('no-scroll');
    });

    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            burgerBtn.classList.remove('active');
        });
    });
});