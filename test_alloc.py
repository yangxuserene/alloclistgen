from torus import Torus 
from dragonfly import Dragonfly


#  jobrank_list = [216, 125, 100]
#  Dragonfly(8, 33, 'rand_router', jobrank_list, 1)
#  Dragonfly(8, 33, 'rand_group', jobrank_list, 1)
#  Dragonfly(8, 33, 'rand_node', jobrank_list, 1)
#  Dragonfly(8, 33, 'hyb', jobrank_list, 3)
jobrank_list = [10, 5, 10]
Dragonfly(8, 33, 'op_rand', jobrank_list, 3)

#  jobrank_list = [10, 5, 10]
#  torus_dim = [8, 16, 16]
#  Torus(torus_dim, 'cont', jobrank_list, 3)
#  Torus(torus_dim, 'rand', jobrank_list, 3)
#  Torus(torus_dim, 'hyb', jobrank_list, 3)

