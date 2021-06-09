import os
import random
import tomlkit as toml


MODULE_DIR = os.path.abspath(__file__).replace('satori.py', '')


class Spellcard:
  def __init__(self, dat):
    self.name = dat['name']
    self.display_name = dat['display_name']
    self.min_harm = dat['harm'][0]
    self.max_harm = dat['harm'][1]
    self.atk_boost_value = dat['atk'][0]
    self.atk_boost_dura = dat['atk'][1]
    self.shield = dat['shield']
    self.hp_boost = dat['hp']


  def do_harm(self):
    '''Returns the harm done by the card'''
    return random.randint(self.min_harm, self.max_harm)



class Girl:
  def __init__(self, name, dispname, hp, atk, spellcards):
    dbgprint('init: {} {} {} {}'.format(name, dispname, hp, atk))
    self.cur_hp = hp
    self.name = name
    self.display_name = dispname
    self.atk = atk
    self.spellcard = []
    for config_file in spellcards:
      self.spellcard.append(Spellcard(config_file))
    self.shield = 0
    self.atk_boost = []
    self.tag = False


  def is_dead(self):
    '''Returns whether the girl has died'''
    return self.cur_hp < 0



  def use_spellcard(self, enemy):
    '''Uses a spellcard'''
    ## choose a spellcard
    spc = random.choice(self.spellcard)
    cur_harm = spc.do_harm()
    print('{}使用{}'.format(self.display_name, spc.display_name))
    if not enemy.drop_hp(cur_harm):
      print("无法造成伤害")
    else:
      print("造成{}点伤害".format(cur_harm))
    if spc.atk_boost_value != 0:
      self.add_atk_boost(spc.atk_boost_value, spc.atk_boost_dura)
      print('获得{}点攻击加成，持续{}回合'.format(spc.atk_boost_value, spc.atk_boost_dura))
    if spc.shield != 0:
      dbgprint('adding shield to {}, duration is {}'.format(self.name, spc.shield))
      self.shield += spc.shield
      self.tag = True
      print('{}在以后{}轮内不会受到伤害'.format(self.display_name, self.shield if self.shield == 1 else self.shield - 1))
    if spc.hp_boost != 0:
      self.cur_hp += spc.hp_boost
      print('血量恢复了{}点'.format(spc.hp_boost))


  def drop_hp(self, val):
    '''Wrapper for hp drop that deals with shields'''
    if self.shield == 0:
      self.cur_hp -= val
      return True
    return False
   
  
  def get_hp(self):
    '''Returns the current hp of a girl'''
    return self.cur_hp

  
  def get_atk(self):
    '''Returns the MAXIMUM atk of a girl'''
    return self.atk


  def get_round_atk(self):
    '''Returns a randomly generated atk for single round'''
    return random.randint(0, self.atk)


   
  def add_atk_boost(self, natk, atime):
    '''Appends an atk boost'''
    dbgprint('adding atkboost to {}: {}, {}'.format(self.name, natk, atime))
    self.atk_boost.append((natk, atime))
    self.atk += natk


  def after_round(self):
    '''After round cleanup'''
    for boost in self.atk_boost:
      remain = boost[1]
      val = boost[0]
      self.atk -= val
      self.atk_boost.remove(boost)
      if remain != 0:
        self.add_atk_boost(val, remain - 1)
    if (self.shield > 1) or (self.shield == 1 and not self.tag):
      self.shield -= 1
    self.tag = False
    dbgprint('boost of {}: {}'.format(self.name, self.atk_boost))
    dbgprint('shield of {}: {}'.format(self.name, self.shield))
    dbgprint('atk of {} is now {}'.format(self.name, self.atk))

  

## Remove the following comments to disable debug print
#'''
def dbgprint(s):
  '''Debug print'''
  with open('debug_satori.log', 'a') as fo:
    fo.write('DEBUG: {}\n'.format(s))
#'''

def find_chr(config_file, chr1, chr2):
  '''Finds a character from the TOML config file'''
  for i in config_file['character']:
  # dbgprint(i)
    if i['name'] == chr1:
      j = i
    elif i['name'] == chr2:
      k = i
  return j, k


def satori(chr1, chr2):
  '''Main function'''
  dbgprint('Running satori: {}, {}'.format(chr1, chr2))
  ## read and parse toml files
  with open('characters.toml', 'r') as file_input:
    content = file_input.read()
  config_file = toml.parse(content)
  ## get the indexes of characters
  j, k = find_chr(config_file, chr1, chr2)
  g1 = Girl(chr1, j['display_name'], j['hp'], j['atk'], j['spellcard'])
  g2 = Girl(chr2, k['display_name'], k['hp'], k['atk'], k['spellcard'])
  ## print initial information
  while True:
 #   dbgprint('round start!')
    if g1.is_dead() or g2.is_dead():
      break
    ## get current round's atk
    print('===')
    round_start(g1, g2)
    atk1 = g1.get_round_atk()
    atk2 = g2.get_round_atk()
    print('本回合：{}的ATK是{};{}的ATK是{}'.format(g1.display_name, atk1, g2.display_name, atk2))
    if atk1 > atk2:
      g1.use_spellcard(g2)
    else:
      g2.use_spellcard(g1)
    g1.after_round()
    g2.after_round()


def round_start(g1, g2):
  
  dbgprint("New round")
  print("{}:\n血量:{}\nATK:{}\n{}:\n血量:{}\nATK:{}".format(g1.display_name, g1.cur_hp, g1.atk, g2.display_name, g2.cur_hp, g2.atk))


satori('reimu', 'marisa')