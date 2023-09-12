import sqlite3
import matplotlib.pyplot as plt

# open data.sqlite as read-only
conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()

def get_scaled(subject_id: int, score: int) -> int:
    cur.execute('SELECT scaled_score FROM Scores WHERE subject_id = ? AND score = ?', (subject_id, score))
    result = cur.fetchone()
    if result is None:
        return 0
    return result[0]

def get_all_scaled(subject_id: int) -> list:
    cur.execute('SELECT scaled_score FROM Scores WHERE subject_id = ?', (subject_id,))
    result = cur.fetchall()
    if result is None:
        return []
    return [x[0] for x in result]

def get_subject_name(subject_id: int) -> str:
    cur.execute('SELECT name FROM Scores WHERE subject_id = ? AND score = ?', (subject_id, 50))
    result = cur.fetchone()
    if result is None:
        return 'No name found'
    return result[0]

def get_subject_id(subject_name: str) -> int:
    cur.execute('SELECT subject_id FROM Scores WHERE name = ? AND score = ?', (subject_name, 50))
    result = cur.fetchone()
    if result is None:
        return 0
    return result[0]

digital_solutions_scaled = get_all_scaled(get_subject_id('Digital Solutions'))
biology_scaled = get_all_scaled(get_subject_id('Biology'))
psychology_scaled = get_all_scaled(get_subject_id('Psychology'))

plt.plot(range(1, 101), digital_solutions_scaled, label='Digital Solutions')
plt.plot(range(1, 101), biology_scaled, label='Biology')
plt.plot(range(1, 101), psychology_scaled, label='Psychology')

plt.legend()
plt.savefig('digital_solutions_vs_biology_vs_psychology.png')