from operator import index
import sys
import math
from dataclasses import dataclass
from random import randrange

from scipy import rand

ME = 1
OPP = 0
NONE = -1

@dataclass
class Tile:
    x: int
    y: int
    scrap_amount: int
    owner: int
    units: int
    recycler: bool
    can_build: bool
    can_spawn: bool
    in_range_of_recycler: bool

@dataclass
class Target:
    x: int
    y: int

width, height = [int(i) for i in input().split()]
nb_turn = 0
# game loop
while True:
    tiles = []
    my_units = []
    opp_units = []
    my_recyclers = []
    opp_recyclers = []
    opp_tiles = []
    my_tiles = []
    neutral_tiles = []

    my_matter, opp_matter = [int(i) for i in input().split()]
    for y in range(height):
        for x in range(width):
            # owner: 1 = me, 0 = foe, -1 = neutral
            # recycler, can_build, can_spawn, in_range_of_recycler: 1 = True, 0 = False
            scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler = [int(k) for k in input().split()]
            tile = Tile(x, y, scrap_amount, owner, units, recycler == 1, can_build == 1, can_spawn == 1, in_range_of_recycler == 1)

            tiles.append(tile)

            if tile.owner == ME:
                my_tiles.append(tile)
                if tile.units > 0:
                    my_units.append(tile)
                elif tile.recycler:
                    my_recyclers.append(tile)
            elif tile.owner == OPP:
                opp_tiles.append(tile)
                if tile.units > 0:
                    opp_units.append(tile)
                elif tile.recycler:
                    opp_recyclers.append(tile)
            else:
                neutral_tiles.append(tile)

    actions = []

    dist_milieu = [math.dist([width/2,height/2],[t.x,t.y]) if t.can_spawn else 999 for t in my_tiles]
    tuile_spawn = my_tiles[dist_milieu.index(min(dist_milieu))]
    if my_matter >= 10:
        amount = int(my_matter/10)
        actions.append('SPAWN {} {} {}'.format(amount, tuile_spawn.x, tuile_spawn.y))
    for tile in my_tiles:
        if tile.can_spawn:
            amount=0     
            if amount > 0:
                actions.append('SPAWN {} {} {}'.format(amount, tile.x, tile.y))
        if tile.can_build:
            should_build = False # TODO: pick whether to build recycler here
            if nb_turn == 0:
                should_build = True
            if should_build:
                actions.append('BUILD {} {}'.format(tile.x, tile.y))


    for tile in my_units:

        distance = [math.dist([tile.x,tile.y],[t.x,t.y]) for t in opp_tiles]
        tuile_proche = opp_tiles[distance.index(min(distance))]
        target = Target(tuile_proche.x,tuile_proche.y)
      
        if target:
            amount = tile.units # TODO: pick amount of units to move
            actions.append('MOVE {} {} {} {} {}'.format(amount, tile.x, tile.y, target.x, target.y))

    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    nb_turn+=1
    print(';'.join(actions) if len(actions) > 0 else 'WAIT')


# def tuiles_adj(tiles,index):
#     liste_tuiles_dispo = []
#     if index > 0 or index//width > 0:
#         if tiles[index-1].owner == NONE:
#             liste_tuile_dipso.append(tiles[index-1])

