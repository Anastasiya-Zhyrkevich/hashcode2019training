from copy import deepcopy as copy


n, m = None, None
l, r = None, None
pizza = []


PATH = 'a_example.in'

def read_file(path):
    global n, m, l, r, pizza
    with open(path) as f:
        lines = f.readlines()
        line = lines[0]
        line = [int(x) for x in line.split()]
        n, m, l, r = line[0], line[1], line[2], line[3]

        pizza = lines[1:]
        for i in xrange(n):
            pizza[i] = pizza[i].strip()


class Solution(object):

    def __init__(self, reward, slices):
        self.reward = reward
        self.slices = slices

    def print_out(self, filename):
        with open(filename, 'w') as f:
            f.write("%d\n" % len(self.slices))
            for sl in self.slices:
                for c in sl:
                    f.write("%d " % (c - 1))
                f.write("\n")

    def __lt__(self, other):
        return (- self.reward + other.reward)

    def __gt__(self, other):
        return (self.reward - other.reward)

    def add(self, r, sl):
        self.reward += r
        self.slices.extend(sl)

    def add_slices(self, sl):
        for s in sl:
            self.reward += slice_size(*s)

        self.slices.extend(sl)

    def __str__(self):
        return "S: %d, %s" % (self.reward, self.slices)

    def __repr__(self):
        return "S: %d, %s" % (self.reward, self.slices)

read_file(PATH)

def get_dp(pizza, n, m):
    dp = {'T': [[0] * (m + 1) for _ in xrange(n + 1)],
    'M' : [[0] * (m + 1) for _ in xrange(n + 1)]}

    for i in xrange(0, n):
        for j in xrange(0, m):
            for k in dp.keys():
                dp[k][i + 1][j + 1] = dp[k][i][j + 1] + dp[k][i + 1][j] - dp[k][i][j]

            dp[pizza[i][j]][i + 1][j + 1] += 1
    print dp
    return dp

def is_slice(dp, i1, i2, j1, j2):
    # print "is_slice %d %d %d %d" % (i1, i2, j1, j2)
    global n, m
    global l, r

    assert (1 <= i1 <= n)
    assert (1 <= i2 <= n)
    assert (1 <= j1 <= m)
    assert (1 <= j2 <= m)
    assert (i1 <= i2)
    assert (j1 <= j2)

    for k in dp.keys():
        assert len(dp[k]) == n + 1
        assert len(dp[k][0]) ==  m + 1

        cnt = get_ingr_cnt(dp[k], i1, i2, j1, j2)
        if cnt < l or cnt > r:
            return False
    return True

def slice_size(i1, i2, j1, j2):
    return (j2 - j1 + 1) * (i2 - i1 + 1)

def get_ingr_cnt(dp, i1, i2, j1, j2):
    # print "get ingr cnt ", i1, i2, j1, j2
    return dp[i2][j2] - dp[i1 - 1][j2] - dp[i2][j1 - 1] + dp[i1 - 1][j1 - 1]

def v_stripe_dp(dp, i1, i2, j1, j2):
    # print "v_stripe_dp %d %d %d %d" % (i1, i2, j1, j2)
    assert(j2 - j1 <= 1)

    bs = [Solution(0, [])] * (i2 + 1)
    for i in xrange(i1, i2 + 1):
        bs[i] = copy(bs[i - 1])

        for ii in xrange(i, i1 - 1, -1):
            if is_slice(dp, ii, i, j1, j2):

                pot_sl = copy(bs[ii - 1])
                pot_sl.add_slices([(ii, i, j1, j2)])

                if pot_sl.reward > bs[i].reward:
                    bs[i] = pot_sl

    # print "v_stripe_dp %d %d %d %d" % (i1, i2, j1, j2)
    # print bs
    return bs[i2]


def vertical_dp(pizza):
    global n,m,l,r

    dp = get_dp(pizza, n, m)

    best_solution = [Solution(0, [])] * (m + 1)

    for j in xrange(1, m + 1):
        best_solution[j] = copy(best_solution[j - 1])
        print "j ", j
        for d in xrange(1, min(j, 2) + 1):

            pot_sol = copy(best_solution[j - d])
            pot_sol.add_slices(v_stripe_dp(dp, 1, n, j - d + 1, j).slices)

            if pot_sol.reward > best_solution[j].reward:
                best_solution[j] = pot_sol

        print best_solution[j]

    print best_solution
    return best_solution[m]



t1 = vertical_dp(pizza)
t1.print_out('a.out')


# dp = get_dp(pizza, n, m)
# v_stripe_dp(dp, 1, 3, 2, 2)
