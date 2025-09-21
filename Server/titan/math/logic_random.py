"""
Python conversion of Supercell.Laser.Titan.Math.LogicRandom.cs
Random number generator for game logic
"""

class LogicRandom:
    """Random number generator for consistent game logic"""

    def __init__(self, seed: int = 0):
        """Initialize with seed"""
        self.seed = seed

    def get_iterated_random_seed(self) -> int:
        """Get current seed"""
        return self.seed

    def set_iterated_random_seed(self, value: int) -> None:
        """Set current seed"""
        self.seed = value & 0xFFFFFFFF

    def rand(self, max_value: int) -> int:
        """Generate random number 0 to max_value-1"""
        if max_value > 0:
            self.seed = self.iterate_random_seed()
            tmp_val = self.seed

            if tmp_val < 0:
                tmp_val = -tmp_val

            return tmp_val % max_value

        return 0

    def iterate_random_seed(self) -> int:
        """Iterate the random seed"""
        seed = self.seed

        if seed == 0:
            seed = -1

        # XOR shift algorithm
        tmp = seed ^ (seed << 13)
        tmp = tmp ^ (tmp >> 17)
        tmp = tmp ^ (tmp << 5)

        self.seed = tmp & 0xFFFFFFFF
        return self.seed

    def rand_float(self) -> float:
        """Generate random float 0.0 to 1.0"""
        return self.rand(0x7FFFFFFF) / float(0x7FFFFFFF)

    def rand_between(self, min_val: int, max_val: int) -> int:
        """Generate random number between min and max (inclusive)"""
        if min_val >= max_val:
            return min_val
        return min_val + self.rand(max_val - min_val + 1)

    def rand_boolean(self) -> bool:
        """Generate random boolean"""
        return self.rand(2) == 1

    def shuffle_array(self, array: list) -> None:
        """Shuffle array in place"""
        for i in range(len(array) - 1, 0, -1):
            j = self.rand(i + 1)
            array[i], array[j] = array[j], array[i]

    def encode(self, stream) -> None:
        """Encode to stream"""
        stream.write_v_int(self.seed)

    def decode(self, stream) -> None:
        """Decode from stream"""
        self.seed = stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return f"LogicRandom(seed={self.seed})"
