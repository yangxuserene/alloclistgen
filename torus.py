import random
from enum import Enum

class Torus(object):
    def __init__(self, dim):
        self.dim = dim 
        self.total_node = 1
        for item in self.dim:
            self.total_node *= item


    def cont_alloc(self, job_ranks):
        print "this is TORUS cont alloc"
        f = open('torus_test_alloc.conf', 'w')
        start = 0
        for num_rank in job_ranks:
            for rankid in range(start, start+ num_rank):
                f.write("%s " % rankid)
            f.write("\n")
            start += num_rank
        f.closed

