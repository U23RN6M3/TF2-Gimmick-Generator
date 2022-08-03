import random
from re import A
from sre_constants import NEGATE
from turtle import color
import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graphical Word Generator")

DEFAULT_FONT = pygame.font.SysFont('comicsans', 15)
FPS = 60

WHITE = (255, 255, 255)
GREEN = (0, 255, 200)
RED = (255, 70, 70)
YELLOW = (255, 255, 0)

def draw_window(req, result, include_unlockables, include_reskins):
    bg = pygame.Surface((WIDTH, HEIGHT))
    WIN.blit(bg, (0, 0))

    a = RED
    b = RED

    if include_unlockables == False:
        a = RED
    else:
        a = GREEN
    
    if include_reskins == False:
        b = RED
    else:
        b = GREEN

    include_unlockables = DEFAULT_FONT.render("(m) Include Unlockables: " + str(include_unlockables), 1, a)
    include_reskins = DEFAULT_FONT.render("(n) Include Reskins: " + str(include_reskins), 1, b)
    result = DEFAULT_FONT.render("(Arrow Up) Result: " + str(result), 1, YELLOW)
    requirements = DEFAULT_FONT.render("Requirements: " + str(req), 1, YELLOW)
    WIN.blit(include_reskins, (10, 90))
    WIN.blit(include_unlockables, (10, 70))
    WIN.blit(result, (10, 10))
    WIN.blit(requirements, (10, 40))
    
    pygame.display.update()

def main():

    recalled = True
    run = True
    clock = pygame.time.Clock()

    observations = [
        "Observant",
        "Aggressive",
        "Judgeful",
        "Crouching",
        "Talkative",
        "Friendly",
        "Irritating",
        "Funny",
        "Teammate-Ignorant",
        "Tryhard",
        "Helpful",
        "Spy-Paranoid",
        "Enemy-Helping"
    ]

    class_weapon_library = {
        "Primaries":{
            "Scout":[
                "Force-a-Nature",
                "Shortstop",
                "Soda Popper",
                "Baby Face's Blaster",
                "Back Scatter"
            ],
            "Soldier":[
                "Original",
                "Direct Hit",
                "Black Box",
                "Rocket Jumper",
                "Liberty Launcher",
                "Cow Mangler 5000",
                "Beggar's Bazooka",
                "Air Strike"
            ],
            "Pyro":[
                "Rainblower",
                "&&Nostromo Napalmer",
                "Backburner",
                "Degreaser",
                "Phlogistinator",
                "Dragon's Fury"
            ],
            "Demo":[
                "Loch-n-Load",
                "Ali Baba's Wee Booties",
                "Bootlegger",
                "Loose Cannon",
                "B.A.S.E. Jumper",
                "Iron Bomber"
            ],
            "Heavy":[
                "&&Iron Curtain",
                "Natascha",
                "Brass Beast",
                "Tomislav",
                "Huo-Long Heater"
            ],
            "Engineer":[
                "Frontier Justice",
                "Widowmaker",
                "Pomson 6000",
                "Rescue Ranger",
                "Panic Attack"
            ],
            "Medic":[
                "Syringe gun",
                "Blutsauger",
                "Crusader's Crossbow",
                "Overdose"
            ],
            "Sniper":[
                "Sniper Rifle",
                "&&AWper Hand",
                "Huntsman",
                "&&Fortified Compound",
                "Sydney Sleeper",
                "Bazaar Bargain",
                "Machina",
                "&&Shooting Star",
                "Hitman's Heatmaker",
                "Classic"
            ],
            "Spy":[
                "Revolver",
                "&&Big Kill",
                "Diamondback",
                "Ambassador",
                "L'Etranger",
                "Enforcer"
            ]
        },
        "Secondaries":{
            "Scout":[
                "&&Lugermorph",
                "&&C.A.P.P.E.R",
                "Winger",
                "Pretty Boy's Pocket Pistol",
                "Flying Guillotine",
                "Bonk! Atomic Punch",
                "Crit-o-Cola",
                "Mad Milk",
                "&&Mutated Milk"
            ],
            "Soldier":[
                "&&Reserve Shooter",
                "Buff Banner",
                "Gunboats",
                "Battalions Backup",
                "Concheror",
                "Mantreads",
                "Righteous Bison",
                "B.A.S.E. Jumper",
                "Panic Attack"
            ],
            "Pyro":[
                "&&Reserve Shooter",
                "Flare Gun",
                "Detonator",
                "Manmelter",
                "Scorch Shot",
                "Panic Attack",
                "Thermal Thruster",
                "Gas Passer"
            ],
            "Demo":[
                "Scottish Resistance",
                "Chargin' Targe",
                "Sticky Jumper",
                "Splendid Screen",
                "Tide Turner",
                "Quickiebomb Launcher"
            ],
            "Heavy":[
                "Family Business",
                "Sandvich",
                "&&Robo-Sandvich",
                "Dalakohs Bar",
                "&&Fishcake",
                "Buffalo Steak Sandvich",
                "Panic Attack",
                "Second Banana"
            ],
            "Engineer":[
                "&&Lugermorph",
                "&&C.A.P.P.E.R.",
                "Wrangler",
                "&&Giger Counter",
                "Short Circuit"
            ],
            "Medic":[
                "Kritzkreig",
                "Quick-Fix",
                "Vaccinator"
            ],
            "Sniper":[
                "Cleaner's Carbine",
                "Jarate",
                "&&Self-Aware Beauty Mark",
                "Razorback",
                "Darwin's Danger Shield",
                "Cozy Camper"
            ],
            "Spy":[
                "&&Ap-Sap",
                "&&Snack Attack",
                "Red-Tape Recorder"
            ],
        },
        "Melees":{
            "Scout":[
                "Holy Mackerel",
                "&&Unarmed Combat",
                "&&Batsaber",
                "Sandman",
                "Candy Cane",
                "Boston Basher",
                "Three-Rune Blade",
                "Sun-on-a-Stick",
                "Fan O' War",
                "Atomizer",
                "Wrap Assasin"
            ],
            "Soldier":[
                "Equalizer",
                "Pain Train",
                "Half-Zatochi",
                "Disiplinary Action",
                "Market Gardener",
                "Escape Plan"
            ],
            "Pyro":[
                "Lollichop",
                "Axtinguisher",
                "&&Postal Plummeler",
                "Homewrecker",
                "&&Maul",
                "Powerjack",
                "Back Scratcher",
                "Sharpened Volcano Fragment",
                "Third Degree",
                "Neon Annihilator",
                "Hot Hand"
            ],
            "Demo":[
                "&&Scottish Handshake",
                "Eyelander",
                "&&Horseless Headless Horsemann's Headtaker",
                "&&Nessie's Nine Iron",
                "Scotsman's Skullcutter",
                "Pain Train",
                "Ullapool Caber",
                "Claidheamh Mor",
                "Half-Zatochi",
                "Persian Persuader"
            ],
            "Heavy":[
                "&&Apoco-Fists",
                "KGB",
                "GRU",
                "&&Bread Bite",
                "Warrior's Spirit",
                "Fists of Steel",
                "Eviction Notice",
                "Holiday Punch"
            ],
            "Engineer":[
                "&&Golden Wrench",
                "Gunslinger",
                "Southern Hospitality",
                "Jag",
                "Eaureka Effect"
            ],
            "Medic":[
                "Ubersaw",
                "Vita-Saw",
                "Amputator",
                "Solemn Vow"
            ],
            "Sniper":[
                "Tribalman's Shiv",
                "Bushwacka",
                "Shahanshah"
            ],
            "Spy":[
                "&&Sharp Dresser",
                "&&Black Rose",
                "Your Eternal Award",
                "&&Wanga Prick",
                "Conniver's Kunai",
                "Big Earner",
                "Spy-cicle"
            ],
        },
    }

    class_specific_primary_weapons = {
        "Scout":[
            "Scattergun",
        ],
        "Soldier":[
            "Rocket Launcher"
        ],
        "Pyro":[
            "Flamethrower"
        ],
        "Demo":[
            "Grenade Launcher"
        ],
        "Heavy":[
            "Minigun"
        ],
        "Engineer":[
            "Shotgun"
        ],
        "Medic":[
            "Syringe gun"
        ],
        "Sniper":[
            "Sniper Rifle"
        ],
        "Spy":[
            "Revolver"
        ]
    }

    class_specific_secondary_weapons = {
        "Scout":[
            "Pistol",
        ],
        "Soldier":[
            "Shotgun"
        ],
        "Pyro":[
            "Shotgun"
        ],
        "Demo":[
            "Stickybomb Launcher"
        ],
        "Heavy":[
            "Shotgun"
        ],
        "Engineer":[
            "Pistol"
        ],
        "Medic":[
            "Medigun"
        ],
        "Sniper":[
            "SMG"
        ],
        "Spy":[
            "Sapper"
        ]
    }

    class_specific_melee_weapons = {
        "Scout":[
            "Bat",
        ],
        "Soldier":[
            "Shovel"
        ],
        "Pyro":[
            "Axe"
        ],
        "Demo":[
            "Bottle"
        ],
        "Heavy":[
            "Fists"
        ],
        "Engineer":[
            "Wrench"
        ],
        "Medic":[
            "Bonesaw"
        ],
        "Sniper":[
            "Kukri"
        ],
        "Spy":[
            "Knife"
        ]
    }

    class_special_items = {
        "Spy":[
            "Invis Watch",
            "Cloak n Dagger",
            "Deadringer",
            "Don't Disguise",
            "Don't Backstab",
            "Don't Sap Buildings",
            "Don't go Invis",
            "Don't move while Invis",
            "Don't move without Invis",
            "Don't Cap"
        ],
        "Engineer":[
            "PDAs",
            "Only build Sentries",
            "Only build Dispensers",
            "Only build Teleporters",
            "Don't Teleport"
            "Don't use PDAs",
            "Don't build Sentries",
            "Don't build Dispensers",
            "Don't build Teleporters",
            "Don't Upgrade Buildings",
            "Don't Destroy Sappers",
            "Don't Self Destruct Buildings",
        ],
        "Sniper":[
            "Don't Spycheck",
            "Always Spycheck",
            "Don't Headshot",
            "Don't Scope",
        ]
        
    }

    tf2classes = [
        "Scout",
        "Soldier",
        "Pyro",
        "Demo",
        "Heavy",
        "Engineer",
        "Medic",
        "Sniper",
        "Spy"
    ]

    result = ""
    req = ""

    include_unlockables = False
    include_reskins = False

    while run == True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            key_pressed = pygame.key.get_pressed()

            if event.type == pygame.KEYDOWN:
                if key_pressed[pygame.K_m]:
                    if include_unlockables == False:
                        include_unlockables = True
                    elif include_unlockables == True:
                        include_unlockables = False
                
                if key_pressed[pygame.K_n]:
                    if include_reskins == False:
                        include_reskins = True
                    elif include_reskins == True:
                        include_reskins = False
                

                if key_pressed[pygame.K_UP]:
                    random.shuffle(observations)
                    random.shuffle(tf2classes)
                    tf2class = tf2classes[0]
                    slot_eliminator = random.randint(1, 5)
                    
                    b = "Don't Primary"
                    c = "Don't Secondary"
                    d = "Don't Melee"
                    e = ""
                    
                    primary_list = []
                    secondary_list = []
                    melee_list = []

                    if tf2class == "Spy" or tf2class == "Engineer" or tf2class == "Sniper":
                        random.shuffle(class_special_items[tf2class])
                        e = ", " + class_special_items[tf2class][0]
                    if slot_eliminator != 1:
                        random.shuffle(class_specific_primary_weapons[tf2class])
                        random.shuffle(class_weapon_library["Primaries"][tf2class])
                        if include_unlockables == True:
                            for i in class_weapon_library["Primaries"][tf2class]:
                                if include_reskins == False:
                                    if i[:2] != "&&":
                                        primary_list.append(i)
                                else:
                                    if i[:2] == "&&":
                                        primary_list.append(i[2:])
                                    else:
                                        primary_list.append(i)
                        for i in class_specific_primary_weapons[tf2class]:
                            primary_list.append(i)
                        b = primary_list[0]
                    if slot_eliminator != 2:
                        random.shuffle(class_specific_secondary_weapons[tf2class])
                        random.shuffle(class_weapon_library["Secondaries"][tf2class])
                        if include_unlockables == True:
                            for i in class_weapon_library["Secondaries"][tf2class]:
                                if include_reskins == False:
                                    if i[:2] != "&&":
                                        secondary_list.append(i)
                                else:
                                    if i[:2] == "&&":
                                        secondary_list.append(i[2:])
                                    else:
                                        secondary_list.append(i)
                        for i in class_specific_secondary_weapons[tf2class]:
                            secondary_list.append(i)
                        c = secondary_list[0]
                    if slot_eliminator != 3:
                        random.shuffle(class_specific_melee_weapons[tf2class])
                        random.shuffle(class_weapon_library["Melees"][tf2class])
                        if include_unlockables == True:
                            for i in class_weapon_library["Melees"][tf2class]:
                                if include_reskins == False:
                                    if i[:2] != "&&":
                                        melee_list.append(i)
                                else:
                                    if i[:2] == "&&":
                                        melee_list.append(i[2:])
                                    else:
                                        melee_list.append(i)
                        for i in class_specific_melee_weapons[tf2class]:
                            melee_list.append(i)
                        d = melee_list[0]
                    
                    a = " | Name: " + " " + observations[0] + " " + observations[1] + " " + tf2class
                    req = " | Required Items: " + b + ", " + c + ", " + d + e
                    result = a
                
            draw_window(req, result, include_unlockables, include_reskins)
    if recalled == True:
        main()

if __name__ == "__main__":
    main()