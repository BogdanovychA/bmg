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
git clone https://github.com/BogdanovychA/bmg
cd bmg
python3 -m venv .venv       # або 'python.exe -m venv .venv' на Windows
source .venv/bin/activate      # або '.venv\Scripts\activate.bat' чи '.venv\Scripts\Activate.ps1' на Windows
pip install -r requirements.txt
pre-commit install       # або 'pre-commit.exe install' на Windows
pre-commit run --all-files       # опційно; на Windows: 'pre-commit.exe run --all-files'
flet run       # або 'flet run --web '