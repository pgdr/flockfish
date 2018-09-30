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

def board(fen):
    p = _get_stockfish()
    p.stdin.write("""\
    position \
    fen \
    {}
    """.format(fen))

    p.stdin.write('d\n')
    brd = []
    for line in iter(p.stdout.readline, b''):
        line = line.strip()
        if line and line[0] in ('|', '+'):
            brd.append(line)
        print(">>> " + line)
        if 'Checkers' in line:
            return brd


def bestmove(fen):
    p = _get_stockfish()
    p.stdin.write("""\
    position \
    fen \
    {}
    """.format(fen))

    p.stdin.write('go\n')

    for line in iter(p.stdout.readline, b''):
        line = line.rstrip()
        print(">>> " + line)
        if 'bestmove' in line:
            return line.split()[1]


app = Flask('Flockfish')

@app.route('/next/', methods=['GET'])
def route_next():
    fen = request.args.get('fen')
    return jsonify(bestmove(fen))

@app.route('/board/', methods=['GET'])
def route_board():
    fen = request.args.get('fen')
    return jsonify(board(fen))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6464)
