from math import log2


def entropy(n_bytes, alphabet):
    return n_bytes * log2(alphabet)


if __name__ == "__main__":
    n_bytes_az = 0
    entropy_az = 0
    alphabet_az = 26
    n_bytes_256 = 32
    alphabet_256 = 256
    entropy_256 = entropy(n_bytes_256, alphabet_256)
    while entropy_az < entropy_256:
        n_bytes_az += 1
        entropy_az = entropy(n_bytes_az, alphabet_az)
    print(f"Entropy for 256 bits is {entropy_256} for {n_bytes_256} bytes")
    print(f"Entropy for a-z is {entropy_az} for {n_bytes_az} chars")
