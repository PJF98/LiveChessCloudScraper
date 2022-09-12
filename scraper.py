import json
import urllib.request

tournament = 'a42d785d-fa38-421e-9c48-34902021636c'
num_rounds = 9

with urllib.request.urlopen("http://1.pool.livechesscloud.com/get/{}/tournament.json".format(tournament)) as url:
    tournament_data = json.load(url)

headers = []
headers.append('[Event \"{}\"]'.format(tournament_data['name']))
headers.append('[Site \"{}\"]'.format(tournament_data['location']))

for i in range(num_rounds):
    with urllib.request.urlopen("http://1.pool.livechesscloud.com/get/{}/round-{}/index.json".format(tournament, str(i+1))) as url:
        round_data = json.load(url)
    if i == 0:
        headers.append('[EventDate \"{}\"]'.format(round_data['date']))
        event_date = round_data['date']
    headers = headers[:3]
    headers.append('[Date \"{}\"]'.format(round_data['date']))
    for j, data in enumerate(round_data['pairings']):
        print('Round: {}, Board:{}'.format(i+1, j+1))
        headers = headers[:4]
        headers.append('[Board \"{}\"]'.format(j+1))
        headers.append('[White \"{}, {}\"]'.format(data['white']['lname'], data['white']['fname']))
        headers.append('[Black \"{}, {}\"]'.format(data['black']['lname'], data['black']['fname']))
        headers.append('[Result \"{}\"]'.format(data['result']))
        with urllib.request.urlopen("http://1.pool.livechesscloud.com/get/{}/round-{}/game-{}.json".format(tournament, str(i+1), str(j+1))) as url:
            move_data = json.load(url)
        moves = [i.split()[0] for i in move_data['moves']]
        movestr = ''
        for k in range(len(moves)):
            if k%2 == 0:
                movestr += str(round(k/2 + 1)) + '. '
            movestr += moves[k] + ' '
        movestr += data['result']
        with open('{}_{}.pgn'.format(tournament_data['name'], event_date), 'a') as f:
            f.writelines(headers)
            f.write('\n\n')
            f.write(movestr)
            f.write('\n\n')


