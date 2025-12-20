# Техническое задание (ТЗ) на разработку проекта wShop

## 1. Общее описание проекта

Название проекта: wShop

Цель: Разработка интернет-магазина премиальных оправ для очков с использованием современного стека технологий Python/Django и интерактивного фронтенда без использования тяжелых JS-фреймворков (React/Vue).

Ключевая особенность: Реализация пользовательского опыта Single Page Application (SPA) посредством библиотеки HTMX, обеспечивающей плавные переходы и динамическое обновление контента без полной перезагрузки страницы.

Язык интерфейса: Английский.

## 2. Технологический стек

### Backend

- **Язык:** Python 3.11+
    
- **Фреймворк:** Django 5.x
    
- **База данных:** PostgreSQL 16
    
- **Архитектурный паттерн:** MVT (Model-View-Template) с элементами сервисной архитектуры (Services Layer).
    

### Frontend

- **HTML-движок:** Django Templates
    
- **Интерактивность:** HTMX (AJAX-запросы, HTML-swapping)
    
- **State Management/UI Logic:** Alpine.js (для модальных окон, дропдаунов, локальных состояний UI)
    
- **Стилизация:** Tailwind CSS (utility-first подход)
    

### Инфраструктура и Инструменты

- **Контейнеризация:** Docker, Docker Compose
    
- **Web Server:** Nginx (как reverse proxy и раздача статики)
    
- **Платежный шлюз:** NOWPayments API
    
- **WSGI Server:** Gunicorn
    

## 3. Функциональные требования

### 3.1. Каталог продукции

- **Список товаров:** Отображение сетки товаров с пагинацией (infinite scroll или кнопка "Load More" через HTMX).
    
- **Фильтрация:** Динамическая фильтрация по категориям, цене, материалу и бренду без перезагрузки страницы.
    
- **Поиск:** Живой поиск по названию модели.
    

### 3.2. Детальная страница товара (PDP)

- Галерея изображений.
    
- Описание, характеристики.
    
- Кнопка "Add to Cart" (AJAX-запрос с обновлением счетчика корзины).
    

### 3.3. Корзина (Shopping Cart)

- **UI:** Реализация в виде модального окна (Alpine.js `x-data="{ open: false }"`).
    
- **Действия:** Изменение количества товаров, удаление позиции, автоматический пересчет итоговой суммы.
    
- **Синхронизация:** Состояние корзины хранится в сессии (для гостей) или в БД (для авторизованных).
    

### 3.4. Оформление заказа (Checkout)

- Форма ввода данных доставки.
    
- Валидация данных на лету.
    
- Создание сущности `Order` в статусе `Pending`.
    

### 3.5. Оплата

- Интеграция с NOWPayments.
    
- Генерация платежной ссылки или QR-кода.
    
- Обработка Webhook от платежной системы для смены статуса заказа на `Paid`.
    

## 4. Нефункциональные требования

- **Code Quality:** Строгое соблюдение PEP8. Использование Type Hints. Принцип DRY (Don't Repeat Yourself).
    
- **Clean Code:** Код должен быть самодокументируемым. **Комментарии в коде запрещены**(согласно требованию), ясность достигается за счет корректного нейминга переменных и функций.
    
- **Безопасность:** Защита от CSRF (Django middleware), SQL Injection (использование ORM), XSS (экранирование шаблонов). Хранение секретов (API keys, DB credentials) только в переменных окружения (`.env`).
    
- **Производительность:** Оптимизация SQL-запросов (`select_related`, `prefetch_related`) для решения проблемы N+1.
    
- **SPA Feel:** Все навигационные ссылки должны обрабатываться через `hx-boost="true"` или целевые HTMX-запросы.
    

## 5. Структура базы данных (Schema Design)

Предлагаемая схема (упрощенная нотация):

- **Users (CustomUser):** `email`, `password`, `is_active`, `is_staff`.
    
- **Categories:** `name`, `slug`, `parent` (для вложенности).
    
- **Products:** `category_id` (FK), `name`, `slug`, `description`, `price`, `stock`, `is_active`.
    
- **ProductImages:** `product_id` (FK), `image_url`, `is_main`.
    
- **Orders:** `user_id` (FK, nullable), `status` (new, paid, shipped, cancelled), `total_price`, `payment_id`(NOWPayments ID), `created_at`.
    
- **OrderItems:** `order_id` (FK), `product_id` (FK), `quantity`, `price_at_purchase`.
    

## 6. Структура проекта

Согласно вашему требованию, папка `src` устранена, проект `config` переименован в `wShop`, а приложения вынесены в корень для плоской структуры.

Plaintext

```
wShop/
├── .env.example              # Пример переменных окружения
├── .gitignore
├── docker-compose.yml        # Оркестрация сервисов
├── Dockerfile                # Сборка образа Django
├── manage.py                 # Точка входа Django
├── nginx/
│   └── nginx.conf            # Конфигурация Nginx
├── requirements.txt          # Зависимости Python
├── wShop/                    # Бывшая папка config (Project Settings)
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/                     # Django приложения (Apps)
│   ├── __init__.py
│   ├── catalog/              # Products, Categories, Filters
│   ├── cart/                 # Shopping cart
│   ├── orders/               # Order management
│   └── payments/             # NOWPayments integration logic
├── core/                     # Базовые классы, миксины, утилиты
├── services/                 # Слой бизнес-логики 
├── static/                   # Скомпилированная статика (CSS/JS/Images)
│   ├── css/
│   │   └── input.css         # Tailwind input
│   └── js/
│       └── app.js            # Alpine components init
└── templates/                # HTML Шаблоны
    ├── base.html             # Основной layout (hx-boost)
    ├── components/           # Переиспользуемые фрагменты
    ├── catalog/
    ├── cart/
    └── orders/
```

## 7. API Endpoints (Внутренние для HTMX)

В отличие от REST API, эти эндпоинты возвращают HTML-фрагменты.

- `GET /catalog/filter/?category=sun&price_max=200` — Возвращает обновленный HTML сетки товаров.
    
- `GET /cart/detail/` — Возвращает HTML содержимое модального окна корзины.
    
- `POST /cart/add/<product_id>/` — Добавляет товар, возвращает обновленный бейдж корзины (HX-OOB swap).
    
- `POST /cart/update/<item_id>/` — Обновляет кол-во, возвращает HTML строки товара и новую сумму.
    
- `DELETE /cart/remove/<item_id>/` — Удаляет товар из DOM корзины.
    
- `POST /orders/create/` — Валидирует форму. При успехе возвращает редирект или HTML с подтверждением и кнопкой оплаты.
    

## 8. Docker конфигурация

**Сервисы:**

1. **db:** Образ `postgres:16-alpine`. Volume для персистентности данных.
    
2. **web:** Django приложение (Gunicorn). Зависит от `db`.
    
3. **nginx:** Образ `nginx:alpine`. Проксирует запросы на порт 8000 (web), раздает `/static/` и `/media/`.
    

## 9. Deliverables (Результаты работы)

1. Полный исходный код в Git-репозитории.
    
2. Настроенный `Dockerfile` и `docker-compose.yml` для запуска одной командой (`docker-compose up --build`).
    
3. Файл `requirements.txt` с зафиксированными версиями библиотек.
    
4. Скрипт или инструкция для наполнения базы данных тестовыми товарами (Fixtures).
    

## 10. Критерии приемки

1. **SPA Experience:** Переходы между каталогом и детальной страницей происходят без мигания экрана (full page reload).
    
2. **Cart Interaction:** Добавление товара в корзину обновляет счетчик в хедере без перезагрузки. Модальное окно корзины открывается/закрывается корректно.
    
3. **Payment Flow:** Тестовая транзакция через NOWPayments Sandbox проходит успешно, статус заказа в админке меняется автоматически.
    
4. **Responsive:** Сайт корректно отображается на мобильных устройствах и десктопах (Tailwind breakpoints).
    
5. **Code Style:** Код проходит проверку линтерами (flake8/black), отсутствуют закомментированные участки кода и текстовые комментарии.