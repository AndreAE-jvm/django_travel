function addToWishlist(element, event, eventId) {
    event.preventDefault();

    console.log('НАЧАЛО ДОБАВЛЕНИЯ ');
    console.log('Добавление в избранное:', eventId);

    // Проверяем начальное состояние
    console.log('Начальные классы элемента:', element.className);
    console.log('Начальный цвет:', window.getComputedStyle(element).color);

    // Находим контейнер
    const container = element.closest('.wishlist-icon-container');
    console.log('Контейнер найден:', container);

    if (container) {
        console.log('Классы контейнера ДО:', container.className);
        container.classList.add('has-filled');
        console.log('Классы контейнера ПОСЛЕ:', container.className);
        console.log('Opacity контейнера:', window.getComputedStyle(container).opacity);
    }

    // Меняем сердечко на красное сразу при нажатии
    element.classList.remove('wishlist-heart');
    element.classList.add('wishlist-heart-filled');
    console.log('Классы элемента ПОСЛЕ изменения:', element.className);

    const heartIcon = element.querySelector('i');
    heartIcon.className = 'bi bi-heart-fill';

    console.log('Цвет элемента ПОСЛЕ:', window.getComputedStyle(element).color);
    console.log('=== ОТПРАВКА ЗАПРОСА ===');

    // Получаем CSRF-токен
    const csrftoken = getCookie('csrftoken');

    // Отправляем запрос на сервер
    fetch(`/events/wishlist/add/${eventId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Ответ сервера:', data);
        if (data.success) {
            console.log(' УСПЕХ - обновляем ссылку');
            element.href = `/events/wishlist/remove/${data.wishlist_id}/`;
            element.title = 'Убрать из избранного';
            element.setAttribute('data-wishlist-id', data.wishlist_id);

            element.onclick = function(e) {
                e.preventDefault();
                if (confirm('Убрать из избранного?')) {
                    removeFromWishlist(this, e, data.wishlist_id);
                }
                return false;
            };

            showNotification('success', 'Добавлено в избранное');
        } else {
            console.log(' ОШИБКА - возвращаем как было');
            if (container) {
                container.classList.remove('has-filled');
            }
            element.classList.remove('wishlist-heart-filled');
            element.classList.add('wishlist-heart');
            heartIcon.className = 'bi bi-heart';
            showNotification('error', 'Ошибка при добавлении');
        }
    })
    .catch(error => {
        console.error(' ОШИБКА:', error);
        if (container) {
            container.classList.remove('has-filled');
        }
        element.classList.remove('wishlist-heart-filled');
        element.classList.add('wishlist-heart');
        heartIcon.className = 'bi bi-heart';
        showNotification('error', 'Ошибка при добавлении');
    });

    return false;
}