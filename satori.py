import tomlkit as toml
import os
import random
# import gettext

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
  global ch1, ch2  ## for quick reference
  ch1 = cfg['character'][ind1]
  ch2 = cfg['character'][ind2]
  global dchr1, dchr2
  dchr1 = ch1['display_name']
  # dbgprint(dchr1)
  dchr2 = ch2['display_name']
  # dbgprint(dchr2)
  ## contest start
  print('{} VS {}'.format(dchr1, dchr2))
  ## print initial information
  hp1, atk1, hp2, atk2 = ch1['hp'], ch1['atk'], ch2['hp'], ch2['atk']
  round_start(hp1, hp2, atk1, atk2, True)
  while True:
    if check_end():
      break
    ## get current round's atk
    print('===')
    cur_atk1 = random.randint(0, atk1)
    cur_atk2 = random.randint(0, atk2)
    round_start(ch1['hp'], ch2['hp'], cur_atk1, cur_atk2)
    if cur_atk1 > cur_atk2:
      use_spellcard(ch1, ch2)
    else:
      use_spellcard(ch2, ch1)
  #  break
  
def round_start(h1, h2, a1, a2, init = False):
  if init:
    print('初始数据：')
  print('{}:\n血量：{}\n ATK: {}'.format(dchr1, h1, a1))
  print('{}:\n血量：{}\n ATK: {}'.format(dchr2, h2, a2))


def use_spellcard(ch, enemy):
  card_id = random.randint(0, len(ch['spellcard']) - 1)
  card = ch['spellcard'][card_id]
  ch_name = ch['display_name']
  card_name = card['display_name']
  print('{}使用{}'.format(ch_name, card_name), end = '')
  harm = random.randint(card['harm'][0], card['harm'][1])
  print('造成{}点伤害'.format(harm))
  enemy['hp'] -= harm
  

def check_end():
  return (ch1['hp'] < 0 or ch2['hp'] < 0)


satori('reimu', 'marisa')