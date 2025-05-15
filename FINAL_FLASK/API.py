import requests


API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjA4ZTJkMzBlLTI3Y2YtNGE0YS1iMDM4LTQxYjNjMjMxNTQ2YiIsImlhdCI6MTc0NTY1ODAyMCwic3ViIjoiZGV2ZWxvcGVyLzRjYWE5M2ViLTBkMjctMzkwOC03Y2M5LWU5MjVlN2VhODY5NSIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIzMS4xODIuMjA3LjcxIl0sInR5cGUiOiJjbGllbnQifV19.jk49eZ5nUcaFIlKMMgZYITuqRUvxOGzfRpEM5_FIbcKAxsuDQaE3fOgtpeb1bKnwUVcHdyiBc3yUUbOvY8TQBg"
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}'
}


def get_all_cards():
    url = 'https://api.clashroyale.com/v1/cards'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()['items']  # повертає лише список карт
    else:
        raise Exception("Не вдалося отримати карти.")

    # for card in cards:
    #      name = card.get('name', 'Unknown card')
    #      rarity = card.get('rarity', 'Unknown rarity')
    #      print(f"Name: {name}, rarity: {rarity}")

    return cards


print(get_all_cards())