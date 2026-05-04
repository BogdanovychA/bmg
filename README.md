# Мініігри (Bogdanovych's MiniGames)

![Made in Ukraine](https://img.shields.io/badge/Made%20in-Ukraine-blue?logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMjAwIiBoZWlnaHQ9IjgwMCI%2BCjxyZWN0IHdpZHRoPSIxMjAwIiBoZWlnaHQ9IjgwMCIgZmlsbD0iIzAwNTdCNyIvPgo8cmVjdCB3aWR0aD0iMTIwMCIgaGVpZ2h0PSI0MDAiIHk9IjQwMCIgZmlsbD0iI0ZGRDcwMCIvPgo8L3N2Zz4%3D)

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
