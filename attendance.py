import requests


def main(group, date, status):
    url1 = f"https://api.marsit.uz/api/v1/attendance/{group}"
    url2 = 'https://api.marsit.uz/api/v1/attendance'
    params = {
        "group_id": group,
        "from_date": "2024-10-02",
        "till_date": "2024-10-02"
    }
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ3aG8iOjAsInN1YiI6IjMyMyIsImV4cCI6MTcyNzk1MjYyNH0.oFCV4fT1VOBbVJnZIpb27JmZ5Z-fWQwmo56yohshbic'

    header1 = {
        'Authorization': f'Bearer {token}'
    }
    header2 = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url1, headers=header1, params=params)
    if response.status_code == 200:
        data = response.json()
        son = 0
        for student in data['students']:
            son += 1
            student_id = student['student_id']
            data = {
                "date": date,
                "group_id": group,
                "student_id": student_id,
                "status": status
            }
            response = requests.post(url2, headers=header2, json=data)
            if response.status_code == 200:
                pass
            else:
                print(f"Request failed with status code {response.status_code}: {response.text}")
        print("groups attandance is successful")
    else:
        print(f"Error: {response.status_code}, {response.text}")

sana = 2
for i in range(sana):
    sana += 2
    print(main(655, f"2024-09-0{sana}", 1))