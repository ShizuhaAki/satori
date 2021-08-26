'''
    satori, random spellcard fight generator
    Copyright (C) 2021 Shu Shang

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import time
import random
import tomlkit as toml
from docopt import docopt


OPTIONS = '''Usage:
satori [options] <girl1> <girl2>

-s, --style (normal | anke)  Specifies the output style [default: normal]
-v, --verbose                      Enter verbose mode
--version                          Print version information
-h, --help                         Print this short help and exit
'''


class Spellcard:
  '''Class for spellcards'''
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
  '''A girl in Gensokyo'''
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
    self.tag = 0


  def is_dead(self):
    '''Returns whether the girl has died'''
    return self.cur_hp < 0



  def use_spellcard(self, enemy, mode):
    '''Uses a spellcard'''
    ## choose a spellcard
    spc = random.choice(self.spellcard)
    cur_harm = spc.do_harm()
    print('{}使用{}'.format(self.display_name, spc.display_name))
    if not enemy.drop_hp(cur_harm):
      print("无法造成伤害")
    else:
      if mode == 'anke':
        print("造成{}d{}={}点伤害".format(spc.min_harm, spc.max_harm, cur_harm))
      else:
        print("造成{}点伤害".format(cur_harm))
    if spc.atk_boost_value != 0:
      self.add_atk_boost(spc.atk_boost_value, spc.atk_boost_dura)
      print('获得{}点攻击加成，持续{}回合'.format(spc.atk_boost_value, spc.atk_boost_dura))
    if spc.shield != 0:
      dbgprint('adding shield to {}, duration is {}'.format(self.name, spc.shield))
      remain_shield = 0
      if self.shield >= 1:
        remain_shield += self.shield - 1
      remain_shield += spc.shield
      print('{}在以后{}轮内不会受到伤害'.\
        format(self.display_name, remain_shield))
      self.tag = spc.shield
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
    if self.shield != 0:
      self.shield -= 1
    self.shield += self.tag
    self.tag = 0
    dbgprint('boost of {}: {}'.format(self.name, self.atk_boost))
    dbgprint('shield of {}: {}'.format(self.name, self.shield))
    dbgprint('atk of {} is now {}'.format(self.name, self.atk))


## Remove the following comments to disable debug print
#'''
def dbgprint(msg):
  '''Debug print'''
  with open('debug_satori.log', 'a') as file_output:
    file_output.write('DEBUG: {}\n'.format(msg))
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


def satori(chr1, chr2, mode):
  '''Main function'''
  dbgprint('Running satori: {}, {} @ {}'.format(chr1, chr2, int(time.time())))
  ## read and parse toml files
  with open('characters.toml', 'r') as file_input:
    content = file_input.read()
  config_file = toml.parse(content)
  ## get the indexes of characters
  j, k = find_chr(config_file, chr1, chr2)
  girl_1 = Girl(chr1, j['display_name'], j['hp'], j['atk'], j['spellcard'])
  girl_2 = Girl(chr2, k['display_name'], k['hp'], k['atk'], k['spellcard'])
  ## print initial information
  while True:
 #   dbgprint('round start!')
    if girl_1.is_dead() or girl_2.is_dead():
      break
    ## get current round'msg atk
    print('===')
    round_start(girl_1, girl_2)
    atk1 = girl_1.get_round_atk()
    atk2 = girl_2.get_round_atk()
    if mode == 'normal':
      print('本回合：{}的ATK是{};{}的ATK是{}'.\
        format(girl_1.display_name, atk1, girl_2.display_name, atk2))
    else:
      print('本回合：{}的ATK是1d{}={};{}的ATK是1d{}={}'.\
            format(girl_1.display_name, girl_1.get_atk(), \
               atk1, girl_2.display_name, girl_2.get_atk(), atk2))
    if atk1 > atk2:
      girl_1.use_spellcard(girl_2, mode)
    else:
      girl_2.use_spellcard(girl_1, mode)
    girl_1.after_round()
    girl_2.after_round()


def round_start(girl_1, girl_2):
  '''Start a new round'''
  dbgprint("New round")
  print("{}:\n血量:{}\nATK:{}\n{}:\n血量:{}\nATK:{}".\
        format(girl_1.display_name, girl_1.cur_hp, girl_1.atk, \
          girl_2.display_name, girl_2.cur_hp, girl_2.atk))


def main():
  '''Main function'''
  args = docopt(OPTIONS)
  mode = args['--style']
  satori(args['<girl1>'], args['<girl2>'], mode)


main()
