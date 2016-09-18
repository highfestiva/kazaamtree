# kazaamtree.py

A tiny but fast 2D space partition tree. Coordinates are inserted one by one, and an
approximation set can be fetched by AABB.

Insertion is O(log(N)) and inserting a single coordinate takes ~15 microseconds on
average on my computer when inserting one million coordinates. The approximate AABB
fetch of all 1M coordinates into a list take ~0.85 seconds. The Python process
consumes 240 MB of RAM when keeping a 1M tree in-memory.

This is how you'd use it on geographic coordinates:

```python
#!/usr/bin/env python3

from kazaamtree.coord import latlng
from kazaamtree import kazaamindextree
from random import random

tree = kazaamindextree()
for _ in range(10000):
    tree.add(latlng(57.8+random(), 12.4+random()))

for i,bucket in enumerate(tree.buckets()):
    print('Bucket %i contains %i coordinates with center at (%s).' % (i, len(bucket), str(bucket.center(crdtype=latlng))))
```

The kazaamtree automatically gets spatially partitioned into buckets. More than most
binary tree algorithms, the spatial balancing benefits from adding random coordinates
as opposed to ordered ones.

If you instead of geographic coordinates (as in the example above) want to use
cartesian, you simply replace the text `latlng` with `coord`.
