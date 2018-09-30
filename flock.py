#!/usr/bin/env python
from __future__ import print_function
import subprocess
from flask import Flask, jsonify, request


class Stockfish(object):
    PATH_TO_STOCKFISH = 'stockfish'

    def __init__(self):
        self._cmd = [Stockfish.PATH_TO_STOCKFISH]
        self._stf = subprocess.Popen(self._cmd,
                                    stdout=subprocess.PIPE,
                                    stdin=subprocess.PIPE)

    def _write(self, cmd):
        self._stf.stdin.write(cmd)
        self._stf.stdin.write('\n')

    def read_until(self, stopcriteria):
        output = []
        for line in iter(self._stf.stdout.readline, b''):
            line = line.rstrip()
            output.append(line)
            print(">>> " + line)
            if stopcriteria(line):
                break
        return output

    def go(self):
        self._write('go')

    def brd(self):
        self._write('d')

    def pos(self, fen=None, moves=None):
        wstr = 'position'
        if fen is None:
            fen = 'startpos'
        else:
            fen = 'fen {}'.format(fen)
        if moves is not None:
            moves = 'moves {}'.format(moves)
        self._write('position {} {}'.format(fen, moves).strip())


def get_board(fen=None, moves=None):
    stf = Stockfish()
    stf.pos(fen=fen, moves=moves)
    stf.brd()

    output = stf.read_until(lambda line: 'Checkers' in line)
    brd = []
    for line in output:
        line = line.strip()
        if line and line[0] in ('|', '+'):
            brd.append(line)
    return brd

def get_bestmove(fen=None, moves=None):
    stf = Stockfish()
    stf.pos(fen=fen, moves=moves)
    stf.go()

    output = stf.read_until(lambda line: 'bestmove' in line)[-1]
    return output.split()[1]

def get_fen(fen=None, moves=None):
    stf = Stockfish()
    stf.pos(fen=fen, moves=moves)
    stf.brd()
    output = stf.read_until(lambda line: 'Fen' in line)[-1]
    return output[5:]  # - "Fen: "


app = Flask('Flockfish')

@app.route('/bestmove/', methods=['GET'])
def route_next():
    fen_ = request.args.get('fen')
    moves_ = request.args.get('moves')
    return jsonify({'bestmove': get_bestmove(fen=fen_, moves=moves_)})

@app.route('/fen/', methods=['GET'])
def route_fenstring():
    fen_ = request.args.get('fen')
    moves_ = request.args.get('moves')
    return jsonify({'fen': get_fen(fen=fen_, moves=moves_)})

@app.route('/board/', methods=['GET'])
def route_board():
    fen_ = request.args.get('fen')
    moves_ = request.args.get('moves')
    return jsonify({'board': get_board(fen=fen_, moves=moves_)})

@app.route('/', methods=['GET'])
def route_all():
    fen_ = request.args.get('fen')
    moves_ = request.args.get('moves')
    return jsonify({'board': get_board(fen=fen_, moves=moves_),
                    'bestmove': get_bestmove(fen=fen_, moves=moves_),
                    'fen': get_fen(fen=fen_, moves=moves_)})


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 2:
        exit('Usage: python flock.py [stockfish]')
    if len(sys.argv) == 2:
        Stockfish.PATH_TO_STOCKFISH = sys.argv[1]
    app.run(host='0.0.0.0', port=6464)
