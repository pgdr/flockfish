import requests

PATH = '127.0.0.1'
PORT = '6464'

def get(moves, field=None):
    url = 'http://{}:{}'.format(PATH, PORT)
    resp = requests.get(url=url,
                        params={'moves': ' '.join(moves)})
    data = resp.json()
    if field is None:
        return data
    return data[field]

def play(n=10):
    moves = []
    for i in range(n):
        bestmove = get(moves, field='bestmove')
        print(bestmove)
        moves.append(bestmove)
    return moves

def board(moves):
    return get(moves, field='board')

if __name__ == '__main__':
    moves = play()
    print('\n'.join(board(moves)))
