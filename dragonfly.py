import random
from enum import Enum

class NetworkType(Enum):
    # network type
    Dragonfly = 1
    Torus = 2


class Network(object):
    def __init__(self, ntype):
        self.network_type = ntype
        if self.network_type == NetworkType.Dragonfly:
            self.num_router = 8
            self.num_group = 33
            self.total_node = self.num_router*self.num_router*self.num_group/2
        elif self.network_type == NetworkType.Torus:
            self.dim = [8,16,16]
            self.total_node = 1
            for item in self.dim:
                self.total_node *= item

class Dragonfly(object):
    def __init__(self, router, group, alloc_type, job_rank, num_seed):
        self.num_router = router
        self.num_group = group
        self.total_node = self.num_router*self.num_router*self.num_group/2
        self.job_rank = job_rank
        self.alloc_type = alloc_type
        self.num_seed = num_seed
        self.alloc_file_prefix()
        self.load_alloc()

    def alloc_file_prefix(self):
        self.alloc_file = self.alloc_type+'-alloc-'+str(self.total_node)+'-'
        for jobsize in self.job_rank:
            self.alloc_file += str(jobsize)+'_'
            #print self.alloc_file
        self.alloc_file = self.alloc_file[:-1]

    def load_alloc(self):
        if self.alloc_type == 'cont':
            print "this is dragonfly cont alloc"
            self.cont_alloc()
        elif self.alloc_type == 'rand':
            print "this is dragonfly rand alloc"
            self.random_alloc()
        elif self.alloc_type == 'rand_router' or 'rand_group' or 'rand_node':
            print "Dragonfly "+ self.alloc_type + " Allocation!"
            self.random_router_alloc()
        else:
            print slef.alloc_type +" Function Not Supported Yet!"
            exit()

    def random_router_alloc(self):
        #  chunk_size is the num of consecutive nodes 
        #  chunk_size equals to num of nodes attached to a router for router level random allocation
        #  chunk_size equals to num of nodes in each group for group level random allocation
        if self.alloc_type == 'rand_router':
            chunk_size = self.num_router/2
        elif self.alloc_type == 'rand_group':
            chunk_size = self.num_router * self.num_router/2
        elif self.alloc_type == 'rand_node':
            chunk_size = 1

        for seed in range(self.num_seed):
            self.alloc_file += '-'+str(seed)
            #print self.alloc_file
            f = open(self.alloc_file+'.conf', 'w')
            node_list = range(0, int(self.total_node))
            random.seed(seed)
            for rank in self.job_rank:
                #each job needs 'num_chunk' of nodes
                num_chunk = rank/chunk_size if rank%chunk_size == 0 else (rank/chunk_size)+1
                alloc_list = []
                for i in range(num_chunk):
                    idx = random.randint(0, len(node_list)-chunk_size)
                    alloc_list += node_list[idx:idx+chunk_size]
                    node_list = [elem for elem in node_list if (elem not in alloc_list)]
                print alloc_list
                for idx in range(rank):
                    f.write("%s " % alloc_list[idx])
                f.write("\n")
            f.closed
            self.alloc_file=self.alloc_file[:-2]


    def random_alloc(self):
        for seed in range(self.num_seed):
            self.alloc_file += '-'+str(seed)
            #print self.alloc_file
            f = open(self.alloc_file+'.conf', 'w')
            node_list = range(0, int(self.total_node))
            random.seed(seed)
            for rankid in self.job_rank:
                alloc_list = random.sample(node_list, rankid)
                node_list = [i for i in node_list if (i not in alloc_list)]
                #print "length of alloc list", len(alloc_list), "\n", alloc_list,"\n"
                for idx in range(len(alloc_list)):
                    f.write("%s " % alloc_list[idx])
                f.write("\n")
            f.closed
            self.alloc_file=self.alloc_file[:-2]

    def cont_alloc(self):
        f = open(self.alloc_file, 'w')
        start = 0
        for num_rank in self.job_rank:
            for rankid in range(start, start+ num_rank):
                f.write("%s " % rankid)
            f.write("\n")
            start += num_rank
        f.closed

    def hybrid_alloc(self, job_rank):
        #1st job get contiguous allocation , the other job get random allocation
        f = open(alloc_file, 'w')
        node_list = range(0, int(self.total_node))
        random.seed(0)
        group_size = 32
        for rankid in range(len(job_rank)):
            if(rankid == 0):
                job_size = job_rank[rankid]
                num_groups = job_size/group_size +1;#job_0 will take this number of groups
                alloc_list = node_list[0: job_rank[rankid]]
                node_list = node_list[num_groups*group_size : ]
            else:
                alloc_list = random.sample(node_list, job_rank[rankid])

            node_list = [i for i in node_list if (i not in alloc_list)]
            print "length of alloc list", len(alloc_list), "\n", alloc_list,"\n"
            for idx in range(len(alloc_list)):
                f.write("%s " % alloc_list[idx])
            f.write("\n")
        f.closed

    def hybrid_alloc_2 (self, job_rank):
        #1st and 2nd job get contiguous allocation , 3rd job get random allocation
        f = open(alloc_file, 'w')
        node_list = range(0, int(self.total_node))
        random.seed(0)
        group_size = 32
        for rankid in range(len(job_rank)):
            #if(rankid !=2 2 ):
            if(rankid < 3 ):#all job get contiguous allocation
                job_size = job_rank[rankid]
                num_groups = job_size/group_size +1;#job_0 and job_1 will take this number of groups
                alloc_list = node_list[0: job_rank[rankid]]
                node_list = node_list[num_groups*group_size : ]
            else:
                alloc_list = random.sample(node_list, job_rank[rankid])

            node_list = [i for i in node_list if (i not in alloc_list)]
            print "length of alloc list", len(alloc_list), "\n", alloc_list,"\n"
            for idx in range(len(alloc_list)):
                f.write("%s " % alloc_list[idx])
            f.write("\n")
        f.closed



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

