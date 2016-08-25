# kazaamtree.py

A tiny but fast 2D space partition tree. Coordinates are inserted one by one, and an
approximation set can be fetched by AABB.

Inserting a single coordinate takes ~15 microseconds on average on my computer when
inserting one million coordinates. The approximate AABB fetch of all 1M coordinates
into a list take ~0.85 seconds. The Python process consumes 240 MB of RAM when
keeping a 1M tree in-memory.
