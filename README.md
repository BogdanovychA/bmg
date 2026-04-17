# Мініігри (Bogdanovych's MiniGames)

⚠️ **Увага:** Застосунок знаходиться **в розробці**. У вільний час я вивчаю Python і розважаюся із написанням коду. 😎

## Корисні посилання

## Грати

* [Веб-версія](https://minigames.bogdanovych.org/)
* [Android (Google Play)](https://play.google.com/store/apps/details?id=org.foundation101.minigames)

## Інше

* [Підтримати проєкт](https://send.monobank.ua/jar/8Qn1woNnC7)

## 🚀 Встановлення

### Вимоги
- Python 3.12 або новіше

### Запуск
```bash
# 1. Клонуйте репозиторій
git clone https://github.com/BogdanovychA/bmg
cd bmg

# 2. Створіть оточення та встановіть залежності (Python підтягнеться автоматично)
uv sync

# 3. Налаштуйте pre-commit хуки (для розробки)
uv run pre-commit install
# опційно: uv run pre-commit run --all-files

# 4. Запустіть застосунок
uv run flet run     # опційно з ключем  --web
