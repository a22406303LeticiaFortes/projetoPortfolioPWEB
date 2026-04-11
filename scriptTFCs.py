import requests

url = 'https://secure.ensinolusofona.pt/dados-publicos-academicos/resources/GetCourseDetail'
payload = {
    'language': 'PT',
    'courseCode': 12,
    'schoolYear': '202526'
}
headers = {'content-type': 'application/json'}

response = requests.post(url, json=payload, headers=headers, timeout=20)
print(response.status_code)
print(response.text[:500])