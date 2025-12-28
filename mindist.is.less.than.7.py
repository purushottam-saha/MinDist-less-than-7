#####################################################
#               MinDist is less than 7              #
#####################################################
# The code below generates 3-3-3-2 partitions 
# (with a gap, which is considered as the 
# double cards obtained) from 1-12, and computes 
# the gaps between those partitions, 
# i.e. the same suit cards.
# As we obtain no partition with minimum distances 
# with first atleast 4 and second one atleast 5 
# (4,4 will allow for a MinDist of 7), then
# the claim is shown. 
# Please refer to the paper "MinDist is atmost 7".


import itertools
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

def stream_3332_partitions(elements):
    elements = set(elements)

    for dbl_element in tqdm(itertools.combinations(elements,1)):
        dbl_element = frozenset(dbl_element)
        remaining = elements - dbl_element
        for block2 in itertools.combinations(remaining, 2):
            block2 = frozenset(block2)
            remaining1 = remaining - block2
            for block3a in itertools.combinations(remaining1, 3):
                block3a = frozenset(block3a)
                remaining2 = remaining1 - block3a
                for block3b in itertools.combinations(remaining2, 3):
                    block3b = frozenset(block3b)
                    block3c = frozenset(remaining2 - block3b)
                    yield tuple(sorted([block2,block3a,block3b,block3c]))
                    
def distances(meld):
    meld = sorted(list(meld))
    if len(meld)==2:
        return [meld[1]-meld[0],]
    if len(meld)==3:
        return [meld[2]-meld[1], meld[1]-meld[0]]
    
def evaluate_partition(partition):
    dists = []
    for meld in partition:
        dists = dists + distances(meld)
    dists = sorted(dists)
    if dists[0] >= 4: # if one 3 is allowed, then already MinDist < 7
        if (dists[1] >= 5) or (dists[2] >= 5): 
            # if two 4 are allowed, then also MinDist < 7
            return dists[:3], partition
    return None

if __name__=="__main__":
    elements = range(12)
    num_cores = cpu_count()
    valid_partitions = []
    with Pool(processes=num_cores) as pool:
        for result in pool.imap_unordered(evaluate_partition, stream_3332_partitions(elements), chunksize= 50):
            if result is not None:
                print(result)