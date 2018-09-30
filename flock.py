#!/usr/bin/env python
from __future__ import print_function
import subprocess
from flask import Flask, jsonify, request

PATH_TO_STOCKFISH = 'stockfish'

def _get_stockfish():
    cmd = [PATH_TO_STOCKFISH]
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE)
    return p

def _write(stf, cmd):
    stf.stdin.write(cmd)
    stf.stdin.write('\n')

def _go(stf):
    _write(stf, 'go')

def _brd(stf):
    _write(stf, 'd')

def _pos(stf, fen=None, moves=None):
    wstr = 'position'
    if fen is None:
        fen = 'startpos'
    else:
        fen = 'fen {}'.format(fen)
    if moves is not None:
        moves = 'moves {}'.format(moves)
    _write(stf, 'position {} {}'.format(fen, moves).strip())


def get_board(fen=None, moves=None):
    stf = _get_stockfish()
    _pos(stf, fen=fen, moves=moves)
    _brd(stf)

    brd = []
    for line in iter(stf.stdout.readline, b''):
        line = line.strip()
        if line and line[0] in ('|', '+'):
            brd.append(line)
        print(">>> " + line)
        if 'Checkers' in line:
            return brd

def get_bestmove(fen=None, moves=None):
    stf = _get_stockfish()
    _pos(stf, fen=fen, moves=moves)
    _go(stf)

    for line in iter(stf.stdout.readline, b''):
        line = line.rstrip()
        print(">>> " + line)
        if 'bestmove' in line:
            return line.split()[1]

def get_fen(fen=None, moves=None):
    stf = _get_stockfish()
    _pos(stf, fen=fen, moves=moves)
    _brd(stf)
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
    app.run(host='0.0.0.0', port=6464)
