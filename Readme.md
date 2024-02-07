# Readme

---

## What is the project?

Its a terminal application with which a user can retrieve information (table, fixture, last-5-games-table, etc.) about the Bundesliga as well as 2. Bundesliga. The user can run the program with flags (e.g. `--table` → gets the current table of the Bundesliga pretty printed to the terminal, `--fixture 21` → gets the fixture of the given gameday, when no gameday is input, it gets the current. 

## What is the MVP (Minimal Viable Product)?

- There are 2 modes
    - `get bundesliga --table` retrieves the asked data and displays it, after that the program exits
    - `get bundesliga --table -s or get -s --start-session` will start a session so the program waits for new tasks and does not exit till user says so `exit`
- if a user starts a session using `get bundesliga -s` the user should no longer need to add `bundesliga` in his requests (its now the default).
    - the user can either specifiy for one request `bundesliga2 --table` to get the table for the 2. Bundesliga, but the session still remembers `bundesliga` as its main section
    - the user can swtich the main section within a session using `switch bundesliga2 (--table) optional`  to switch session and ask at the same time or just switch session
- `bundesliga --table gameday (optional)` to get the specified table of the Bundesliga / 2. Bundesliga pretty printed to the terminal. The table should also contain the results of the last 5 games
    
    ![table](https://github.com/AaronBittel/Football-League-Scraper-CLI-/assets/148724144/0e82326f-0075-44b6-b203-87fe9c33c990)
    
    ![table_extra](https://github.com/AaronBittel/Football-League-Scraper-CLI-/assets/148724144/49eb0592-d128-46e3-a399-2ca1f3e574f0)
    
- `bundesliga --fixture gameday (optional)` to get the specified fixture of the Bundesliga / 2. Bundesliga pretty printed to the terminal
    
    ![fixture](https://github.com/AaronBittel/Football-League-Scraper-CLI-/assets/148724144/73a20f79-6386-408e-8c9b-5bc02614a48e)

## What are the sprinkles?

- `--table-last-5` get the table of the last 5 (specified) games
- `--top-goal-scorer` gets the best goal scorer
- `--top-assister` gets the best assister
- `--top-scorer` gets the best goal scorer + assister
- Ability to ask for multiple data at the same time `get bundesliga --table --fixture` → async needed if one should come at a time (maybe with input to get the next)
- use aiohttp to retrieve data asynchroniously
- use caching that every page / data from page is fetched once in a session
- different leagues

## When will the project be complete?

Once the features of the MVP is implemented.
