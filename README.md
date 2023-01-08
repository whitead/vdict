# vdict

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ur-whitelab/vdict)
[![tests](https://github.com/ur-whitelab/vdict/actions/workflows/tests.yml/badge.svg)](https://github.com/ur-whitelab/vdict)
[![PyPI version](https://badge.fury.io/py/vdict.svg)](https://badge.fury.io/py/vdict)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

This a very thin wrapper around [hnswlib](https://github.com/nmslib/hnswlib) to make it look like a python dictionary whose keys are numpy arrays. Install with `pip install vdict`.

```python
from vdict import vdict
import numpy as np

data = vdict()
v1 = np.random.rand(32)
v2 = np.random.rand(32)
data[v1] = 'hello'
data[v2] = 32
assert data[v1] == 'hello'
```

You can have it throw IndexErrors if you try to access a key that doesn't exist:

```python
data = vdict(tol=0.001)
v1 = np.random.rand(32)
v2 = np.random.rand(32)
data[v1] = 'hello'
# this will throw an IndexError because we didn't add yet!
print(data[v2])
```


The default tolerance is `1` (generally do not throw errors), but you can set it to a smaller value to make it more strict.

## Details

* All vectors must be the same length
* Accessing with a vector gives the closest value keyed by the closest vector
* The algorithm is *approximate* nearest neighbor search. You can tune the accuracy (see below)
* You can have millions of vectors in the dictionary
* If you know the approximate size, pass `est_nelements` to `vidct()` to reduce how often things are resized

## Usage

The `vdict` class has some reasonable defaults, but you may need to tune for your use case. These are adjustable in the constructor. You can read about the parameters at the [hnswlib](https://github.com/nmslib/hnswlib). Briefly,
the most important ones are:

* `M` - the number of neighbors to consider when building the graph (higher `M` means more accurate, but more memory). 12-48 is typical.
* `space` - the distance metric to use. The default is `l2`, but you can also use `cosine` or `ip` (inner product).
* `ef_construction` - parameter that controls speed/accuracy trade-off during the index construction - 50 - 200 is typical.

```python
from vdict import vdict
data = vdict(M=16, space='cosine', ef_construction=100)

# add some vectors
data[np.random.rand(32)] = 'hello'
data[np.random.rand(32)] = 'world'
```

## License

MIT

## Author

Andrew White
