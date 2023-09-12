import sqlite3
import requests

# Function to get score for a subject and score combination
def get_score(subject_id: int, score: int) -> int:
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    data = "score[{}]={}".format(subject_id, score)

    response = requests.get('https://qce.atarcalc.com/api/calculate.json', data=data, headers=headers)
    try:
        result = response.json()
        scaled_2022 = result['subjects'][0]['scaled']['2022']
        return scaled_2022
    except Exception as e:
        print(f'Error fetching score for Subject {subject_id}, Score {score}: {response.text}')
        return 0

# Function to get subject name
def get_name(subject_id: int) -> str:
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = "score[{}]={}".format(subject_id, 50)

    response = requests.get('https://qce.atarcalc.com/api/calculate.json', data=data, headers=headers)
    try:
        result = response.json()
        name = result['subjects'][0]['name']
        return name
    except Exception as e:
        print(f'Error fetching name for Subject {subject_id}: {response.text}')
        return 'No name found'

# Create a new database
conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()

# Populate the table with all 150 subjects and scores
for subject_id in range(26, 151):
    subject_name = get_name(subject_id)
    for score in range(1, 101):
        score_value = get_score(subject_id, score)
        cur.execute('INSERT INTO Scores (subject_id, name, score, scaled_score) VALUES (?, ?, ?, ?)', (subject_id, subject_name, score, score_value))
        conn.commit()
    print('Finished subject_id {i}'.format(i=subject_id))

# Close the connection when done
conn.close()
