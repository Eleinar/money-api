import requests
from PySide6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtCore import QTimer

class CurrentRates(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Курсы валют ЦБ РФ")
        self.setGeometry(100, 100, 600, 400)
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Валюта", "Номинал", "Курс"])
        
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_rates)
        self.timer.start(60000)  # Обновление каждую минуту
        
        self.update_rates()
        
    def update_rates(self):
        try:
            response = requests.get("https://127.0.0.1:8001/current-rates")
            response.raise_for_status()  # Проверяем, что запрос успешен
            data = response.json()
            
            self.table.setRowCount(len(data))
            for i, (code, rate) in enumerate(data.items()):
                self.table.setItem(i, 0, QTableWidgetItem(rate['Name']))
                self.table.setItem(i, 1, QTableWidgetItem(str(rate['Nominal'])))
                self.table.setItem(i, 2, QTableWidgetItem(str(rate['Value'])))
            
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при запросе к серверу: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении данных: {e}")