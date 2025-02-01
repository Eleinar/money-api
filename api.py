from fastapi import FastAPI, HTTPException
import requests
import uvicorn

app = FastAPI()

def get_current_rates():
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    try:
        # Отключаем проверку SSL
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Проверяем, что запрос успешен
        data = response.json()
        print("Ответ от API ЦБ РФ:", data)  # Логируем ответ
        if 'Valute' not in data:
            raise ValueError("Ключ 'Valute' отсутствует в ответе от API ЦБ РФ")
        return data['Valute']
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API ЦБ РФ: {e}")  # Логируем ошибку
        raise HTTPException(status_code=500, detail=f"Ошибка при запросе к API ЦБ РФ: {e}")
    except ValueError as e:
        print(f"Ошибка в данных от API ЦБ РФ: {e}")  # Логируем ошибку
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/current-rates")
def read_current_rates():
    try:
        currencies = get_current_rates()
        selected_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'CHF', 'AUD', 'CAD', 'RUB', 'NOK']
        result = {code: currencies[code] for code in selected_currencies if code in currencies}
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)