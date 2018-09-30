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
        self.stdout = self._stf.stdout

    def _write(self, cmd):
        self._stf.stdin.write(cmd)
        self._stf.stdin.write('\n')

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

    brd = []
    for line in iter(stf.stdout.readline, b''):
        line = line.strip()
        if line and line[0] in ('|', '+'):
            brd.append(line)
        print(">>> " + line)
        if 'Checkers' in line:
            return brd

def get_bestmove(fen=None, moves=None):
    stf = Stockfish()
    stf.pos(fen=fen, moves=moves)
    stf.go()

    for line in iter(stf.stdout.readline, b''):
        line = line.rstrip()
        print(">>> " + line)
        if 'bestmove' in line:
            return line.split()[1]

def get_fen(fen=None, moves=None):
    stf = Stockfish()
    stf.pos(fen=fen, moves=moves)
    stf.brd()
    for line in iter(stf.stdout.readline, b''):
        line = line.strip()
        print(">>> " + line)
        if 'Fen' in line:
            return line[5:]


app = Flask('Flockfish')

@app.route('/bestmove/', methods=['GET'])
def route_next():
    fen_ = request.args.get('fen')
    moves_ = request.args.get('moves')
    return jsonify(get_bestmove(fen=fen_, moves=moves_))

@app.route('/fen/', methods=['GET'])
def route_fenstring():
    fen_ = request.args.get('fen')
    moves_ = request.args.get('moves')
    return jsonify(get_fen(fen=fen_, moves=moves_))

@app.route('/board/', methods=['GET'])
def route_board():
    fen_ = request.args.get('fen')
    moves_ = request.args.get('moves')
    return jsonify(get_board(fen=fen_, moves=moves_))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 2:
        exit('Usage: python flock.py [stockfish]')
    if len(sys.argv) == 2:
        Stockfish.PATH_TO_STOCKFISH = sys.argv[1]
    app.run(host='0.0.0.0', port=6464)
