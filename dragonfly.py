import random
from enum import Enum

class Dragonfly(object):
    def __init__(self, router, group, alloc_type, job_rank, num_seed):
        self.num_router_per_group = router
        self.num_group = group
        self.num_node_per_router = self.num_router_per_group/2
        self.total_node = self.num_router_per_group*self.num_node_per_router*self.num_group
        self.total_router = self.num_router_per_group*self.num_group
        self.job_rank = job_rank
        self.alloc_type = alloc_type
        self.num_seed = num_seed
        self.alloc_file_prefix()
        self.load_alloc()

    def alloc_file_prefix(self):
        self.alloc_file = self.alloc_type+'-alloc-'+str(self.total_node)+'-'
        for jobsize in self.job_rank:
            self.alloc_file += str(jobsize)+'_'
        self.alloc_file = self.alloc_file[:-1]

    def load_alloc(self):
        if self.alloc_type == 'cont':
            print "this is dragonfly cont alloc"
            self.cont_alloc()
        elif self.alloc_type == 'rand_rotr':
            self.random_router_alloc();
            print "Dragonfly "+ self.alloc_type + " Allocation!"
        elif self.alloc_type == 'rand_grop':
            self.random_group_alloc();
            print "Dragonfly "+ self.alloc_type + " Allocation!"
        elif self.alloc_type == 'rand_node':
            print "Dragonfly "+ self.alloc_type + " Allocation!"
            self.random_alloc()
        elif self.alloc_type == 'rand_part':
            print "Dragonfly "+ self.alloc_type + " Allocation!"
            self.random_partition_alloc()
        elif self.alloc_type == 'rand-perm':
            print "lists of permutations of a random allocated node set "
            self.random_permutation()
        elif self.alloc_type == 'hyb':
            print "Dragonfly xxx "+ self.alloc_type + " Allocation!"
            self.hybrid_alloc()
        elif self.alloc_type == 'cont-perm':
            print "Dragonfly different permutation of Contiguous Allocation"
            self.cont_permutation()
        elif self.alloc_type == 'op_rand':
            print "Dragonfly Over Provision Random Allocation!"
            self.overprovision_random_alloc()
        else:
            print self.alloc_type +" Function Not Supported Yet!"
            exit()



    def cont_alloc(self):
        f = open(self.alloc_file+'.conf', 'w')
        start = 0
        for num_rank in self.job_rank:
            for rankid in range(start, start+ num_rank):
                f.write("%s " % rankid)
            f.write("\n")
            start += num_rank
        f.closed
    
    def random_router_alloc(self):
        for seed in range(self.num_seed):
            tmp_filename = self.alloc_file
            self.alloc_file = self.alloc_file[:9]+str(seed)+self.alloc_file[9:]
            #print self.alloc_file
            f = open(self.alloc_file+'.conf', 'w')
            random.seed(seed)
            router_id_list = list(xrange(self.total_router))
            for rank in self.job_rank:
                alloc_list = []
                while(len(alloc_list) < rank):
                    router_id = random.choice(router_id_list)
                    router_id_list.remove(router_id)
                    node_id_start = router_id*self.num_node_per_router
                    for x in range(self.num_node_per_router):
                        alloc_list.append(node_id_start+x)
                alloc_list = alloc_list[:rank]
                #  print alloc_list, '\n', len(alloc_list)
                for item in alloc_list:
                    f.write("%s " % item)
                f.write("\n")

            f.closed
            self.alloc_file= tmp_filename

    def random_group_alloc(self):
        num_node_per_group = self.num_router_per_group*self.num_node_per_router
        for seed in range(self.num_seed):
            tmp_filename = self.alloc_file
            self.alloc_file = self.alloc_file[:9]+str(seed)+self.alloc_file[9:]
            #print self.alloc_file
            f = open(self.alloc_file+'.conf', 'w')
            random.seed(seed)
            group_id_list = list(xrange(self.num_group))
            for rank in self.job_rank:
                alloc_list = []
                while(len(alloc_list) < rank):
                    group_id = random.choice(group_id_list)
                    group_id_list.remove(group_id)
                    node_id_start = group_id*num_node_per_group
                    for x in range(num_node_per_group):
                        alloc_list.append(node_id_start+x)
                alloc_list = alloc_list[:rank]
                #  print alloc_list, '\n', len(alloc_list)
                for item in alloc_list:
                    f.write("%s " % item)
                f.write("\n")

            f.closed
            self.alloc_file= tmp_filename


    def random_partition_alloc(self):
        num_node_per_partition = 8
        for seed in range(self.num_seed):
            tmp_filename = self.alloc_file
            self.alloc_file = self.alloc_file[:9]+str(seed)+self.alloc_file[9:]
            #print self.alloc_file
            f = open(self.alloc_file+'.conf', 'w')
            random.seed(seed)
            partition_id_list = list(xrange(self.total_node / num_node_per_partition ))
            for rank in self.job_rank:
                alloc_list = []
                while(len(alloc_list) < rank):
                    partition_id = random.choice(partition_id_list)
                    partition_id_list.remove(partition_id)
                    node_id_start = partition_id*num_node_per_partition
                    for x in range(num_node_per_partition):
                        alloc_list.append(node_id_start+x)
                alloc_list = alloc_list[:rank]
                #  print alloc_list, '\n', len(alloc_list)
                for item in alloc_list:
                    f.write("%s " % item)
                f.write("\n")

            f.closed
            self.alloc_file= tmp_filename



    def random_alloc(self):
        chunk_size = 1
        #  chunk_size is the num of consecutive nodes 
        for seed in range(self.num_seed):
            tmp_filename = self.alloc_file
            self.alloc_file = self.alloc_file[:9]+str(seed)+self.alloc_file[9:]
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
                #  print alloc_list[0:rank]
                for idx in range(rank):
                    f.write("%s " % alloc_list[idx])
                f.write("\n")
            f.closed
            self.alloc_file= tmp_filename

    def random_permutation(self):
        #each job gets random nodes set,
        #randomize that nodes set sequence resulting random mapping with random allocation
        for seed in range(self.num_seed):#num. of random node set for each job
            tmp_filename = self.alloc_file
            #  self.alloc_file += '-'+'perm'+str(seed)
            node_list = range(0, int(self.total_node))
            random.seed(seed)
            for rank in self.job_rank:
                alloc_list = random.sample(node_list, rank)
                node_list = [elem for elem in node_list if (elem not in alloc_list)]
                for perm_seed in range(10):#num. of permutation for each node set
                    self.alloc_file = self.alloc_file[:9]+str(seed)+str(perm_seed)+self.alloc_file[9:]
                    f = open(self.alloc_file+'.conf', 'a')
                    self.alloc_file=tmp_filename
                    random.seed(perm_seed)
                    random.shuffle(alloc_list)
                    #  alloc_list.sort()
                    for idx in range(rank):
                        f.write("%s " % alloc_list[idx])
                    f.write("\n")
                f.closed

    def cont_permutation(self):
        for seed in range(self.num_seed):
            file_surfix = self.alloc_file
            self.alloc_file = self.alloc_file[:9]+str(seed)+self.alloc_file[9:]
            f = open(self.alloc_file+'.conf', 'w')
            start = 0
            for num_rank in self.job_rank:
                alloc_list = range(start, start+num_rank)
                random.seed(seed)
                #  if num_rank == 216:#AMG gets random mapping, others get consecutive mapping
                random.shuffle(alloc_list)
                #  alloc_list.sort()
                for item in alloc_list:
                    f.write("%s " % item)
                f.write("\n")
                start += num_rank
            f.closed
            self.alloc_file = file_surfix 

    def hybrid_alloc(self):
        #  the first 'cont_job_num' jobs get contiguous allocation 
        #  the other job get random allocation
        cont_job_num = 1
        for seed in range(self.num_seed):
            self.alloc_file += '-'+str(seed)
            f = open(self.alloc_file+'.conf', 'w')
            node_list = range(0, int(self.total_node))
            random.seed(seed)
            group_size = self.num_router_per_group*self.num_router_per_group/2 
            for rankid in range(len(self.job_rank)):
                if(rankid < cont_job_num ):
                    job_size = self.job_rank[rankid]
                    alloc_list = node_list[0: job_size]
                    node_list = node_list[job_size: ]
                else:
                    alloc_list = random.sample(node_list, self.job_rank[rankid])
                node_list = [i for i in node_list if (i not in alloc_list)]
                for idx in range(len(alloc_list)):
                    f.write("%s " % alloc_list[idx])
                f.write("\n")
            f.closed
            self.alloc_file=self.alloc_file[:-2]

    def overprovision_random_alloc(self):
        # each job gets random allocation in a over provision area
        # the size of the area is TWICE as mush as the job size
        for seed in range(self.num_seed):
            self.alloc_file += '-'+str(seed)
            f = open(self.alloc_file+'.conf', 'w')
            node_list = range(0, int(self.total_node))
            random.seed(seed)
            start = 0
            for num_rank in range(len(self.job_rank)):
                op_size = self.job_rank[num_rank]*2
                op_list = node_list[start : start+op_size]
                node_list = node_list[start+op_size: ]
                alloc_list = random.sample(op_list, self.job_rank[num_rank])
                #  alloc_list.sort()
                #  print "length of alloc list", len(alloc_list), "\n", alloc_list,"\n"
                for idx in range(len(alloc_list)):
                    f.write("%s " % alloc_list[idx])
                f.write("\n")
            f.closed
            self.alloc_file=self.alloc_file[:-2]
