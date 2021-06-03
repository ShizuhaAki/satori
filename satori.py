import tomlkit as toml
import os

MODULE_DIR = os.path.abspath(__file__).replace('satori.py', '')


def satori(chr1, chr2):
  with open('characters.toml', 'r') as fi:
    content = fi.read()
  print(content)
  global cfg
  cfg = toml.parse(content)
  print(cfg)

satori('reimu', 'marisa')