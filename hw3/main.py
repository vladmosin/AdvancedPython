import numpy as np


class MatrixEasy:
    def __init__(self, matrix):
        self.matrix = matrix

    def __add__(self, other):
        return MatrixEasy(self.matrix + other.matrix)

    def __mul__(self, other):
        return MatrixEasy(self.matrix * other.matrix)

    def __matmul__(self, other):
        return self.matrix @ other.matrix

    def save(self, path):
        np.savetxt(path, self.matrix)


class ToString:
    def __str__(self):
        return str(self.matrix)


class ToFile:
    def save(self, path):
        np.savetxt(path, self.matrix)


class Access:
    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, matrix):
        self.matrix = matrix


class MatrixMedium(np.lib.mixins.NDArrayOperatorsMixin, ToString, Access, ToFile):
    def __init__(self, matrix):
        self._matrix = matrix

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        inputs = tuple(x.matrix for x in inputs)
        result = getattr(ufunc, method)(*inputs, **kwargs)
        return MatrixMedium(result)


"""
Hash - product of all matrix element modulo 29
"""
class Hasher:
    def __hash__(self):
        return int(np.prod(self.matrix)) % 29


class MatrixHard(MatrixEasy, Hasher):
    map_ = {}

    def __matmul__(self, other):
        min_hash = min(hash(self), hash(other))
        max_hash = max(hash(self), hash(other))

        if min_hash in MatrixHard.map_ and max_hash in MatrixHard.map_[min_hash]:
            return MatrixHard.map_[min_hash][max_hash]

        if min_hash not in MatrixHard.map_:
            MatrixHard.map_[min_hash] = {}

        MatrixHard.map_[min_hash][max_hash] = MatrixHard(self.matrix @ other.matrix)

        return MatrixHard.map_[min_hash][max_hash]


def run_easy():
    np.random.seed(0)
    a = MatrixEasy(np.random.randint(0, 10, (10, 10)))
    b = MatrixEasy(np.random.randint(0, 10, (10, 10)))

    (a + b).save('artifacts/easy/matrix+.txt')
    (a * b).save('artifacts/easy/matrix*.txt')
    (a @ b).save('artifacts/easy/matrix@.txt')


def run_medium():
    np.random.seed(0)
    a = MatrixMedium(np.random.randint(0, 10, (10, 10)))
    b = MatrixMedium(np.random.randint(0, 10, (10, 10)))

    (a + b).save('artifacts/medium/matrix+.txt')
    (a * b).save('artifacts/medium/matrix*.txt')
    (a @ b).save('artifacts/medium/matrix@.txt')


def run_hard():
    a = MatrixHard(np.array([
        [1, 0],
        [1, 1]
    ]))

    b = MatrixHard(np.array([
        [1, 1],
        [1, 1]
    ]))

    c = MatrixHard(np.array([
        [1, 2],
        [0, 1]
    ]))

    a.save('artifacts/hard/A.txt')
    b.save('artifacts/hard/B.txt')
    c.save('artifacts/hard/C.txt')
    b.save('artifacts/hard/D.txt')

    (a @ b).save('artifacts/hard/AB.txt')
    MatrixHard(c.matrix @ b.matrix).save('artifacts/hard/CD.txt')

    with open('artifacts/hard/hash.txt', 'w') as f:
        f.write(f'{hash(a @ b)}\n')
        f.write(f'{hash(MatrixHard(c.matrix @ b.matrix))}')


if __name__ == '__main__':
    run_hard()
