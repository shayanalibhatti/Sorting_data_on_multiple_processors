# Sorting data on multiple processors
In this Python repository, I sorted data using multiple processors via MPI4PY library. Multi processor processing is very important for parallel processing. In this project, we sort data using the available processors and sort the data using parallel processing. Following is the task description:

### Task description
Write a sorting program which works in parallel with collective communication using mpi4py for an arbitrary number of processes. The root process should generate a large unsorted data set (e.g. 10,000 elements), then slice it into bins by value and send each bin (except one) to the other processes to sort. You can utilize any appropriate method to sort the data. The sorted data should then be sent back to the root process and put into rank order. The data should now be completely sorted.

As an example, consider sorting this data set on four processors:
3 5 7 4 6 7 11 9 2 8 3 2
The first (root) process looks at the range of these data and divides it into four groups, one for each process rank. So process with rank 0 will be sent data in the range 0–2, process 1 will be sent data in the range 3–5, process 2 will be sent data in the range 6–8, and process 3 will be sent data in the range 9–11:

Thus process rank 0 receives two data points, [2, 2], while process rank 2 receives four, [7, 6, 7, 8], etc. (A better algorithm will balance the load better but that’s not your concern right now.) When each process has sorted its own data points, then reunifying them on root will produce a completely sorted data set.

### Code explanation
First we install mpi4py in command prompt:
```
mpi4py using pip install mpi4py
```

Following is the explanation of the code:
First we import the mpi4py library as MPI, then we also import math library
```
from mpi4py import MPI
import math
```

We create an intraprocess communicator as:
```
comm = MPI.COMM_WORLD
```

Get the number of maximum processors available from the communicator
```
max_processors = comm.size
```

This is the data that we want to sort using parallel processing
```
data = [3,5,7,4,6,7,11,9,2,8,3,2]
```

We create a bin size based on the task
```
# Bin size
bin_size = math.floor(int((max(data)-min(data))/comm.size))
```

Here we make lists of data based on the bins defined in the task description above
```
# Store appropriate numbers in their bins
for rank in range(max_processors):
    new_list.append([x for x in data if (x >= bin_size*rank+rank) and x<=(bin_size+bin_size*rank+rank)])
```    

We scatter each of the list to each processor
```
# Scatter the lists among the max # of processors
v = comm.scatter(new_list,root)
```

Here we sort each list that the processor has
```
# Sort each of the lists that each processor gets
v = sorted(v)
```

Finally we gather the sorted lists that each processor has into one object 'g' and print it
```
# Gather all the sorted lists
g = comm.gather(v,root)
if comm.rank==0:
    for i in range(len(g)):
        print("Rank:",i," ",g[i])
```
