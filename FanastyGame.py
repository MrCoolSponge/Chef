import random
import data
import SaveData
from sys import exit

enterdashenter = '\n---------\n'
askinput = 'What do you do?'
enter = "\n"

class Engine(object):
    def __init__(self, scene_map):
        self.scene_map = scene_map

    def play(self):
        flag = True
        current_scene = self.scene_map.opening_scene()
        if current_scene == "Scene":
            flag = False
        while flag:
            print enterdashenter
            next_scene_name = current_scene.enter()
            if next_scene_name == "Scene":
                exit(0)
            else:
                current_scene = self.scene_map.next_scene(next_scene_name)

class Scene(object):
    pass

class Battle(Scene):
    def enter(self):
        if data.Battle_active == False:
            self.player = data.Character()
            self.the_enemy = data.enemyinconter(data.Current_Scene)
            self.enemy = self.the_enemy.Inconter()
            self.Org_HP = self.enemy.stats['HP']
            data.Battle_active = True
            self.enemy_turn = False
        print 'A %s stands infornt of you!' % self.enemy.enemy_name
        while data.Battle_active:
            if self.enemy.stats['HP'] <= 0:
                self.enemy.stats['HP'] = self.Org_HP
                print self.enemy.enemy_death
                data.level_up(self.enemy.stats['Exp'], self.player.stats['Exp'])
                data.Battle_active = False
                return data.Current_Scene
            if self.player.stats['HP'] <= 0:
                print enterdashenter
                print 'You have taken to much damage'
                print 'Everything fades to black...'
                exit()
            print enter
            print askinput
            print 'Your HP is %d' % self.player.stats['HP']
            if self.enemy.stats['HP'] >= (self.Org_HP/2):
                print "The enemy still stands strong!"
            elif self.enemy.stats['HP'] < (self.Org_HP/2):
                print "The battle seems half finish!"
            action = raw_input()
            if action == 'attack':
                self.equip_a = data.Equipment(self.player.equipment['Weapon'], 0)
                self.equip_d = data.Equipment(self.enemy.equipment['Armor'] , 0)
                self.damage = data.Damage_calc(self.player.stats['Atk'],
                                          self.enemy.stats['Def'], self.equip_a.return_equipment(),
                                          self.equip_d.return_equipment())
                self.FinalDamage = self.damage.Damage()
                self.enemy.stats['HP'] = ((self.enemy.stats['HP']) - self.FinalDamage)
                print enter
                print 'You attack the %s for %d damage' % (self.enemy.enemy_name, self.FinalDamage)
                self.enemy_turn = True
            elif action == 'examine':
                print 'The %s is level %d' % (self.enemy.enemy_name, self.enemy.enemy_level)
                print self.enemy.stats
            elif action == 'magic':
                print 'Chose which spell to use'
                for spells in data.Character.magic_print:
                    print spells
                self.magic_spells_chose = raw_input()
                self.magic = data.Magic(self.magic_spells_chose)
                self.FinalMagic = self.magic.reture_magic()
                if self.FinalMagic == 'Nothing':
                    print "That isn't an option..."
                    continue
                elif self.FinalMagic[0] >= self.player.stats['Mag']:
                    print 'Not enough MP...'
                    continue
                else:
                    print 'You cast %s!' % self.magic_spells_chose
                self.equip_a = data.Equipment(self.player.equipment['Weapon'], 1)
                self.equip_d = data.Equipment(self.enemy.equipment['Armor'] , 1)
                self.player.stats['Mag'] - self.FinalMagic[0]
                self.damage = data.Damage_calc(self.player.stats['SpA'],
                                          self.enemy.stats['SpD'], self.equip_a.return_equipment(),
                                          self.equip_d.return_equipment())
                self.final_magic_damage = self.damage.MagicDamage(self.FinalMagic[1])
                self.enemy.stats['HP'] = ((self.enemy.stats['HP']) - self.final_magic_damage)
                print 'You attack the %s for %d damage' % (self.enemy.enemy_name, self.final_magic_damage)
            else:
                print 'Not an option'
            while self.enemy_turn:
                if self.enemy.stats['HP'] <= 0:
                    self.enemy.stats['HP'] = self.Org_HP
                    print self.enemy.enemy_death
                    print "You got %d Experience from defeating the %s!" % (self.enemy.stats['Exp'],
                                                                              self.enemy.enemy_name)
                    data.Character.stats['Exp'] += self.enemy.stats['Exp']
                    data.Character.stats['Gold'] += self.enemy.stats['Gold']
                    Level = True
                    while Level:
                        self.LevelUp = data.LevelUp(data.Character.stats['Lvl'], data.Character.stats['Exp'])
                        self.LevelUpHappening = self.LevelUp.Level_Up_Happening()
                        if self.LevelUpHappening == 'yes':
                            self.LevelUp.Level_Up()
                        elif self.LevelUpHappening == 'no':
                            Level = False
                    data.Battle_active = False
                    return data.Current_Scene
                if self.player.stats['HP'] <= 0:
                    print enter
                    print 'You have taken to much damage'
                    print 'Everything fades to black...'
                    exit()
                print enter
                print '%s attacks!' % self.enemy.enemy_name
                self.equip_a = data.Equipment(self.enemy.equipment['Weapon'], 0)
                self.equip_d = data.Equipment(self.player.equipment['Armor'] , 0)
                self.damage = data.Damage_calc(self.enemy.stats['Atk'],
                                          self.player.stats['Def'], self.equip_a.return_equipment(),
                                          self.equip_d.return_equipment())
                self.finaldamage = self.damage.Damage()
                self.player.stats['HP'] = ((self.player.stats['HP']) - self.finaldamage)
                print 'The %s did %d damage' % (self.enemy.enemy_name, self.finaldamage)
                self.enemy_turn = False
                continue

class Forest(Scene):
    def enter(self):
        forest_active = True
        forest_travel = 1
        if data.Current_Scene == 'Forest':
            pass
        else:
            print "You walk into the forest"
            pass
        data.Current_Scene = 'Forest'
        while forest_active:
            print askinput
            action = raw_input()
            if action == 'go deeper':
                print "You make your way farther in"
                encounter = random.randint(0, 10)
                if encounter >= 8:
                    return 'Battle'
            elif action == 'save':
                data.SaveGame()
                print "Game Saved"
            elif action == 'heal':
                self.FullHeath = data.Character.stats['HP_Max']
                self.FullMagic = data.Character.stats['Mag_Max']
                data.Character.stats['HP'] = self.FullHeath
                data.Character.stats['MP'] = self.FullMagic
                print "\nYour HP is now at %d" % data.Character.stats['HP']
                print "\nYour MP is now at %d" % data.Character.stats['MP']
            elif action == 'print':
                print data.Character.stats
            else:
                print "Not an option"

class OverWorld(Scene):
    pass

class Intro(Scene):
    def enter(self):
        if data.intro == 0:
            print "Welcome to the world of Emelrock!"
            print "To start I'm going to need some info about yourself."
            print enter
            data.intro = 1
        self.sex_pick = True
        while self.sex_pick:
            print "Are you Male or Female?"
            self.sex = raw_input()
            if (self.sex == 'Male') or (self.sex == 'male'):
                print "So you are a male?"
                self.sexpick = raw_input()
                if (self.sexpick == 'yes') or (self.sexpick == 'Yes'):
                    data.Character.stats['Sex'] = 'male'
                    self.sex_pick = False
                elif (self.sexpick == 'no') or (self.sexpick == 'No'):
                    continue
                else:
                    print "Thats not an option..."
            elif (self.sex == 'Female') or (self.sex == 'female'):
                print "So are you a female?"
                self.sexpick = raw_input()
                if (self.sexpick == 'yes') or (self.sexpick == 'Yes'):
                    data.Character.stats['Sex'] = 'female'
                    self.sex_pick = False
                elif (self.sexpick == 'no') or (self.sexpick == 'No'):
                    continue
                else:
                    print "That's not an option..."
            else:
                print 'Sadly that not an option...'
                print enter
        print "So you are a %s. fair enough" % data.Character.stats['Sex']
        print enter
        self.namepick = True
        while self.namepick:
            print "So what is your name traveler?"
            self.namepick_chose = raw_input()
            data.Character.stats['Nam'] = self.namepick_chose
            print "So your name is %s, huh?" % data.Character.stats['Nam']
            confrim_action = raw_input()
            if (confrim_action == 'No') or (confrim_action == 'no'):
                continue
            elif (confrim_action == 'Yes') or (confrim_action == 'yes'):
                self.namepick = False
            else:
                print "That isn't an option..."
        self.classpick = True
        while self.classpick:
            print "What class do you wish to be %s?" % data.Character.stats['Nam']
            print "Warrior, Mage, or Tactician?"
            print "(Note that typing one of these out will give you a discription of what the class does)"
            self.classpick_action = raw_input()
            if (self.classpick_action == 'Warrior') or (self.classpick_action == 'warrior'):
                print enter
                print data.Class_Warrior_Disc
                print "Do you wish to pick this class?"
                self.classaction = raw_input()
                if (self.classaction == 'no') or (self.classaction == 'No'):
                    continue
                elif (self.classaction == 'yes') or (self.classaction == 'Yes'):
                    data.Character.stats['HP'] = 60
                    data.Character.stats['HP_Max'] = 60
                    data.Character.stats['Mag'] = 10
                    data.Character.stats['Mag_Max'] = 10
                    data.Character.stats['Atk'] = 10
                    data.Character.stats['SpA'] = 1
                    data.Character.stats['Def'] = 2
                    data.Character.stats['SpD'] = 2
                    data.Character.stats['Cla'] = "Warrior"
                    self.classpick = False
                else:
                    print "That's not a option..."
            elif (self.classpick_action == 'Mage') or (self.classpick_action == 'mage'):
                print enter
                print data.Class_Mage_Disc
                print "Do you wish to pick this class?"
                self.classaction = raw_input()
                if (self.classaction == 'no') or (self.classaction == 'No'):
                    continue
                elif (self.classaction == 'yes') or (self.classaction == 'Yes'):
                    data.Character.stats['HP'] = 40
                    data.Character.stats['HP_Max'] = 40
                    data.Character.stats['Mag'] = 50
                    data.Character.stats['Mag_Max'] = 50
                    data.Character.stats['Atk'] = 1
                    data.Character.stats['SpA'] = 10
                    data.Character.stats['Def'] = 1
                    data.Character.stats['SpD'] = 3
                    data.Character.stats['Cla'] = "Mage"
                    self.classpick = False
                else:
                    print "That's not a option..."
            elif (self.classpick_action == 'Tactician') or (self.classpick_action == 'tactician'):
                print enter
                print data.Class_Tactician_Disc
                print "Do you wish to pick this class?"
                self.classaction = raw_input()
                if (self.classaction == 'no') or (self.classaction == 'No'):
                    continue
                elif (self.classaction == 'yes') or (self.classaction == 'Yes'):
                    data.Character.stats['HP'] = 30
                    data.Character.stats['HP_Max'] = 30
                    data.Character.stats['Mag'] = 30
                    data.Character.stats['Mag_Max'] = 30
                    data.Character.stats['Atk'] = 5
                    data.Character.stats['SpA'] = 5
                    data.Character.stats['Def'] = 1
                    data.Character.stats['SpD'] = 2
                    data.Character.stats['Cla'] = "Tactician"
                    self.classpick = False
                else:
                    print "That's not a option..."
        self.final_cheack = True
        while self.final_cheack:
            print "So you are a %s %s who goes by them name %s, correct?" % (data.Character.stats['Sex'],
                                                     data.Character.stats['Cla'], data.Character.stats['Nam'])
            self.final_choses = raw_input()
            if (self.final_choses == 'yes') or (self.final_choses == 'Yes'):
                return "Forest"
            elif (self.final_choses == 'no') or (self.final_choses == 'No'):
                return "Intro"
                

class StartingScreen(Scene):
    def enter(self):
        #print enterdashenter
        print "Welcome to Fanstaty Game (name in devolpement)"
        if SaveData.GameSaved == True:
            print 'If you wish to load your save file type "load"'
            print 'If you want start a new game type "start"'
        else:
            print 'You have no save data. To start type "start"'
        print enterdashenter
        self.action = True
        while self.action:
            print "What do you wish to do?"
            self.option = raw_input()
            if (self.option == 'load') and (SaveData.GameSaved == True):
                data.Character.stats = SaveData.Character.stats
                return SaveData.LastScene
            elif self.option == 'start':
                return 'Intro'
            else:
                print "thats not an option"
                
class Menu(Scene):
    def enter(self):
        print """---------
Stats
Equipment
Items
Save
Return"""
        Menu_Choice = raw_input()
        if (Menu_Choice == 'Stats') or (Menu_Choice == 'stats'):
            print """HP: %d/%d
MP: %d/%d
Attack: %d
Defence: %d
Special Attack: %d
Special Defence: %d""" % (data.Character.stats['HP'], data.Character.stats['HP_Max'],
                          data.Character.stats['Mag'], data.Character.stats['Mag_Max'],
                          data.Character.stats['Atk'], data.Character.stats['Def'], 
                          data.Character.stats['SpA'], data.Character.stats['SpD'])
            return 'Menu'
        elif (Menu_Choice == 'Equipment') or (Menu_Choice == 'equipment'):
            return 'Equipment'

class Equipment(Scene):
    def enter(self):
        if data.Character.equ_item == 0:
            print "You don't have any items"
        else:
            pass
        itemlist = data.Character.equ_item
        print enterdashenter
        print "Pick an item\n"
        for items in itemlist:
            print items
        self.instence = data.Items()
        self.list = data.Character.equ_item
        self.Option = raw_input()
        Option_Final = self.instence.check_action(self.list, self.Option)
        if Option_Final == True:
            pass
        elif Option_Final == False:
            print "That isn't an item in your inventory..."
            return 'Menu'
        print "what do you want to do with %s" % self.Option
        New_Option = raw_input()
        
            

class Map(object):
    Scene = {
        'Intro': Intro(),
        'Battle': Battle(),
        'OverWorld': OverWorld(),
        'StartingScreen': StartingScreen(),
        'Forest': Forest(),
        'Menu': Menu(),
        'Equipment': Equipment()
    }
    def __init__(self, start_scene):
        self.start_scene = start_scene
    def next_scene(self, scene_name):
        return Map.Scene.get(scene_name)
    def opening_scene(self):
        return self.next_scene(self.start_scene)

The_Map = Map("StartingScreen")
The_Game = Engine(The_Map)
The_Game.play()

#The_Map = Map('Menu')
#The_Game = Engine(The_Map)
#The_Game.play()