import random
import SaveData

intro = 0

Battle_active = False

Current_Scene = 'Forest'

Menu_Option = ['Discard', 'discard', 'Equip']

class EnemyLevel(object):
    levelrange = {
        'Skeleton': [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 5],
        'Gelly': [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 5]
    }
    def __init__(self, LevelRange_Name):
        self.LevelRange_Name = LevelRange_Name
    def enemyLevelRange(self):
        self.LevelRangeReturn = self.levelrange[self.LevelRange_Name]
        return self.LevelRangeReturn
    def enemyLevel(self, Level):
        self.enemyLevel = Level.pop(random.randint(0, 15))
        return self.enemyLevel

class EnemyStats(object):
    def __init__(self, Enemy_Level, Enemy_Stats):
        self.Enemy_Level = Enemy_Level
        self.Enemy_Stats = Enemy_Stats
    def EnemyStatsReturn(self, EnemyStat):
        EnemyStat['HP'] = ((self.Enemy_Stats['HP'] * self.Enemy_Level)/10) + self.Enemy_Stats['HP']
        EnemyStat['Atk'] = ((self.Enemy_Stats['Atk'] * self.Enemy_Level)/10) + self.Enemy_Stats['Atk']
        EnemyStat['Def'] = ((self.Enemy_Stats['Def'] * self.Enemy_Level)/10) + self.Enemy_Stats['Def']
        EnemyStat['SpA'] = ((self.Enemy_Stats['SpA'] * self.Enemy_Level)/10) + self.Enemy_Stats['SpA']
        EnemyStat['SpD'] = ((self.Enemy_Stats['SpD'] * self.Enemy_Level)/10) + self.Enemy_Stats['SpD'] 
        EnemyStat['Exp'] = (self.Enemy_Stats['Exp'] * self.Enemy_Level)/7

Class_Warrior_Disc = """The Warrior is a class focused on melee attackes.
Sporting the highest physical attack stat of any of the classes. 
This option is for those of you who want nothing but physical might on your side and the ablity to crush all who dare to stand in your way!"""

Class_Mage_Disc = """The Mage is a class focused on Arcane art.
Sporting the highest special attack stat of any of the classes.
This option is for those of you who want nothing more then to set fire to your enemys or anything else that might stand in your way!"""

Class_Tactician_Disc ="""The Tactician is a jack of all traits but a master of non
Sporting a balance between physical and special attack.
This option is for those who want both the power of magic and the might of a sword!"""

Battle_active = False

class NPC(object):
    pass

class Character(object):
    magic_print	= ['Fire MP:5', 'Explosion MP:20']
    magic_own = {
        'fire': 1, 
        'explosion': 1
    }
    equipment = {
        'Weapon': 'na',
        'Armor': 'na'
        }
    stats = {
        'HP': 30,
        'HP_Max': 30,
        'Mag': 10,
        'Mag_Max': 10,
        'Atk': 5,
        'SpA': 5,
        'Def': 1,
        'SpD': 1,
        'Lvl': 5,
        'Exp': 0,
        'Gold': 0,
        'Sex': 0,
        'Nam': 0,
        'Cla': 0
    }
    equ_item = ['Iron Sword']
    use_item = [0]

class Skeleton(NPC):
    def __init__(self):
        self.enemy_name = 'Skeleton'
        self.Level = EnemyLevel(self.enemy_name)
        self.list_of_levels = self.Level.enemyLevelRange()
        self.enemy_level = self.Level.enemyLevel(self.list_of_levels)
        self.enemy_death = 'The Skeleton colapsed into a pile of bones'
        self.equipment = {
            'Weapon': 'na',
            'Armor': 'na'
        }
        self.stats = {
                'HP': 20,
                'Atk': 3,
                'Def': 2,
                'SpD': 2,
                'SpA': 1,
                'Exp': 140,
                'Gold': 1,
                'Lvl': 1
        }
        self.EnemyStats = EnemyStats(self.enemy_level, self.stats)
        self.EnemyStats.EnemyStatsReturn(self.stats)

class Gelly(NPC):
    def __init__(self):
        self.enemy_name = 'Gelly'
        self.Level = EnemyLevel(self.enemy_name)
        self.list_of_levels = self.Level.enemyLevelRange()
        self.enemy_level = self.Level.enemyLevel(self.list_of_levels)
        self.enemy_death = 'The Gelly colaps into a pool of slime!'
        self.equipment = {
            'Weapon': 'na',
            'Armor': 'na'
        }
        self.stats = {
                'HP': 50,
                'Atk': 1,
                'Def': 1, 
                'SpD': 1,
                'SpA': 1,
                'Exp': 100,
                'Gold': 1,
                'Lvl': 1
        }
        self.EnemyStats = EnemyStats(self.enemy_level, self.stats)
        self.EnemyStats.EnemyStatsReturn(self.stats)

class enemyinconter(object):
    enemys = {
        'Gelly': Gelly(),
        'Skeleton': Skeleton()
    }
    Scenes = {
        'Forest': ['Skeleton', 'Skeleton', 'Gelly', 'Gelly', 'Gelly']
    }
    def __init__(self, current):
        self.EnemyInArea = self.Scenes[current]
        self.EnemyFromArea = self.EnemyInArea.pop(random.randint(0, 4))
        self.EnemyInArea.append(self.EnemyFromArea)
    def Inconter(self):
        return enemyinconter.enemys.get(self.EnemyFromArea)

class Magic(object):
    ## Magic is listed as such : 
    ## 'Name of Spell': [MP Cost, Damage]
    Magic = {
        'fire': [5, 5],
        'explosion': [20, 30]
    }
    def __init__(self, magic):
        self.magic_spell = magic
        self.magic_Owned = Character.magic_own[self.magic_spell]
    def reture_magic(self):
        if self.magic_Owned == 1:
            return self.Magic[self.magic_spell]
        else:
            return 'Nothing'

class Damage_calc(object):
    def __init__(self, Atk, Def, Equip_D, Equip_A):
        self.Atk = Atk
        self.Def = Def
        self.Equip_D = Equip_D
        self.Equip_A = Equip_A
    def Damage(self):
        self.Atk_M = self.Equip_A + self.Atk
        self.Def_M = self.Equip_D + self.Def
        damage = (((float(self.Atk_M)/float(self.Def_M)) * random.randint(8,10)) / float(2))
        return damage
    def MagicDamage(self, magic_power):
        self.Atk_M = self.Equip_A + self.Atk
        self.Def_M = self.Equip_D + self.Def
        self.Magic_Damage = magic_power
        damage_modife = (self.Magic_Damage * (float(self.Atk_M)/float(self.Def_M)))
        return damage_modife

class LevelUp(object):
    def __init__(self, Level, Exp):
        self.Level = Level
        self.Exp = Exp
        self.Exp_Need = (self.Level**3)
    def Level_Up_Happening(self):
        if self.Exp_Need <= self.Exp:
            return 'yes'
        else:
            return 'no'
    def Level_Up(self):
        if self.Exp_Need <= self.Exp:
            Character.stats['Exp'] - self.Exp
            Character.stats['Lvl'] += 1
            print "\nYou have now reached level %d!" % Character.stats['Lvl']
            if Character.stats['Cla'] == "Warrior":
                Attack = random.randint(2, 5)
                print "Your Attack has gone up by %d!" % Attack
                Character.stats['Atk'] += Attack
                Special_Atk = random.randint(0, 1)
                print "Your Special Attack has gone up by %d!" % Special_Atk
                Character.stats['SpA'] += Special_Atk
                Defense = random.randint(2, 5)
                print "Your Defense has gone up by %d!" % Defense
                Character.stats['Def'] += Defense
                Special_Def = random.randint(1, 2)
                print "Your Special Defense has gone up by %d!" % Special_Def
                Character.stats['SpD'] += Special_Def
            elif Character.stats['Cla'] == "Mage":
                Attack = random.randint(0, 1)
                print "Your Attack has gone up by %d!" % Attack
                Character.stats['Atk'] += Attack
                Special_Atk = random.randint(2, 5)
                print "Your Special Attack has gone up by %d!" % Special_Atk
                Character.stats['SpA'] += Special_Atk
                Defense = random.randint(1, 2)
                print "Your Defense has gone up by %d!" % Defense
                Character.stats['Def'] += Defense
                Special_Def = random.randint(2, 5)
                print "Your Special Defense has gone up by %d!" % Special_Def
                Character.stats['SpD'] += Special_Def
            elif Character.stats['Cla'] == "Tactician":
                Attack = random.randint(1, 3)
                print "Your Attack has gone up by %d!" % Attack
                Character.stats['Atk'] += Attack
                Special_Atk = random.randint(1, 3)
                print "Your Special Attack has gone up by %d!" % Special_Atk
                Character.stats['SpA'] += Special_Atk
                Defense = random.randint(1, 3)
                print "Your Defense has gone up by %d!" % Defense
                Character.stats['Def'] += Defense
                Special_Def = random.randint(1, 3)
                print "Your Special Defense has gone up by %d!" % Special_Def
                Character.stats['SpD'] += Special_Def


class Equipment(object):
    ##Equipment stats are listed like 
    ##"name": [primaery stat, secondary stat, third stat]
    ##A weapons primary stat will always be its physical attack
    ##secondary stat will always be its special attack
    ##third will be any status ailment
    ##For Armor will be listed at physical def, special def, and any buff
    Equipment = {
        'na': [0, 0, 0],
        'Iron Sword': [10, 0, 0],
        'Stone Sword': [5, 0, 0],
        'Staff': [0, 10, 0],
        'Broken Staff': [0, 5, 0],
        'Iron Chest Plate': [10, 0, 0],
        'Chest Plate': [5, 0, 0],
        'Robs': [0, 10, 0],
        'Tattered Robs': [0, 5, 0]
        }
    def __init__(self, Item_Name, b):
        self.Equipment_ = self.Equipment[Item_Name]
        self.Equipment_Type = b
    def return_equipment(self):
        return self.Equipment_[self.Equipment_Type]

class Items(object):
    def check_action(self, check, input):
        try:
            check.index(input)
            return True
        except ValueError:
            return False

def SaveGame():
    fuck = Character()
    f = open('SaveData.py', 'w')
    f.write('''GameSaved = True
LastScene = '%s'
class Character(object):
    stats = {
        'HP': %d,
        'HP_Max': %d,
        'Mag': %d,
        'Mag_Max': %d,
        'Atk': %d,
        'SpA': %d,
        'Def': %d,
        'SpD': %d,
        'Lvl': %d,
        'Exp': %d,
        'Gold': %d,
        'Sex': '%s',
        'Nam': '%s',
        'Cla': '%s'
    }''' % (Current_Scene,
            fuck.stats['HP'], fuck.stats['HP_Max'], fuck.stats['Mag'], 
            fuck.stats['Mag_Max'], fuck.stats['Atk'], 
            fuck.stats['SpA'], fuck.stats['Def'], fuck.stats['SpD'],
            fuck.stats['Lvl'], fuck.stats['Exp'], fuck.stats['Gold'],
            fuck.stats['Sex'], fuck.stats['Nam'], fuck.stats['Cla']))