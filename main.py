from PySide6.QtWidgets import QApplication
from gui import CurrentRates
import threading
import uvicorn
import api  # Импортируем api для запуска сервера
import time

# Функция для запуска сервера FastAPI
def run_fastapi():
    uvicorn.run(api.app, host="0.0.0.0", port=8001)

# Запуск сервера в отдельном потоке
fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
fastapi_thread.start()

# Даем серверу время на запуск
time.sleep(2)

# Запуск графического интерфейса
app = QApplication([])
window = CurrentRates()
window.show()
app.exec()