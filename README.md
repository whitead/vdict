# vdict

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ur-whitelab/vdict)
[![tests](https://github.com/ur-whitelab/vdict/actions/workflows/tests.yml/badge.svg)](https://github.com/ur-whitelab/vdict)
[![PyPI version](https://badge.fury.io/py/vdict.svg)](https://badge.fury.io/py/vdict)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

This a very thin wrapper around [hnswlib](https://github.com/nmslib/hnswlib) to make it look like a python dictionary whose keys are numpy arrays.

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

Note that the vectors all need to be the same length.

## Installation

```bash
pip install vdict
```

## Usage

The `vdict` class has some reasonable defaults, but you may need to tune for your use case. These are adjustable in the constructor. You can read about the parameters at the [hnswlib](https://github.com/nmslib/hnswlib). Briefly,
the most important ones are:

* `M` - the number of neighbors to consider when building the graph (higher `M` means more accurate, but more memory). 12-48 is typical.
* `space` - the distance metric to use. The default is `l2`, but you can also use `cosine` or `ip` (inner product).
* `ef_construction` - parameter that controls speed/accuracy trade-off during the index construction - 50 - 200 is typical.

```python
from vdict import vdict
data = vdict(M=16, space='cosine', ef_construction=100)
```

## License

MIT

## Author

Andrew White
