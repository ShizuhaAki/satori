# satori

satori is a tool that generates a Gensokyo-style spellcard fight purely randomly.

## Usage

Clone this repository, and run `main.py`.

```bash
# Install dependencies
pip3 install tomlkit
# Clone and run
git clone https://github.com/Ravenclaw-OIer/satori
python3 satori/main.py reimu marisa # change reimu and marisa to whoever you want
```


## Rules
satori reads spellcard data from ~~your mind~~ `characters.toml` file.


### Rounds

A spellcard fight is consisted of several rounds, it will continue until one of the players has her hp strictly lower than 0.

In each round, the following events happen in chronological order:

+ A random number is generated between 0 and the `atk` value of both players. This value is the `atk` value used for comparison in this round.
+ The one with the higher `atk` value for this round will be the attacker. A spellcard is randomly picked from her spellcards.
+ A number is randomly picked between the two values specified in the spellcard's `harm` field. This is the harm (hp drop) caused by this spellcard. This value may be 0.
+ The hp drop is applied.
+ If the spellcard comes with shields, hp boosts or atk boosts, it is applied.
+ The round ends, if both player have their `hp>=0`, return to step 1.

### Spellcards

Each spellcard has the following fields:

+ 


## Contributing

You can contribute by

- Writing more spellcards
- Implementing complex spellcard behaviors
- Simply playing around and report bugs

## License

This program is free software, you can redistribute it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3, or, at your option, any later version.

