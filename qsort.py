import pdb
import random


class Qsort:
    @staticmethod
    def sort(nums):
        if len(nums) <= 1:
            return nums
        else:
            q = random.choice(nums)
            s_nums = []
            m_nums = []
            e_nums = []
            pdb.set_trace()
            for n in nums:
                if n < q:
                    s_nums.append(n)
                elif n > q:
                    m_nums.append(n)
                else:
                    e_nums.append(n)
                print('q: {}\ns: {}\nm: {}\ne: {}'.format(q, s_nums, m_nums, e_nums))
            return Qsort.sort(s_nums) + e_nums + Qsort.sort(m_nums)
