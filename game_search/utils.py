import re


def tokenize_string(s):
    # Stemming can be applied here.
    return re.sub("[^\w]", " ", s.lower()).split()


def longest_contiguous_subarray(arr):
    # Initialize result
    max_len = 1
    n = len(arr)
    for i in range(n - 1):

        # Initialize min and max for
        # all subarrays starting with i
        mn = arr[i]
        mx = arr[i]

        # Consider all subarrays starting
        # with i and ending with j
        for j in range(i + 1, n):

            # Update min and max in
            # this subarray if needed
            mn = min(mn, arr[j])
            mx = max(mx, arr[j])

            # If current subarray has
            # all contiguous elements
            if ((mx - mn) == j - i):
                max_len = max(max_len, mx - mn + 1)

    return max_len


class EncoderGeneratedList(list):
    '''
    Fast hack.
    '''

    def __init__(self, generator):
        self.generator = generator
        super(EncoderGeneratedList, self).__init__()

    def __iter__(self):
        return self.generator

    def __len__(self):
        return 1
