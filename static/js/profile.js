document.addEventListener('DOMContentLoaded', function() {
    // Маска телефона
    const phoneInput = document.getElementById('id_phone') || document.querySelector('[name="phone"]');
    if (phoneInput && typeof IMask !== 'undefined') {
        IMask(phoneInput, { mask: '+{7} (000) 000-00-00', lazy: true });
    }
    });
