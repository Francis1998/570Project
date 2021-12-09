"""
1.Memory in the program should be in Kilobytes and Time taken by the program should be in seconds. You can use
linux utility command time to measure the time and /usr/bin/time (https://unix.stackexchange.com/a/18851) to measure
the memory usage respectively. These are one of the many examples, you can use anything for measuring the
performance. Memory taken by your program refers to the amount of RAM/ Resident set size used.

2.The memory plot and the time plot need to have just 2 line plots, one from the basic version and the other from the
advanced version. You can estimate datapoints by generating multiple test cases by yourself. You need to generate
valid pngs when you submit.

3.Memory and time values in the output txt file are float values.

4.containing the cost of the alignment as well in the 3rd line, followed by memory and time taken in the 4th and the
5th line respectively.

5.Yes your code be tested on a series of input text files? You need to code your programs to take inputs from the
user through the command line.

6.Please don’t use any fancy plots for the graphs for time and memory. Just a line graph of about 15-20 data points
should be sufficient.

7.Your program should not print anything when it is run. It should only write to output.txt file.

8.X axis of the plot needs to be the problem size, which is length of the larger string out of the 2 strings (not the
length of the base strings but the length of the final strings)

"""
import os
import sys
import time
import tracemalloc

import psutil


class BasicSolution:
    def __init__(self):
        self.alphas = {"AA": 0, "CC": 0, "GG": 0, "TT": 0,
                       "AC": 110, "CA": 110, "AG": 48, "GA": 48,
                       "AT": 94, "TA": 94, "CG": 118, "GC": 118,
                       "GT": 110, "TG": 110, "CT": 48, "TC": 48}
        self.delta = 30
        self.a_string = ""
        self.b_string = ""

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
        return self.calculate_dp_cost(self.a_string, self.b_string)
        # self.calculate_dp_cost(self.b_string, self.a_string)

    def calculate_dp_cost(self, a_string, b_string):
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
            elif OPT[i][j] == self.delta + OPT[i - 1][j]:# 没变的是斜杠
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
        self.a_string, self.b_string = alignment_a[::-1], alignment_b[::-1]

        # print("".join(alignment_a) , "".join(alignment_b))
        # print("".join(self.a_string[:50:]), "".join(self.a_string[len(alignment_a) - 50::]))
        # print("".join(self.b_string[:50:]), "".join(self.b_string[len(alignment_b) - 50::]))
        # print(OPT[len_a][len_b])
        # for i in range(80):
        #     if alignment_a[i] != "_______ACACACTG__ACTAC_TGACTG_GTGA__C_TACTGACGTGACTGACTACTGACGTGTGACTAC_TGACTG_G"[i]:
        #         print(i, alignment_a[i], "_______ACACACTG__ACTAC_TGACTG_GTGA__C_TACTGACGTGACTGACTACTGACGTGTGACTAC_TGACTG_G"[i])
        return OPT[len_a][len_b], alignment_a, alignment_b

if __name__ == '__main__':
    tracemalloc.start()
    dp = BasicSolution()
    # pid = os.getpid()
    # p = psutil.Process(pid)
    # info_start = p.memory_full_info().uss/1024
    start_time = time.time()
    # print("/Users/chrisliu/PycharmProjects/test1/570/BaseTestcases_CS570FinalProject/" + str(sys.argv[i]))
    cost, alignment_a, alignment_b = dp.generate_result(sys.argv[1])
    over_time = time.time()
    # info_end = p.memory_full_info().uss/1024
    f = open("../output.txt", 'w')
    # print(len(dp.a_string), len(dp.b_string))
    f.write("".join(dp.a_string[:50:]) + " " + "".join(dp.a_string[len(alignment_a) - 50::]) + "\n")
    f.write("".join(dp.b_string[:50:]) + " " + "".join(dp.b_string[len(alignment_b) - 50::]) + "\n")
    _, peak = tracemalloc.get_traced_memory()
    f.write(str(cost) + "\n" + str(over_time - start_time) + "\n" + str(peak / 1024))
    tracemalloc.stop()

#     time_list, memo_list, probsize_list = [], [], []
#     for i in range(1, 2):
#         dp = BasicSolution()
#         # pid = os.getpid()
#         # p = psutil.Process(pid)
#         # info_start = p.memory_full_info().uss/1024
#         tracemalloc.start(25)
#         start_time = time.time()
#         dp.generate_result("/Users/chrisliu/PycharmProjects/test1/570/BaseTestcases_CS570FinalProject/input"+str(2)+".txt")
#         _, peak = tracemalloc.get_traced_memory()
#         over_time = time.time()
#         # info_end = p.memory_full_info().uss/1024
#         time_list.append(over_time - start_time)
#         memo_list.append(peak / 1024)
#         # print("time: ", over_time - start_time)
#         # print("memo: ", peak / 1024)
#         problem_size = len(dp.a_string) * len(dp.b_string)
#         probsize_list.append(problem_size)
#     print(probsize_list)