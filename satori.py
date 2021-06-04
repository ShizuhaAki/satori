import tomlkit as toml
import os
import random
# import gettext

MODULE_DIR = os.path.abspath(__file__).replace('satori.py', '')

class Girl:
  def __init__():
    pass

  def __init__(name, dispname, hp, atk, spellcards):
    self.cur_hp = hp
    self.name = name
    self.display_name = dispname
    self.hp = hp
    self.atk = atk
    self.spellcard = spellcards


  def is_dead():
    return self.hp < 0


  def use_spellcard():
    pass

  def init_round():
    pass

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
  g1, g2 = Girl(), Girl()
  ## print initial information
  while True:
    if check_end():
      break
    ## get current round's atk
    print('===')
    g1.init_round()
    g2.init_round()
    round_start(ch1['hp'], ch2['hp'], cur_atk1, cur_atk2)
    if g1.cur_atk > g2.cur_atk:
      g1.use_spellcard(g2)
    else:
      g2.use_spellcard(g1)
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