import tomlkit as toml
import os
import gettext

MODULE_DIR = os.path.abspath(__file__).replace('satori.py', '')

def dbgprint(s):
  s = '\n' + str(s)
  for c in s:
    if (c != '\n'):
      print(c, sep = '', end = '')
    else:
      print(c + 'DEBUG: ', end = '')

def satori(chr1, chr2):
  ## read and parse toml files
  with open('characters.toml', 'r') as fi:
    content = fi.read()
  dbgprint(content)
  global cfg
  cfg = toml.parse(content)
  dbgprint(cfg)
  ## get the indexes of characters
  ind1 = -1
  ind2 = -1
  ind = 0
  for i in cfg['character']:
  # dbgprint(i)
    if i['name'] == chr1:
      ind1 = ind
    elif i['name'] == chr2:
      ind2 = ind
    ind += 1
  ## get the display names
  global ch1  ## for quick reference
  ch1 = cfg['character'][ind1]
  global ch2
  ch2 = cfg['character'][ind2]
  dchr1 = ch1['display_name']
  # dbgprint(dchr1)
  dchr2 = ch2['display_name']
  # dbgprint(dchr2)

satori('reimu', 'marisa')