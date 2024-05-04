import requests


def fetch_data_from_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None


def get_random_data():
    api_url = "https://randomuser.me/api/"
    data = fetch_data_from_api(api_url)

    if data:
        results = data.get('results', [])[0]
        return results.get('email', {})
    else:
        return 'ERROR'


if __name__ == "__main__":
    print(get_random_data())
