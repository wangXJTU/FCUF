import sys
from cluster import kmeans_repeat, kmeans_bs, kmeans_bound
import time
from greedy import max_cover_first, ff, less_BS_first
from load_file import load_EUA


num_users = 10000000
num_bs = 100000
radius = 1000  # m
meter_per_degree = 111111

users, bs, cover, cnum = load_EUA(num_users, num_bs, radius, meter_per_degree)
num_users = len(users)
num_bs = len(bs)

# result_file = "result-EUA.csv"
result_file = "result-EUA" + str(num_users) + "u-" + str(num_bs) + "BS" + ".csv"

rfile = open(result_file, "a")
print(num_users, "users", sep=',', file=rfile)
print(num_bs, "base stations", sep=',', file=rfile)
print(cnum, "covered users", sep=',', file=rfile)

print("method", "#BS", "#coverage(%)", "#repeat", "time", sep=',', file=rfile)
start_time = time.time()
selected_bs_index, cover_num = max_cover_first(cover)
end_time = time.time()
print("Greedy", len(selected_bs_index), cover_num / cnum * 100, 0, \
      (end_time - start_time) / 3600, sep=',', file=rfile)
rfile.flush()
sys.stderr.write("Greedy\n")

start_time = time.time()
selected_bs_index, cover_num = ff(cover)
end_time = time.time()
print("FF", len(selected_bs_index), cover_num / cnum * 100, 0, \
      (end_time - start_time) / 3600, sep=',', file=rfile)
rfile.flush()
sys.stderr.write("FF\n")

start_time = time.time()
selected_bs_index, cover_num = kmeans_bs(users, bs, cover)
end_time = time.time()
print("Kmeans", len(selected_bs_index), cover_num / cnum * 100, 1, \
      (end_time - start_time) / 3600, sep=',', file=rfile)
rfile.flush()
sys.stderr.write("kmeans_bs\n")

start_time = time.time()
selected_bs_index, cover_num, repeat_time = kmeans_bound(users, bs, cover, radius)
# selected_bs_index, cover_num, repeat_time = kmeans_bound_rev(users, bs, cover, radius)
end_time = time.time()
print("Kmeans-B", len(selected_bs_index), cover_num / cnum * 100, repeat_time, \
      (end_time - start_time) / 3600, sep=',', file=rfile)
rfile.flush()
sys.stderr.write("kmeans_bound\n")

start_time = time.time()
selected_bs_index, cover_num, repeat_time = kmeans_repeat(users, bs, cover)
end_time = time.time()
print("Kmeans-R", len(selected_bs_index), cover_num / cnum * 100, repeat_time, \
      (end_time - start_time) / 3600, sep=',', file=rfile)
rfile.flush()
sys.stderr.write("kmeans_repeat\n")

start_time = time.time()
selected_bs_index, cover_num = less_BS_first(cover)
end_time = time.time()
print("FCUF", len(selected_bs_index), cover_num / cnum * 100, 0, \
      (end_time - start_time) / 3600, sep=',', file=rfile)
rfile.flush()
sys.stderr.write("FCUF\n")
rfile.close()
