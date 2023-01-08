import hnswlib
from numpy import ndarray
from typing import *
import numpy as np


class vdict(list):
    """A dict with a vector index for fast lookup of nearest neighbors"""

    def __init__(
        self,
        space: str = "l2",
        M: int = 16,
        est_nelements: int = 200,
        ef_construction: int = 200,
        tol: float = 1,
    ) -> None:
        super().__init__()
        # implementation is map from vector to index, index looks-up in list to value
        # defer construction until we know shape of vectors
        self._ready = False
        self._space = space
        self._M = M
        self._est_nelements = est_nelements
        self._ef_construction = ef_construction
        self._deleted = 0
        self._tol = tol

    def _setup(self, key: ndarray) -> None:
        self._dim = key.shape[-1]
        self.index = hnswlib.Index(space=self._space, dim=self._dim)
        self.index.init_index(
            max_elements=self._est_nelements,
            ef_construction=self._ef_construction,
            M=self._M,
        )
        self._ready = True

    def __getitem__(self, key: ndarray) -> Any:
        if not self._ready:
            raise IndexError("vdict is empty")
        if type(key) is not ndarray and type(key) is list:
            key = np.array(key)
        # check dimensionality
        if key.shape[-1] != self._dim:
            raise ValueError("vector has wrong dimensionality")
        index, distance = self.index.knn_query(key, k=1)
        if distance[0][0] > self._tol:
            raise IndexError("no match found")
        return super().__getitem__(index[0][0])

    def __setitem__(self, key: ndarray, value: Any) -> None:
        if type(key) is not ndarray and type(key) is list:
            key = np.array(key)
        if not self._ready:
            self._setup(key)
        # check dimensionality
        if key.shape[-1] != self._dim:
            raise ValueError("vector has wrong dimensionality")
        super().append(value)
        # optionally increase index size
        if len(self) > self.index.get_current_count():
            self.index.resize_index(len(self) * 2)
        self.index.add_items(key, len(self) - 1)

    def __delitem__(self, key: ndarray) -> None:
        if type(key) is not ndarray and type(key) is list:
            key = np.array(key)
        index = self.index.knn_query(key, k=1)[0][0]
        self.index.mark_deleted(index)
        self._deleted += 1

    def __iter__(self) -> Iterator[Tuple[ndarray, Any]]:
        for i in range(len(self)):
            yield self.index.get_items([i])[0], super().__getitem__(i)

    def __len__(self) -> int:
        return super().__len__() - self._deleted
