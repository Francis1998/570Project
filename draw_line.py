import gc
import time
import tracemalloc
import sys
memo_basic, memo_efficient, time_basic, time_efficient = [], [], [], []
import matplotlib.pyplot as plt
# %matplotlib inline
from basic import BasicSolution
from efficient import EfficientSolution

if __name__ == '__main__':
    basic_time_list, basic_memo_list, probsize_list = [], [], []
    # print(sys.argv)
    for i in range(1, len(sys.argv)):
        dp = BasicSolution()
        # pid = os.getpid()
        # p = psutil.Process(pid)
        # info_start = p.memory_full_info().uss/1024
        tracemalloc.start()
        start_time = time.time()
        # print("/Users/chrisliu/PycharmProjects/test1/570/BaseTestcases_CS570FinalProject/" + str(sys.argv[i]))
        cost, alignment_a, alignment_b = dp.generate_result("BaseTestcases_CS570FinalProject/" + sys.argv[i])
        _, peak = tracemalloc.get_traced_memory()
        over_time = time.time()
        # info_end = p.memory_full_info().uss/1024
        basic_time_list.append(over_time - start_time)
        basic_memo_list.append(peak / 1024)
        f = open("BaseTestcases_CS570FinalProject/output/output_basic_" + sys.argv[i], 'w')
        f.write("".join(dp.a_string[:50:]) + " " + "".join(dp.a_string[len(alignment_a) - 50::]) + "\n")
        f.write("".join(dp.b_string[:50:]) + " " + "".join(dp.b_string[len(alignment_b) - 50::]) + "\n")
        f.write(str(cost) + "\n" + str(over_time - start_time) + "\n" + str(peak / 1024))

        # print("time: ", over_time - start_time)
        # print("memo: ", i, peak / 1024)
        problem_size = len(alignment_a) + len(alignment_b)
        probsize_list.append(problem_size)
        tracemalloc.stop()
    # print(probsize_list)
    # print(basic_memo_list)
    efficient_time_list, efficient_memo_list = [], []
    ##################################
    for i in range(1, len(sys.argv)):
        tracemalloc.start()
        dp = EfficientSolution()
        # pid = os.getpid()
        # p = psutil.Process(pid)
        # info_start = p.memory_full_info().uss/1024
        start_time = time.time()
        # cost, alignment_a, alignment_b = dp.generate_result("../570/BaseTestcases_CS570FinalProject/" + sys.argv[i])
        cost, alignment_a, alignment_b = dp.generate_result("BaseTestcases_CS570FinalProject/" + sys.argv[i])
        _, peak = tracemalloc.get_traced_memory()
        over_time = time.time()
        # info_end = p.memory_full_info().uss/1024
        efficient_time_list.append(over_time - start_time)
        efficient_memo_list.append(peak / 1024)
        # f = open("../570/BaseTestcases_CS570FinalProject/output/output_efficient_" + sys.argv[i] , 'w')
        f = open("output_efficient_" + sys.argv[i], 'w')
        f.write("".join(alignment_a[:50:]) + " " + "".join(alignment_a[len(alignment_a) - 50::]) + "\n")
        f.write("".join(alignment_b[:50:]) + " " + "".join(alignment_b[len(alignment_b) - 50::]) + "\n")
        f.write(str(cost) + "\n" + str(over_time - start_time) + "\n" + str(peak / 1024))
        # print("time: ", over_time - start_time)
        # print("memo: ", peak / 1024)
        # problem_size = len(dp.a_string) * len(dp.b_string)
        # probsize_list.append(problem_size)
        tracemalloc.stop()
    basic_sequence_list = []
    # print(probsize_list)
    efficient_sequence_list = []
    for i in range(len(probsize_list)):
        basic_sequence_list.append([probsize_list[i], basic_time_list[i], basic_memo_list[i]])
        efficient_sequence_list.append([probsize_list[i], efficient_time_list[i], efficient_memo_list[i]])
    # print(basic_sequence_list)
    # print(efficient_sequence_list)
    basic_sequence_list.sort(key=lambda x: x[0])
    efficient_sequence_list.sort(key=lambda x: x[0])
    # print(efficient_sequence_list)
    probsize_list = [pl[0] for pl in basic_sequence_list]
    basic_time_list = [pl[1] for pl in basic_sequence_list]
    basic_memo_list = [pl[2] for pl in basic_sequence_list]
    efficient_time_list = [pl[1] for pl in efficient_sequence_list]
    efficient_memo_list = [pl[2] for pl in efficient_sequence_list]

    # print(len(probsize_list),len(basic_time_list),len(efficient_time_list))
    # fig, ax = plt.subplots(1, 1)
    # ax.plot(probsize_list, basic_time_list, label='trend')
    # ax.set_title('title test', fontsize=12, color='r')
    # plt.show()

    # plt.figure()          # 创建画布
    plt.plot(probsize_list, basic_time_list, color="r", label="basicTime")    # 画图
    plt.plot(probsize_list, efficient_time_list, color="b", label="efficientTime")    # 画图, x, y
    plt.savefig("./graph/CPUPlot.jpg")
    plt.show()           # 图显示
    plt.close()
    # print(basic_memo_list)
    # print(efficient_memo_list)
    plt.figure()  # 创建画布
    plt.plot(probsize_list, basic_memo_list, color="r", label="basicMemo")  # 画图
    plt.plot(probsize_list, efficient_memo_list, color="b", label="efficientMemo")  # 画图, x, y
    plt.savefig("./graph/MemoryPlot.jpg")
    plt.show()  # 图显示
    plt.close()
    print("running success")
# command - python draw_line.py input1.txt input2.txt input3.txt input4.txt input5.txt input6.txt input7.txt input8.txt input9.txt input10.txt input11.txt input12.txt input13.txt input14.txt input15.txt