Simple CLI program to count words in text, and print list of counted words.  
And then user can edit received list of words:
- mark word with label
- hide labeled words


### Purpose of the application.
Might be useful for people learning a new language.
Examples of using:
- Find unknown words in text and learn these words before reading the whole text.
- To have base with known words (personal vocabulary) and append new words to this base during learning process.  


### Overview of the program workflow

- input text from the console
```commandline
$ python count_words.py
```
- load text from a file
```commandline
$ python count_words.py -f text/01_a_touch_of_moss.txt 
```

The app prints a list of words with labels in descending order.  
For now, there are 4 predefined labels (sets of words):
- top100 - 100 most common words in English
- top1000 - most common words from 100 to 1000
- l1 - list number one - user know these words very well.
- l2 - list number two - user know these words (but it's not for sure).  
l1 and l2 are databases (number of txt files), user can edit the base (add/remove words).

#### Example of the launch,
Scenario: get unknown and not very familiar words from text  
(get words from txt file and hide words from top100, top1000 and l1)
```commandline
$ python count_words.py -f text/01_a_touch_of_moss.txt -t100 -t1000 -l1
```

### Edit mode  
To edit l1 and l2 bases:
```commandline
$ python count_words.py -e
```
User can print the list of words from the base. Add new words or remove words.
