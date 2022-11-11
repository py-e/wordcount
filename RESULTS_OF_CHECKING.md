## 3 variants checked:
- save words in txt files
- tinydb (lightweight document oriented database, NOSQL, json)
- sqlite (lightweight disk-based transaction relational database engine)


## Space (disk usage)
| |657 words|1546 words|
|---|---|---|
| txt files:|9 698 bytes|17 602 bytes|
| tinydb json:|18 648 bytes|44 887 bytes|
| sqlite db:|45 056 bytes|73 728 bytes|
No special requirements (application is for usual computer), so we don't care about the space.


## Time (time of execution)
Operations with plain text are fastest, but waiting time is not critical
(example, removing of 644 words: 0.3 sec for txt, 2.1 for tinydb, 2.7 for sqlite).

Time measurement of the functions
(approximate times in seconds)

| |txt|tinydb|sqlite|
|---|---|---|---|
|add_to_base (add 1 word)|0.00001|0.01|0.001|
|word_in_base (check 1 word)|0.00001|0.001|0.0001|
|print_base (get all 657 words)|0.001|0.001|0.001|
|rem_words (remove 10 words)|0.001|0.01|0.01|


## Conclusion
For now, it seems ok to proceed with plain text as data storage format for the current simple CLI application. Later txt can be updated to csv, to change from line with one word (now: 'word') to line with forms (could be: 'word,words,worded,wording').

## Reasons migrate to sql:
- Web application (for many users)
- Relational data ('word' can be related: 'noun' or 'verb', 'Tokyo' can be related: 'name' or 'city')


