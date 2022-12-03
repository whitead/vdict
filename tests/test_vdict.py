from vdict import vdict
import numpy as np


def test_construct_vdict():
    v = vdict()
    assert isinstance(v, vdict)
    v = vdict(space="cosine", M=16)
    assert isinstance(v, vdict)


def test_getitem_vdict():
    vectors = {1: np.random.rand(100), 2: np.random.rand(100)}
    vd = vdict()
    for k, v in vectors.items():
        vd[v] = k
    assert vd[vectors[1]] == 1
    assert vd[vectors[2]] == 2

    # try with a new vector
    new_vectors = {"a": np.random.rand(100), "b": np.random.rand(100)}
    for key, value in new_vectors.items():
        vd[value] = key
        assert vd[value] == key


def test_delete_vdict():
    vectors = {1: np.random.rand(100), 2: np.random.rand(100)}
    vd = vdict()
    for k, v in vectors.items():
        vd[v] = k
    assert len(vd) == 2
    del vd[vectors[1]]
    assert vd[vectors[1]] == 2
    assert vd[vectors[2]] == 2
    assert len(vd) == 1


def test_dim_error():
    vectors = {1: np.random.rand(100), 2: np.random.rand(100)}
    vd = vdict()
    for k, v in vectors.items():
        vd[v] = k
    # try to add a vector with the wrong dimensionality
    wrong_dim = np.random.rand(10)
    try:
        vd[wrong_dim] = 3
    except ValueError:
        pass
    else:
        raise AssertionError("vdict should have raised an error")


def test_growing_size_vdict():
    v = vdict(est_nelements=5)
    for _ in range(1000):
        v[np.random.rand(100)] = 1


def test_iter_vdict():
    vectors = {1: np.random.rand(100), 2: np.random.rand(100)}
    vd = vdict()
    for k, v in vectors.items():
        vd[v] = k
    for k, v in vd:
        assert v in vectors.keys()
        assert np.allclose(k, vectors[v])
