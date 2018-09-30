# flockfish

A [Flask](https://github.com/pallets/flask) server that boots up
[Stockfish](https://github.com/official-stockfish/Stockfish) and returns best
moves.

For this project, you need to download and install `stockfish` and either have
it in `$PATH` or give the path to `stockfish` as an argument.

Four endpoints:
* `/`  (which returns all of the below)
* `/bestmove`
* `/fen`
* `/board`

They all take arguments `?fen=<fenstring>&moves=<space separated fullmoves>`

examples:
* `bestmove?moves=e2e4 c7c5 c2c3 d7d5 e4d5 d8d5` -> `d2d4` (according to Deep Blue)
* `fen?moves=e2e4 c7c5 c2c3 d7d5 e4d5 d8d5` -> `"rnb1kbnr/pp2pppp/8/2pq4/8/2P5/PP1P1PPP/RNBQKBNR w KQkq - 0 4"`
* `board?fen=rnb1kbnr/pp2pppp/8/2pq4/8/2P5/PP1P1PPP/RNBQKBNR w KQkq - 0 4` ->
```
["+---+---+---+---+---+---+---+---+",
 "| r | n | b |   | k | b | n | r |",
 "+---+---+---+---+---+---+---+---+",
 "| p | p |   |   | p | p | p | p |",
 "+---+---+---+---+---+---+---+---+",
 "|   |   |   |   |   |   |   |   |",
 "+---+---+---+---+---+---+---+---+",
 "|   |   | p | q |   |   |   |   |",
 "+---+---+---+---+---+---+---+---+",
 "|   |   |   |   |   |   |   |   |",
 "+---+---+---+---+---+---+---+---+",
 "|   |   | P |   |   |   |   |   |",
 "+---+---+---+---+---+---+---+---+",
 "| P | P |   | P |   | P | P | P |",
 "+---+---+---+---+---+---+---+---+",
 "| R | N | B | Q | K | B | N | R |",
 "+---+---+---+---+---+---+---+---+"]
```

Starting the server, `python flock.py` and then visiting
`http://127.0.0.1:6464/bestmove/?fen=rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R%20b%20KQkq%20-%201%202`
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


The `fen` endpoint
`http://127.0.0.1:6464/fen/?moves=e2e4%20c7c5%20c2c3%20d7d5%20e4d5%20d8d5`
yields
```json
"rnb1kbnr/pp2pppp/8/2pq4/8/2P5/PP1P1PPP/RNBQKBNR w KQkq - 0 4"
 ```
