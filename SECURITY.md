# Рекомендації з безпеки

## Огляд безпеки проєкту

Цей документ описує заходи безпеки, що застосовуються в проєкті, та рекомендації для безпечного розгортання та використання.

---

## Оглянуті загрози та захисні заходи

### 1. Cross-Site Scripting (XSS)

**Загроза**: Впровадження зловмисного JavaScript коду через вхідні поля.

**Захисні заходи**:
- ✅ Використання `html.escape()` для санітизації всіх вхідних даних користувача
- ✅ Впроваджено модуль `validation.py` з функцією `sanitize_html()`
- ✅ Jinja2 автоматично екранує змінні в шаблонах
- ✅ Валідація всіх форм на сервері

**Рекомендації**:
- Завжди використовуйте `val.sanitize_html()` для текстових полів перед збереженням
- Не використовуйте `|safe` фільтр Jinja2 без необхідності
- Перевіряйте вхідні дані на патерни атак

### 2. SQL Injection

**Загроза**: Впровадження SQL коду через параметри запитів.

**Захисні заходи**:
- ✅ Використання параметризованих запитів в SQLite
- ✅ Всі запити до БД використовують placeholders (?)
- ✅ Відсутність динамічного конструювання SQL з вхідних даних

**Приклад безпечного коду**:
```python
# ✅ Правильно - параметризований запит
cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))

# ❌ Неправильно - небезпечна конкатенація
cursor.execute(f'SELECT * FROM products WHERE id = {product_id}')
```

### 3. Валідація вхідних даних

**Захисні заходи**:
- ✅ Серверна валідація всіх форм
- ✅ Модуль `validation.py` з функціями перевірки:
  - `validate_email()` - перевірка формату email
  - `validate_phone()` - перевірка номера телефону
  - `validate_name()` - перевірка імені (тільки літери)
  - `validate_rating()` - перевірка оцінки (1-5)
  - `validate_text_length()` - перевірка довжини тексту
  - `validate_price()` - перевірка ціни
  - `validate_stock()` - перевірка кількості на складі

**Застосування**:
```python
# Валідація email
if not val.validate_email(email):
    flash('Некоректна email адреса', 'error')
    return redirect(url_for('checkout'))
```

### 4. Аутентифікація та авторизація

**Поточний стан**:
- ⚠️ Базова аутентифікація для адмін-панелі
- ⚠️ Credentials зберігаються в коді (тільки для розробки)

**Рекомендації для production**:
```python
# ❌ Не використовувати в production
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

# ✅ Використовувати змінні оточення
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD_HASH = os.environ.get('ADMIN_PASSWORD_HASH')

# ✅ Хешування паролів
from werkzeug.security import generate_password_hash, check_password_hash
password_hash = generate_password_hash(password)
if check_password_hash(password_hash, provided_password):
    # Вхід дозволено
```

### 5. Управління сесіями

**Захисні заходи**:
- ✅ Використання `os.urandom(24)` для секретного ключа сесії
- ✅ HTTP-only cookies (за замовчуванням у Flask)
- ✅ Автоматичне очищення кошика після оформлення замовлення

**Рекомендації для production**:
```python
# ✅ Встановіть секретний ключ через змінні оточення
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# ✅ Налаштуйте безпечні cookies для HTTPS
app.config.update(
    SESSION_COOKIE_SECURE=True,  # Тільки HTTPS
    SESSION_COOKIE_HTTPONLY=True,  # Захист від XSS
    SESSION_COOKIE_SAMESITE='Lax',  # Захист від CSRF
)
```

### 6. Захист від CSRF (Cross-Site Request Forgery)

**Поточний стан**:
- ⚠️ CSRF токени не впроваджені

**Рекомендації для production**:
```python
# Встановити Flask-WTF для захисту від CSRF
pip install Flask-WTF

# Конфігурація
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# У шаблонах
<form method="POST">
    {{ csrf_token() }}
    <!-- інші поля -->
</form>
```

---

## Конфігурація для production

### Змінні оточення

Створіть файл `.env` (НЕ комітьте його в git!):
```bash
# Flask конфігурація
SECRET_KEY=your-very-long-random-secret-key-here
FLASK_ENV=production
FLASK_DEBUG=False

# Адмін credentials
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD_HASH=your_hashed_password

# База даних
DATABASE_PATH=/app/data/store.db

# Email (для сповіщень)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

### Генерація безпечного SECRET_KEY

```python
import secrets
secret_key = secrets.token_hex(32)
print(f"SECRET_KEY={secret_key}")
```

### Docker Security

**Рекомендації для Dockerfile**:
```dockerfile
# Не запускайте як root
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Обмежте права доступу
RUN chmod 700 /app/data

# Використовуйте read-only файлову систему
docker run --read-only -v /tmp:/tmp myapp
```

---

## Моніторинг та логування

### Налаштування логування

```python
import logging
from logging.handlers import RotatingFileHandler

# Налаштування логера
handler = RotatingFileHandler('app.log', maxBytes=10000000, backupCount=3)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# Логування важливих подій
app.logger.info('Нове замовлення створено: %s', order_id)
app.logger.warning('Невдала спроба входу: %s', username)
app.logger.error('Помилка БД: %s', str(e))
```

### Що логувати:

**✅ Логувати**:
- Спроби входу (успішні та невдалі)
- Створення/оновлення/видалення записів
- Помилки та винятки
- Зміни критичних налаштувань

**❌ НЕ логувати**:
- Паролі (навіть хешовані)
- Номери кредитних карток
- Персональні дані користувачів
- Секретні ключі

---

## Резервне копіювання

### Стратегія backup БД

```bash
#!/bin/bash
# Автоматичний backup SQLite

BACKUP_DIR="/backups"
DB_PATH="/app/data/store.db"
DATE=$(date +%Y%m%d_%H%M%S)

# Створення backup
sqlite3 $DB_PATH ".backup '$BACKUP_DIR/store_$DATE.db'"

# Видалення старих backup (зберігати 7 днів)
find $BACKUP_DIR -name "store_*.db" -mtime +7 -delete

echo "Backup створено: store_$DATE.db"
```

**Налаштування cron**:
```bash
# Backup кожні 6 годин
0 */6 * * * /path/to/backup_script.sh
```

---

## Оновлення залежностей

### Перевірка вразливостей

```bash
# Встановіть safety
pip install safety

# Перевірка вразливостей
safety check -r requirements.txt

# Оновлення залежностей
pip list --outdated
pip install --upgrade package_name
```

### Регулярні оновлення

- Перевіряйте безпекові патчі щомісяця
- Підписуйтеся на сповіщення GitHub Security Advisories
- Тестуйте оновлення в dev середовищі перед production

---

## Checklist перед production deployment

### Обов'язкові кроки:

- [ ] Змінити `SECRET_KEY` на унікальний
- [ ] Змінити адмін credentials з `admin/admin123`
- [ ] Вимкнути debug режим (`FLASK_DEBUG=False`)
- [ ] Налаштувати HTTPS/SSL сертифікати
- [ ] Увімкнути CSRF захист
- [ ] Налаштувати логування
- [ ] Налаштувати автоматичні backup
- [ ] Обмежити доступ до БД файлу
- [ ] Використати WSGI сервер (Gunicorn/uWSGI) замість Flask dev server
- [ ] Налаштувати reverse proxy (Nginx/Apache)
- [ ] Перевірити всі залежності на вразливості
- [ ] Налаштувати rate limiting
- [ ] Налаштувати моніторинг помилок (Sentry)

### Додаткові покращення:

- [ ] Впровадити двофакторну аутентифікацію для адмінів
- [ ] Додати captcha на формах
- [ ] Налаштувати Web Application Firewall (WAF)
- [ ] Впровадити Content Security Policy (CSP)
- [ ] Додати email верифікацію при реєстрації
- [ ] Налаштувати rate limiting для API endpoints

---

## Повідомлення про вразливості

Якщо ви знайшли вразливість у безпеці, будь ласка:

1. **НЕ** створюйте публічний issue
2. Надішліть email на: security@shop.ua
3. Опишіть вразливість детально
4. Дайте час на виправлення (responsible disclosure)

Ми відповімо протягом 48 годин та випустимо патч якнайшвидше.

---

## Ресурси

### Корисні посилання:

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [SQLite Security](https://www.sqlite.org/security.html)

### Інструменти для тестування:

- **Bandit** - статичний аналізатор для Python
- **Safety** - перевірка вразливостей залежностей
- **OWASP ZAP** - тестування веб-безпеки
- **SQLMap** - тестування SQL injection

---

**Останнє оновлення**: 2024-12-19

**Версія**: 1.0

**Статус**: Рекомендації застосовані частково, потребують повної імплементації для production
