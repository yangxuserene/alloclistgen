#!/usr/bin/python 
from torus import Torus 
from dragonfly import Dragonfly


jobrank_list = [216, 125, 100]
Dragonfly(8, 33, 'rand_rotr', jobrank_list, 1)
#  Dragonfly(8, 33, 'rand_part', jobrank_list, 1)
#  Dragonfly(8, 33, 'rand_grop', jobrank_list, 1)
#  Dragonfly(8, 33, 'rand_node', jobrank_list, 1)
#  Dragonfly(8, 33, 'hyb', jobrank_list, 1)
#  Dragonfly(8, 33, 'cont-perm', jobrank_list, 10)
#  Dragonfly(8, 33, 'rand_node', jobrank_list, 1)
#  Dragonfly(8, 33, 'cont', jobrank_list, 10)

#  single_job = [[100]]
#  for item in single_job:
    #  Dragonfly(8, 33, 'rand_rotr', item, 10)
    #  Dragonfly(8, 33, 'rand_node', item, 1)
    #  Dragonfly(8, 33, 'rand_grop', item, 1)

#  jobrank_list = [10, 5, 10]
#  torus_dim = [8, 16, 16]
#  Torus(torus_dim, 'cont', jobrank_list, 3)
#  Torus(torus_dim, 'rand', jobrank_list, 3)
#  Torus(torus_dim, 'hyb', jobrank_list, 3)

#===============================================================
# Permutation Study 
#===============================================================
#  CrystalRouter = [100]
#  Dragonfly(8, 33, 'cont', CrystalRouter, 0)
#  Dragonfly(8, 33, 'cont-perm', CrystalRouter, 10)
#  Dragonfly(8, 33, 'rand_node', CrystalRouter, 10)
#  Dragonfly(8, 33, 'rand-perm', CrystalRouter, 1)


#  AMG = [216]
#  Dragonfly(8, 33, 'cont', AMG, 0)
#  Dragonfly(8, 33, 'cont-perm', AMG, 10)
#  Dragonfly(8, 33, 'rand_node', AMG, 10)
#  Dragonfly(8, 33, 'rand-perm', AMG, 1)

#  MG = [125]
#  Dragonfly(8, 33, 'cont', MG, 0)
#  Dragonfly(8, 33, 'cont-perm', MG, 10)
#  Dragonfly(8, 33, 'rand_node', MG, 10)
#  Dragonfly(8, 33, 'rand-perm', MG, 1)

#===============================================================
# End of Permutation Study 
#===============================================================

