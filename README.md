# alloclistgen

This script is for job allocation list generation. It support only 4 different allocation strategies now.

#######################################################################################
1.Contigous Allocation -- "CONT"
assign nodes to each job contigously and each job will get a compact, contiguous allocation

2.Partition Allocation -- "CHUNK"
each job will get a compact allocation, the size of which would the one or multiple chunks.
the size of chunk could be predefined.

3.Stripe Allocation -- "STRIPE"
image the outfit of a zebar(only two jobs), or a multiple-color zebar (when there are several jobs) 

4.Random Allocation -- "PERMEATE"
the nodes allocated to each job will be randomly picked from a permeate-area, the size of with could be multiple of job size.


#######################################################################################
Three things need to be specified in the configuration file "config-alloc.conf"
1. Strategy Name i.e. "CONT", "CHUNK", "STRIPE", "PERMEATE"
2. total number of nodes in the network model
3. a list contains the number of ranks of each job


#######################################################################################
HOW TO RUN
please run the script like
$ python listgen.py config-alloc.conf
And it will put the allocation list for each job in a file with name "allocation.conf"
