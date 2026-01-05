# Bogdanovych's Mini Games

⚠️ **Увага:** Застосунок знаходиться **в розробці**. У вільний час я вивчаю Python і розважаюся із написанням коду. 😎

## 📖 Опис

Грати: https://mini-games.bogdanovych.org/

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