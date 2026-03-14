document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM загружен, начинаем анимацию...');

    // Плавное появление страницы
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 1s ease-in-out';

    setTimeout(() => {
        console.log('Запускаем анимацию появления...');
        document.body.style.opacity = '1';
    }, 450);

    // Инициализация всех функций
    initDatePicker();
    initSmoothScroll();
    initNavbarScroll();
});

/* Инициализация календаря для выбора дат */
function initDatePicker() {
    const dateInput = document.getElementById('date-range');
    const dateFrom = document.getElementById('date_from');
    const dateTo = document.getElementById('date_to');

    if (!dateInput) return;

    // Проверяем, подключен ли flatpickr
    if (typeof flatpickr === 'undefined') {
        console.warn('flatpickr не подключен, загружаем...');
        loadFlatpickr();
        return;
    }

    initFlatpickr(dateInput, dateFrom, dateTo);
}

/* Загрузка flatpickr динамически*/
function loadFlatpickr() {
    // Подключаем CSS
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css';
    document.head.appendChild(link);

    // Подключаем JS
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/flatpickr';
    script.onload = function() {
        // Подключаем русский язык
        const langScript = document.createElement('script');
        langScript.src = 'https://cdn.jsdelivr.net/npm/flatpickr/dist/l10n/ru.js';
        langScript.onload = function() {
            const dateInput = document.getElementById('date-range');
            const dateFrom = document.getElementById('date_from');
            const dateTo = document.getElementById('date_to');
            initFlatpickr(dateInput, dateFrom, dateTo);
        };
        document.head.appendChild(langScript);
    };
    document.head.appendChild(script);
}

/*
 * Инициализация flatpickr */
function initFlatpickr(input, fromField, toField) {
    // Если есть сохраненные даты, показываем их
    let defaultDate = [];
    if (fromField.value && toField.value) {
        // Преобразуем YYYY-MM-DD в объекты Date
        defaultDate = [new Date(fromField.value), new Date(toField.value)];
    }

    flatpickr(input, {
        mode: "range",           // Режим выбора диапазона
        locale: "ru",            // Русский язык
        dateFormat: "d.m.Y",     // Формат отображения
        altFormat: "d.m.Y",
        altInput: true,
        minDate: "today",        // Нельзя выбрать прошедшие даты
        defaultDate: defaultDate,
        showMonths: 2,           // Показывать 2 месяца
        disableMobile: true,     // Отключаем мобильный вид для единообразия

        onChange: function(selectedDates, dateStr, instance) {
            if (selectedDates.length === 2) {
                // Форматируем даты для сервера (YYYY-MM-DD)
                const startDate = formatDateForServer(selectedDates[0]);
                const endDate = formatDateForServer(selectedDates[1]);

                fromField.value = startDate;
                toField.value = endDate;

                console.log('Выбраны даты:', startDate, 'до', endDate);
            } else if (selectedDates.length === 1) {
                // Если выбрана только одна дата
                const startDate = formatDateForServer(selectedDates[0]);
                fromField.value = startDate;
                toField.value = '';
            } else {
                // Если даты не выбраны
                fromField.value = '';
                toField.value = '';
            }
        },

        // Кастомный индикатор загрузки
        onReady: function() {
            console.log('Календарь готов');
        }
    });
}

/* Форматирование даты для сервера (YYYY-MM-DD) */
function formatDateForServer(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

/* Плавная прокрутка к якорям */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const target = document.querySelector(targetId);
            if (target) {
                const navbarHeight = document.querySelector('.navbar')?.offsetHeight || 0;
                window.scrollTo({
                    top: target.offsetTop - navbarHeight - 20,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/* Изменение навигации при скролле */
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('bg-white', 'shadow-sm');
            } else {
                navbar.classList.remove('bg-white', 'shadow-sm');
            }
        });
    }
}