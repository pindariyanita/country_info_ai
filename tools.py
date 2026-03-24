import requests

def fetch_country_data(country: str):
    try:
        country = country.strip().title()

        url = f"https://restcountries.com/v3.1/name/{country}"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return {"error": "Country not found"}

        data = response.json()
        return data[0]

    except Exception as e:
        return {"error": str(e)}