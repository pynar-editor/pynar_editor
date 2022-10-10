# built-in
from collections import Counter, defaultdict
from contextlib import suppress

from itertools import permutations, zip_longest
from difflib import SequenceMatcher as _SequenceMatcher

import math

try:
    import numpy
except ImportError:
    numpy = None

def find_ngrams(input_list, n):
    return list(zip(*[input_list[i:] for i in range(n)]))

class Base:
    def __init__(self, qval=1, external=True):
        self.qval = qval
        self.external = external

    def __call__(self, *sequences):
        raise NotImplementedError

    def maximum(*sequences):
        """Get maximum possible value
        """
        return max(map(len, sequences))

    def distance(self, *sequences):
        """Get distance between sequences
        """
        return self(*sequences)

    def similarity(self, *sequences):
        """Get sequences similarity.

        similarity = maximum - distance
        """
        return self.maximum(*sequences) - self.distance(*sequences)

    def normalized_distance(self, *sequences):
        """Get distance from 0 to 1
        """
        maximum = self.maximum(*sequences)
        if maximum == 0:
            return 0
        return self.distance(*sequences) / maximum

    def normalized_similarity(self, *sequences):
        """Get similarity from 0 to 1

        normalized_similarity = 1 - normalized_distance
        """
        return 1 - self.normalized_distance(*sequences)


    def external_answer(self, *sequences):
        """Try to get answer from known external libraries.
        """
        # if this feature disabled
        if not getattr(self, 'external', False):
            return
        # all external libs doesn't support test_func
        if hasattr(self, 'test_func') and self.test_func is not self._ident:
            return

    def quick_answer(self, *sequences):
        """Try to get answer quick without main implementation calling.

        If no sequences, 1 sequence or all sequences are equal then return 0.
        If any sequence are empty then return maximum.
        And in finish try to get external answer.
        """
        if not sequences:
            return 0
        if len(sequences) == 1:
            return 0
        if self._ident(*sequences):
            return 0
        if not all(sequences):
            return self.maximum(*sequences)
        # try get answer from external libs
        answer = self.external_answer(*sequences)
        if answer is not None:
            return answer

    @staticmethod
    def _ident(*elements):
        """Return True if all sequences are equal.
        """
        try:
            # for hashable elements
            return len(set(elements)) == 1
        except TypeError:
            # for unhashable elements
            for e1, e2 in zip(elements, elements[1:]):
                if e1 != e2:
                    return False
            return True

    def _get_sequences(self, *sequences):
        """Prepare sequences.

        qval=None: split text by words
        qval=1: do not split sequences. For text this is mean comparing by letters.
        qval>1: split sequences by q-grams
        """
        # by words
        if not self.qval:
            return [s.split() for s in sequences]
        # by chars
        if self.qval == 1:
            return sequences
        # by n-grams
        return [find_ngrams(s, self.qval) for s in sequences]

    def _get_counters(self, *sequences):
        """Prepare sequences and convert it to Counters.
        """
        # already Counters
        if all(isinstance(s, Counter) for s in sequences):
            return sequences
        return [Counter(s) for s in self._get_sequences(*sequences)]

    def _intersect_counters(self, *sequences):
        intersection = sequences[0].copy()
        for s in sequences[1:]:
            intersection &= s
        return intersection

    def _union_counters(self, *sequences):
        union = sequences[0].copy()
        for s in sequences[1:]:
            union |= s
        return union

    def _sum_counters(self, *sequences):
        result = sequences[0].copy()
        for s in sequences[1:]:
            result += s
        return result

    def _count_counters(self, counter):
        """Return all elements count from Counter
        """
        if getattr(self, 'as_set', False):
            return len(set(counter))
        else:
            return sum(counter.values())

    def __repr__(self):
        return '{name}({data})'.format(
            name=type(self).__name__,
            data=self.__dict__,
        )

class NCDBase(Base):
    """Normalized compression distance (NCD)

    https://articles.orsinium.dev/other/ncd/
    https://en.wikipedia.org/wiki/Normalized_compression_distance#Normalized_compression_distance
    """
    qval = 1

    def __init__(self, qval=1):
        self.qval = qval

    def maximum(self, *sequences):
        return 1

    def _get_size(self, data):
        return len(self._compress(data))

    def __call__(self, *sequences):
        if not sequences:
            return 0
        sequences = self._get_sequences(*sequences)

        concat_len = float('Inf')
        empty = type(sequences[0])()
        for data in permutations(sequences):
            if isinstance(empty, (str, bytes)):
                data = empty.join(data)
            else:
                data = sum(data, empty)
            concat_len = min(concat_len, self._get_size(data))

        compressed_lens = [self._get_size(s) for s in sequences]
        max_len = max(compressed_lens)
        if max_len == 0:
            return 0
        return (concat_len - min(compressed_lens) * (len(sequences) - 1)) / max_len

class BaseSimilarity(Base):
    def distance(self, *sequences):
        return self.maximum(*sequences) - self.similarity(*sequences)

    def similarity(self, *sequences):
        return self(*sequences)

    def quick_answer(self, *sequences):
        if not sequences:
            return self.maximum(*sequences)
        if len(sequences) == 1:
            return self.maximum(*sequences)
        if self._ident(*sequences):
            return self.maximum(*sequences)
        if not all(sequences):
            return 0
        # try get answer from external libs
        answer = self.external_answer(*sequences)
        if answer is not None:
            return answer

class StrCmp95(BaseSimilarity):
    """strcmp95 similarity

    http://cpansearch.perl.org/src/SCW/Text-JaroWinkler-0.1/strcmp95.c
    """
    sp_mx = (
        ('A', 'E'), ('A', 'I'), ('A', 'O'), ('A', 'U'), ('B', 'V'), ('E', 'I'),
        ('E', 'O'), ('E', 'U'), ('I', 'O'), ('I', 'U'), ('O', 'U'), ('I', 'Y'),
        ('E', 'Y'), ('C', 'G'), ('E', 'F'), ('W', 'U'), ('W', 'V'), ('X', 'K'),
        ('S', 'Z'), ('X', 'S'), ('Q', 'C'), ('U', 'V'), ('M', 'N'), ('L', 'I'),
        ('Q', 'O'), ('P', 'R'), ('I', 'J'), ('2', 'Z'), ('5', 'S'), ('8', 'B'),
        ('1', 'I'), ('1', 'L'), ('0', 'O'), ('0', 'Q'), ('C', 'K'), ('G', 'J'),
    )

    def __init__(self, long_strings=False, external=True):
        self.long_strings = long_strings
        self.external = external

    def maximum(self, *sequences):
        return 1

    @staticmethod
    def _in_range(char):
        return 0 < ord(char) < 91

    def __call__(self, s1, s2):
        s1 = s1.strip().upper()
        s2 = s2.strip().upper()

        result = self.quick_answer(s1, s2)
        if result is not None:
            return result

        len_s1 = len(s1)
        len_s2 = len(s2)

        adjwt = defaultdict(int)

        # Initialize the adjwt array on the first call to the function only.
        # The adjwt array is used to give partial credit for characters that
        # may be errors due to known phonetic or character recognition errors.
        # A typical example is to match the letter "O" with the number "0"
        for c1, c2 in self.sp_mx:
            adjwt[c1, c2] = 3
            adjwt[c2, c1] = 3

        if len_s1 > len_s2:
            search_range = len_s1
            minv = len_s2
        else:
            search_range = len_s2
            minv = len_s1

        # Blank out the flags
        s1_flag = [0] * search_range
        s2_flag = [0] * search_range
        search_range = max(0, search_range // 2 - 1)

        # Looking only within the search range, count and flag the matched pairs.
        num_com = 0
        yl1 = len_s2 - 1
        for i, sc1 in enumerate(s1):
            lowlim = max(i - search_range, 0)
            hilim = min(i + search_range, yl1)
            for j in range(lowlim, hilim + 1):
                if s2_flag[j] == 0 and s2[j] == sc1:
                    s2_flag[j] = 1
                    s1_flag[i] = 1
                    num_com += 1
                    break

        # If no characters in common - return
        if num_com == 0:
            return 0.0

        # Count the number of transpositions
        k = n_trans = 0
        for i, sc1 in enumerate(s1):
            if not s1_flag[i]:
                continue
            for j in range(k, len_s2):
                if s2_flag[j] != 0:
                    k = j + 1
                    break
            if sc1 != s2[j]:
                n_trans += 1
        n_trans = n_trans // 2

        # Adjust for similarities in unmatched characters
        n_simi = 0
        if minv > num_com:
            for i in range(len_s1):
                if s1_flag[i] != 0:
                    continue
                if not self._in_range(s1[i]):
                    continue
                for j in range(len_s2):
                    if s2_flag[j] != 0:
                        continue
                    if not self._in_range(s2[j]):
                        continue
                    if (s1[i], s2[j]) not in adjwt:
                        continue
                    n_simi += adjwt[s1[i], s2[j]]
                    s2_flag[j] = 2
                    break
        num_sim = n_simi / 10.0 + num_com

        # Main weight computation
        weight = num_sim / len_s1 + num_sim / len_s2
        weight += (num_com - n_trans) / num_com
        weight = weight / 3.0

        # Continue to boost the weight if the strings are similar
        if weight <= 0.7:
            return weight

        # Adjust for having up to the first 4 characters in common
        j = min(minv, 4)
        i = 0
        for sc1, sc2 in zip(s1, s2):
            if i >= j:
                break
            if sc1 != sc2:
                break
            if sc1.isdigit():
                break
            i += 1
        if i:
            weight += i * 0.1 * (1.0 - weight)

        # Optionally adjust for long strings.

        # After agreeing beginning chars, at least two more must agree and
        # the agreeing characters must be > .5 of remaining characters.
        if not self.long_strings:
            return weight
        if minv <= 4:
            return weight
        if num_com <= i + 1 or 2 * num_com < minv + i:
            return weight
        if s1[0].isdigit():
            return weight
        res = (num_com - i - 1) / (len_s1 + len_s2 - i * 2 + 2)
        weight += (1.0 - weight) * res
        return weight

class Jaccard(BaseSimilarity):
    """
    Compute the Jaccard similarity between the two sequences.
    They should contain hashable items.
    The return value is a float between 0 and 1, where 1 means equal,
    and 0 totally different.

    https://en.wikipedia.org/wiki/Jaccard_index
    https://github.com/Yomguithereal/talisman/blob/master/src/metrics/distance/jaccard.js
    """
    def __init__(self, qval=1, as_set=False, external=True):
        self.qval = qval
        self.as_set = as_set
        self.external = external

    def maximum(self, *sequences):
        return 1

    def __call__(self, *sequences):
        result = self.quick_answer(*sequences)
        if result is not None:
            return result

        sequences = self._get_counters(*sequences)               # sets
        intersection = self._intersect_counters(*sequences)      # set
        intersection = self._count_counters(intersection)        # int
        union = self._union_counters(*sequences)                 # set
        union = self._count_counters(union)                      # int
        return intersection / union

class LCSStr(BaseSimilarity):
    """longest common substring similarity
    """
    def _standart(self, s1, s2):
        matcher = _SequenceMatcher(a=s1, b=s2)
        match = matcher.find_longest_match(0, len(s1), 0, len(s2))
        return s1[match.a: match.a + match.size]

    def _custom(self, *sequences):
        short = min(sequences, key=len)
        length = len(short)
        for n in range(length, 0, -1):
            for subseq in find_ngrams(short, n):
                subseq = ''.join(subseq)
                for seq in sequences:
                    if subseq not in seq:
                        break
                else:
                    return subseq
        return type(short)()  # empty sequence

    def __call__(self, *sequences):
        if not all(sequences):
            return ''
        length = len(sequences)
        if length == 0:
            return ''
        if length == 1:
            return sequences[0]

        sequences = self._get_sequences(*sequences)
        if length == 2 and max(map(len, sequences)) < 200:
            return self._standart(*sequences)
        return self._custom(*sequences)

    def similarity(self, *sequences):
        return len(self(*sequences))

class RatcliffObershelp(BaseSimilarity):
    """Ratcliff-Obershelp similarity
    This follows the Ratcliff-Obershelp algorithm to derive a similarity
    measure:
        1. Find the length of the longest common substring in sequences.
        2. Recurse on the strings to the left & right of each this substring
           in sequences. The base case is a 0 length common substring, in which
           case, return 0. Otherwise, return the sum of the current longest
           common substring and the left & right recursed sums.
        3. Multiply this length by 2 and divide by the sum of the lengths of
           sequences.

    https://en.wikipedia.org/wiki/Gestalt_Pattern_Matching
    https://github.com/Yomguithereal/talisman/blob/master/src/metrics/distance/ratcliff-obershelp.js
    https://xlinux.nist.gov/dads/HTML/ratcliffObershelp.html
    """

    def maximum(self, *sequences):
        return 1

    def _find(self, *sequences):
        subseq = LCSStr()(*sequences)
        length = len(subseq)
        if length == 0:
            return 0
        before = [s[:s.find(subseq)] for s in sequences]
        after = [s[s.find(subseq) + length:] for s in sequences]
        return self._find(*before) + length + self._find(*after)

    def __call__(self, *sequences):
        result = self.quick_answer(*sequences)
        if result is not None:
            return result
        scount = len(sequences)  # sequences count
        ecount = sum(map(len, sequences))  # elements count
        sequences = self._get_sequences(*sequences)
        return scount * self._find(*sequences) / ecount

class SqrtNCD(NCDBase):
    """Square Root based NCD

    Size of compressed data equals to sum of square roots of counts of every
    element in the input sequence.
    """
    def __init__(self, qval=1):
        self.qval = qval

    def _compress(self, data):
        return {element: math.sqrt(count) for element, count in Counter(data).items()}

    def _get_size(self, data):
        return sum(self._compress(data).values())

strcmp95 = StrCmp95()
jaccard = Jaccard()
ratcliff_obershelp = RatcliffObershelp()
sqrt_ncd = SqrtNCD()
