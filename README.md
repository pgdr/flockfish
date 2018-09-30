# flockfish

A [Flask](https://github.com/pallets/flask) server that boots up
[Stockfish](https://github.com/official-stockfish/Stockfish) and returns best
moves.


Starting the server, `python flock.py` and then visiting
`http://127.0.0.1:6464/next/?fen=rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R%20b%20KQkq%20-%201%202`
yields
a json string containing only `b8c6`.

The `board` endpoint returns the board:

`http://127.0.0.1:6464/board/?fen=rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R%20b%20KQkq%20-%201%202`
yields a json list
```json
["+---+---+---+---+---+---+---+---+",
 "| r | n | b | q | k | b | n | r |",
 "+---+---+---+---+---+---+---+---+",
 "| p | p |   | p | p | p | p | p |",
 "+---+---+---+---+---+---+---+---+",
 "|   |   |   |   |   |   |   |   |",
 "+---+---+---+---+---+---+---+---+",
 "|   |   | p |   |   |   |   |   |",
 "+---+---+---+---+---+---+---+---+",
 "|   |   |   |   | P |   |   |   |",
 "+---+---+---+---+---+---+---+---+",
 "|   |   |   |   |   | N |   |   |",
 "+---+---+---+---+---+---+---+---+",
 "| P | P | P | P |   | P | P | P |",
 "+---+---+---+---+---+---+---+---+",
 "| R | N | B | Q | K | B |   | R |",
 "+---+---+---+---+---+---+---+---+"]
```
