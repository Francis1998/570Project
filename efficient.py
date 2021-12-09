import os
import sys
import time
import tracemalloc

import psutil
# from basic import BasicSolution

class EfficientSolution:
    def __init__(self):
        self.alphas = {"AA": 0, "CC": 0, "GG": 0, "TT": 0,
                       "AC": 110, "CA": 110, "AG": 48, "GA": 48,
                       "AT": 94, "TA": 94, "CG": 118, "GC": 118,
                       "GT": 110, "TG": 110, "CT": 48, "TC": 48}
        self.delta = 30
        self.Path = []
        self.result = []
        # self.a_string = ""
        # self.b_string = ""

    def generate_result(self, path):
        f = open(path, "r")  # eg: "./image/abc.txt"
        file_list = f.readlines()
        # file_len = len(file_list)
        a_base = [item for item in file_list[0].strip("\n")]
        i = 1
        while file_list[i].strip("\n").isdigit():
            index = int(file_list[i].strip("\n"))
            a_base = a_base[:index + 1] + a_base + a_base[index + 1:]
            # print("".join(a_base))
            i += 1
            # print(a_base)
        b_base = [item for item in file_list[i].strip("\n")]
        i += 1
        while i < len(file_list) and file_list[i].strip("\n").isdigit():
            index = int(file_list[i].strip("\n"))
            b_base = b_base[:index + 1] + b_base + b_base[index + 1:]
            i += 1
        # print(file_list)
        f.close()
        # print("".join(a_base[:50]), " ", "".join(a_base[len(a_base) - 50:]))
        # print("".join(b_base[:50]), " ", "".join(b_base[len(b_base) - 50:]))
        self.a_string, self.b_string = "".join(a_base), "".join(b_base)
        # print(self.a_string, len(self.a_string))
        # print(self.b_string, len(self.b_string))
        # print(self.a_string == "ACACTGACTACTGACTGGTGACTACTGACTGG")
        # print(self.b_string == "TATTATACGCTATTATACGCGACGCGGACGCG")
        # print("backward_space_efficient_alignment: ", self.backward_space_efficient_alignment(self.a_string, self.b_string))
        # print("space_efficient_alignment: ", self.space_efficient_alignment(self.a_string, self.b_string))
        return self.divide_and_conquer_alignment(self.a_string, self.b_string)
        # print("divide_and_conquer_alignment: ", cost, "".join(string_a), "".join(string_b))

        # self.calculate_dp_cost(self.b_string, self.a_string)
    def space_efficient_alignment(self, X, Y):# get from 0,0, to i,j
        m, n = len(X), len(Y)
        B = [[0] * 2 for _ in range(m + 1)]
        for i in range(m + 1):
            B[i][0] = i * self.delta
        for j in range(1, n + 1):
            B[0][1] = j * self.delta
            for i in range(1, m + 1):
                B[i][1] = min(
                        self.alphas[X[i - 1] + Y[j - 1]] + B[i - 1][0],
                        self.delta + B[i - 1][1], self.delta + B[i][0])
            for i in range(0, m + 1):
                B[i][0] = B[i][1]
        # print(B[m][0])
        return B
        # return B[m][0]
    def backward_space_efficient_alignment(self, X, Y):# get from i,j to m,n
        m, n = len(X), len(Y)
        B = [[0] * 2 for _ in range(m + 1)]
        # for i in range(n + 1):
        #     B[m - i][1] = i * self.delta
        # print(B)
        for j in range(n, -1, -1):
            # B[m][0] = j * self.delta
            for i in range(m, -1, -1):
                if j == n:
                    B[i][1] = (m - i) * self.delta
                elif i == m:
                    B[m][1] = (n - j) * self.delta
                else:
                    B[i][1] = min(
                        self.alphas[X[i] + Y[j]] + B[i + 1][0],
                        self.delta + B[i + 1][1], self.delta + B[i][0])
            for i in range(0, m + 1):
                B[i][0] = B[i][1]
        # print(B[0][0])
        return B

    def align(self, a_string, b_string):
        len_a, len_b = len(a_string), len(b_string)
        OPT = [[0] * (len_b + 1) for _ in range(len_a + 1)]
        for i in range(len_a + 1):
            OPT[i][0] = i * self.delta
        for j in range(len_b + 1):
            OPT[0][j] = j * self.delta

        for j in range(1, len_b + 1):
            for i in range(1, len_a + 1):
                OPT[i][j] = min(
                    self.alphas[a_string[i - 1] + b_string[j - 1]] + OPT[i - 1][j - 1],
                    self.delta + OPT[i - 1][j], self.delta + OPT[i][j - 1])
        # backwards result
        i, j = len_a, len_b
        # item = 0
        alignment_a = []
        alignment_b = []
        while i >= 1 and j >= 1:
            # item += 1
            # print(item, i, j)
            if OPT[i][j] == self.alphas[a_string[i - 1] + b_string[j - 1]] + OPT[i - 1][j - 1]:
                alignment_a.append(a_string[i - 1])
                alignment_b.append(b_string[j - 1])
                i -= 1
                j -= 1
            elif OPT[i][j] == self.delta + OPT[i - 1][j]:  # 没变的是斜杠
                alignment_a.append(a_string[i - 1])
                alignment_b.append("_")
                i -= 1
            elif OPT[i][j] == self.delta + OPT[i][j - 1]:
                alignment_b.append(b_string[j - 1])
                alignment_a.append("_")
                j -= 1
        if i == 0:
            alignment_b.extend(b_string[:j])
            alignment_a.extend(["_"] * (j))
        elif j == 0:
            alignment_a.extend(a_string[:i])
            alignment_b.extend(["_"] * (i))
        alignment_a, alignment_b = alignment_a[::-1], alignment_b[::-1]
        # print("".join(alignment_a), "".join(alignment_b))
        # print("".join(alignment_a[:50:]), "".join(alignment_a[len(alignment_a) - 50::]))
        # print("".join(alignment_b[:50:]), "".join(alignment_b[len(alignment_b) - 50::]))
        # print(OPT[len_a][len_b])
        return OPT[len_a][len_b], alignment_a, alignment_b

    def divide_and_conquer_alignment(self, X, Y):
        m, n = len(X), len(Y)
        if m <= 2 or n <= 2:
            return self.align(X, Y) # c1, x, y
        prefix = self.space_efficient_alignment(X, Y[:n//2])
        suffix = self.backward_space_efficient_alignment(X, Y[n//2:])
        # print(prefix, suffix)
        min_fg_cost = float("inf")
        q = 0
        for i in range(m+1):
            if min_fg_cost > prefix[i][0] + suffix[i][0]:
                q = i
                min_fg_cost = prefix[i][0] + suffix[i][0]
        # print(min_fg_cost)
        self.Path.append((n//2, q))
        c1, p1, p2 = self.divide_and_conquer_alignment(X[:q], Y[:n//2])
        # x: q; y: n//2
        c2, s1, s2 = self.divide_and_conquer_alignment(X[q:], Y[n//2:])
        return c1 + c2, p1 + s1, p2 + s2

        # print("".join(alignment_a), "".join(alignment_b))
        # print("".join(alignment_a[:50:]), "".join(alignment_a[len(alignment_a) - 50::]))
        # print("".join(alignment_b[:50:]), "".join(alignment_b[len(alignment_b) - 50::]))
        # print(OPT[len_a][len_b])

if __name__ == '__main__':
    dp = EfficientSolution()
    # pid = os.getpid()
    # p = psutil.Process(pid)
    # info_start = p.memory_full_info().uss/1024
    tracemalloc.start()
    start_time = time.time()
    # print("/Users/chrisliu/PycharmProjects/test1/570/BaseTestcases_CS570FinalProject/" + str(sys.argv[i]))
    cost, alignment_a, alignment_b = dp.generate_result(sys.argv[1])
    _, peak = tracemalloc.get_traced_memory()
    over_time = time.time()
    # info_end = p.memory_full_info().uss/1024
    f = open("../output.txt", 'w')
    # print(len(alignment_a), len(alignment_b))
    f.write("".join(alignment_a[:50:]) + " " + "".join(alignment_a[len(alignment_a) - 50::]) + "\n")
    f.write("".join(alignment_b[:50:]) + " " + "".join(alignment_b[len(alignment_b) - 50::]) + "\n")
    f.write(str(cost) + "\n" + str(over_time - start_time) + "\n" + str(peak / 1024))
    tracemalloc.stop()

# if __name__ == '__main__':
#     dp = EfficientSolution()
#     # pid = os.getpid()
#     # p = psutil.Process(pid)
#     # info_start = p.memory_full_info().uss/1024
#     tracemalloc.start(25)
#
#     start_time = time.time()
#     dp.generate_result("/Users/chrisliu/PycharmProjects/test1/570/BaseTestcases_CS570FinalProject/input1.txt")
#     _, peak = tracemalloc.get_traced_memory()
#     over_time = time.time()
#     # info_end = p.memory_full_info().uss/1024
#     print("time: ", over_time - start_time)
#     print("memo: ", peak / 1024)