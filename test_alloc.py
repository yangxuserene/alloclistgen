from torus import Torus 
from dragonfly import Dragonfly


#  jobrank_list = [216, 125, 100]
#  Dragonfly(8, 33, 'rand_router', jobrank_list, 1)
#  Dragonfly(8, 33, 'rand_group', jobrank_list, 1)
#  Dragonfly(8, 33, 'rand_node', jobrank_list, 1)
Dragonfly(8, 33, 'hyb', jobrank_list, 3)

