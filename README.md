# Results of checking
## 3 variants checked:
- save words in txt files
- tinydb (lightweight document oriented database, NOSQL, json)
- sqlite (lightweight disk-based transaction relational database engine)


## Space (disk usage)
No special requirements (application is for usual computer), so we don't care about the space.
Some measurements anyway.

Sizes in bytes:

|                    |657 words| 1546 words | 4 000 words | 10 000 words | 20 000 words |
|--------------------|-----|------|-------|--------------|--------------|
| txt files:         |9 698|17 602| 38 385| 92 403       | 186 195      |
| tinydb json files: |18 648|44 887| 114 168| 290 057      | 583 849      |
| sqlite db:         |45 056|73 728| 151 552| 344 064      | 700 416      |



## Time (time of execution)
Operations with plain text are fastest, but waiting time is not critical<br/>(hardware data is not provided, the ratio is checked).

Time measurement of the functions
(approximate times in seconds)

|                                                                                                                                     | txt    | tinydb | sqlite |
|-------------------------------------------------------------------------------------------------------------------------------------|--------|----|--------|
| add_to_base (add 1 word<br/>to the base with 1000 words)                                                                            | 0.0006 | 0.009 | 0.009  |
| word_in_base (check 1 word<br/>in the base with 1000 words)                                                                         | 0.0002 | 0.002 | 0.0001 |
| print_base (get all: 657 words)                                                                                                     | 0.001  | 0.001 | 0.001  |
| print_base (get all: 20 000 words)                                                                                                  | 0.1    | 0.1 | 0.1    |
| print_base (get: 'v*')<br/>811 words started with v<br/>from base with 20 000 words                                                 | 0.003  | 0.003 | 0.003  |
| add_words - add 10 000 words<br/>to the base with 10 000 words<br/>(two functions for each addition:<br/>word_in_base, add_to_base) | 3      | 119 | 83     |
| rem_words (remove 10 000 words<br/>from base with 20 000 words)                                                                     | 6      | 47 | 45     |


## Conclusion
For now, it seems ok to proceed with plain text as data storage format for the current simple CLI application. Later txt can be updated to csv, to change from line with one word (now: 'word') to line with forms (could be: 'word,words,worded,wording').


## Reasons migrate to sql:
- Web application (for many users)
- Relational data ('word' can be related: 'noun' or 'verb', 'Tokyo' can be related: 'name' or 'city')


