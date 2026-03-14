document.addEventListener('DOMContentLoaded', function() {
    // Инициализация свайпера
    const swiper = new Swiper('.event-gallery-swiper', {
        loop: true,
        spaceBetween: 10,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });

    // Расчет стоимости билетов
    const ticketsInput = document.getElementById('tickets_quantity');
    const totalPriceSpan = document.getElementById('total-price');

    if (ticketsInput && totalPriceSpan) {
        const pricePerTicket = parseFloat(totalPriceSpan.dataset.price);
        const maxTickets = parseInt(ticketsInput.max) || 999; // Получаем максимальное значение

        function enforceMaxAndUpdate() {
            let quantity = parseInt(ticketsInput.value);

            // Проверка на NaN
            if (isNaN(quantity) || quantity < 1) {
                quantity = 1;
            }

            // ПРИНУДИТЕЛЬНО ограничиваем максимальным значением
            if (quantity > maxTickets) {
                quantity = maxTickets;
            }

            // Устанавливаем исправленное значение обратно в поле
            ticketsInput.value = quantity;

            // Обновляем сумму
            totalPriceSpan.textContent = (pricePerTicket * quantity).toLocaleString() + ' ₽';
        }

        // Срабатывает при каждом изменении значения
        ticketsInput.addEventListener('input', enforceMaxAndUpdate);

        // Срабатывает когда поле теряет фокус
        ticketsInput.addEventListener('blur', enforceMaxAndUpdate);

        // Срабатывает при нажатии клавиш (дополнительная защита)
        ticketsInput.addEventListener('keyup', enforceMaxAndUpdate);

        // Инициализация
        enforceMaxAndUpdate();
    }
});