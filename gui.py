import requests
from PySide6.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QMessageBox,
    QComboBox, QLineEdit, QPushButton, QLabel, QHBoxLayout, QFormLayout
)
from PySide6.QtCore import QTimer

class CurrentRates(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Курсы валют ЦБ РФ")
        self.setGeometry(100, 100, 600, 500)

        # Таблица с курсами валют
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Валюта", "Номинал", "Курс"])

        # Конвертер валют
        self.from_currency = QComboBox(self)
        self.to_currency = QComboBox(self)
        self.amount_input = QLineEdit(self)
        self.convert_button = QPushButton("Конвертировать", self)
        self.result_label = QLabel("Результат: ", self)

        # Настройка интерфейса
        layout = QVBoxLayout()
        layout.addWidget(self.table)

        # Форма для конвертера
        converter_layout = QFormLayout()
        converter_layout.addRow("Из валюты:", self.from_currency)
        converter_layout.addRow("В валюту:", self.to_currency)
        converter_layout.addRow("Сумма:", self.amount_input)
        converter_layout.addRow(self.convert_button)
        converter_layout.addRow(self.result_label)

        layout.addLayout(converter_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Таймер для обновления данных
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_rates)
        self.timer.start(60000)  # Обновление каждую минуту

        # Инициализация данных
        self.update_rates()

        # Подключение кнопки конвертации
        self.convert_button.clicked.connect(self.convert_currency)

    def update_rates(self):
        try:
            response = requests.get("http://127.0.0.1:8001/current-rates")
            response.raise_for_status()  # Проверяем, что запрос успешен
            data = response.json()

            # Обновление таблицы
            self.table.setRowCount(len(data))
            for i, (code, rate) in enumerate(data.items()):
                self.table.setItem(i, 0, QTableWidgetItem(rate['Name']))
                self.table.setItem(i, 1, QTableWidgetItem(str(rate['Nominal'])))
                self.table.setItem(i, 2, QTableWidgetItem(str(rate['Value'])))

            # Обновление списков валют
            self.from_currency.clear()
            self.to_currency.clear()
            for code in data.keys():
                self.from_currency.addItem(code)
                self.to_currency.addItem(code)

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при запросе к серверу: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении данных: {e}")

    def convert_currency(self):
        try:
            # Получаем данные для конвертации
            from_currency = self.from_currency.currentText()
            to_currency = self.to_currency.currentText()
            amount = float(self.amount_input.text())

            # Получаем текущие курсы
            response = requests.get("http://127.0.0.1:8000/current-rates")
            response.raise_for_status()
            data = response.json()

            # Выполняем конвертацию
            from_rate = data[from_currency]['Value'] / data[from_currency]['Nominal']
            to_rate = data[to_currency]['Value'] / data[to_currency]['Nominal']
            result = (amount * from_rate) / to_rate

            # Отображаем результат
            self.result_label.setText(f"Результат: {result:.2f} {to_currency}")

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректное число для суммы.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при запросе к серверу: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при конвертации: {e}")

