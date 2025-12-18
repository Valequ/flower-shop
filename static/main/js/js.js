function togglePayment() {
    const payment = document.querySelector('.payment-method');
    payment.classList.toggle('open');
}

function selectPayment(method) {
    document.getElementById('paymentLabel').textContent = method;
    document.querySelector('.payment-method').classList.remove('open');
    // Сохраняем выбранный способ оплаты
    localStorage.setItem('paymentMethod', method);
}