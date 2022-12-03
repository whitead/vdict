import hnswlib
from numpy import ndarray
from typing import *


class vdict(list):
    """A dict with a vector index for fast lookup of nearest neighbors"""

    def __init__(
        self,
        space: str = "l2",
        M: int = 16,
        est_nelements: int = 200,
        ef_construction: int = 200,
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
        # check dimensionality
        if key.shape[-1] != self._dim:
            raise ValueError("vector has wrong dimensionality")
        index = self.index.knn_query(key, k=1)[0][0][0]
        return super().__getitem__(index)

    def __setitem__(self, key: ndarray, value: Any) -> None:
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
        index = self.index.knn_query(key, k=1)[0][0]
        self.index.mark_deleted(index)
        self._deleted += 1

    def __iter__(self) -> Iterator[Tuple[ndarray, Any]]:
        for i in range(len(self)):
            yield self.index.get_items([i])[0], super().__getitem__(i)

    def __len__(self) -> int:
        return super().__len__() - self._deleted
