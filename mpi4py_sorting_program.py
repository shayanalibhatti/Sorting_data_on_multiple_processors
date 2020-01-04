from mpi4py import MPI
import math
root = 0
# Get all processors
comm = MPI.COMM_WORLD
# Get # of maximum processors available
max_processors = comm.size
data = [3,5,7,4,6,7,11,9,2,8,3,2]
new_list = []
# Bin size
bin_size = math.floor(int((max(data)-min(data))/comm.size))
# Store appropriate numbers in their bins
for rank in range(max_processors):
    new_list.append([x for x in data if (x >= bin_size*rank+rank) and x<=(bin_size+bin_size*rank+rank)])
# Scatter the lists among the max # of processors
v = comm.scatter(new_list,root)
print("Rank is ",comm.rank, " data is ", v)
# Sort each of the lists that each processor gets
v = sorted(v)
# Gather all the sorted lists
g = comm.gather(v,root)
if comm.rank==0:
    for i in range(len(g)):
        print("Rank:",i," ",g[i])

