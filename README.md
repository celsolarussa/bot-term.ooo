# Termooo Bot
## Introduction
This app finds the secret word of the day from term.ooo in Portuguese version.

The bot uses the words contained in the `words.txt` file. The first word is sent randomly and the site returns the result of each letter of the chosen word, then we apply a filter on the word list based on the result of the letters and the words that do not fit this filter are removed from the word list, the new word is entered and the cycle repeats until the odds run out or you win.

The game history is inside the `result` folder.

Game modes:
- One word: https://term.ooo
- Two words: https://term.ooo/2/
- Four words: https://term.ooo/4/

To change the game mode it is necessary to change the variable that stores the url of the page at `__main__.py line 81`.


## Dependencies
`python >= 3.8`
## Install
```
pip install -r requirements.txt
```
## Run
```
python -m term
```
## Tests
```
pytest
```
