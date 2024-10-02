import requests

url2 = 'https://api.marsit.uz/api/v1/attendance'

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ3aG8iOjAsInN1YiI6IjMyMyIsImV4cCI6MTcyNzk1MjYyNH0.oFCV4fT1VOBbVJnZIpb27JmZ5Z-fWQwmo56yohshbic'

header2 = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# List of dates from the image
# dates = ["2024-09-02", "2024-09-04", "2024-09-06", "2024-09-09",
#          "2024-09-11", "2024-09-13", "2024-09-16", "2024-09-18",
#          "2024-09-20", "2024-09-23", "2024-09-25", "2024-09-27",
#          "2024-09-30"]
#
# for date in dates:
data = {
    "date": "2024-09-27",
    "group_id": 1288,
    "student_id": 23936,
    "status": 0
}
response = requests.post(url2, headers=header2, json=data)
if response.status_code == 200:
    print(response.json())
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")
