from sklearn.cluster import KMeans
import copy
import numpy as np
import warnings
import math
import sys

warnings.filterwarnings("ignore")


def closest_bs(bs, c, bs_flag=None):
    dis = ((np.array(bs)-c)**2).sum(axis=1)
    if bs_flag is not None:
        dis[bs_flag] = np.max(dis)
    closest_idx = np.argmin(dis)
    return closest_idx


def kmeans_repeat(users, bs, cover, n_clusters=6):
    num_users = len(users)
    num_bs = len(bs)
    if num_users <= 1:
        return [], 0, 0
    selected_bs_index = []
    cover_num = 0
    user_copy = copy.deepcopy(users)  # deleting covered user in each iteration
    cover_copy = copy.deepcopy(cover)
    repeat_time = 0
    bs_flag = [False] * num_bs
    while (not all(bs_flag)) and (0 != len(user_copy)):
        repeat_time += 1
        selected_bs_num = len(selected_bs_index)
        n_clusters = max(n_clusters - selected_bs_num, 2)
        n_clusters = min(n_clusters, len(user_copy))
        if n_clusters >= 2:
            kmeans = KMeans(n_clusters, n_init=10)
            kmeans.fit(user_copy)
            centroids = kmeans.cluster_centers_
            centre_bs = list(map(lambda x: closest_bs(bs, x, bs_flag), centroids))
        # for c in centroids:
            # bs_idx = closest_bs(bs, c)
            # centre_bs.append(bs_idx)
        # print(centre_bs)
        else:
            centre_bs = closest_bs(bs, user_copy[0], bs_flag)
        for bs_idx in centre_bs:
            bs_flag[bs_idx] = True
            norepeat = True
            for user_idx in range(num_users):
                if cover_copy[bs_idx][user_idx]:
                    cover_num += 1
                    user_copy.remove(users[user_idx])
                    if norepeat:
                        selected_bs_index.append(bs_idx)
                        norepeat = False
                    for j in range(num_bs):
                        cover_copy[j][user_idx] = 0

    return list(set(selected_bs_index)), cover_num, repeat_time


def kmeans_bs(users, bs, cover):
    num_users = len(users)
    num_bs = len(bs)
    if num_users <= 1:
        return [], 0, 0
    selected_bs_index = []
    cover_num = 0
    user_copy = copy.deepcopy(users)  # deleting covered user in each iteration
    cover_copy = copy.deepcopy(cover)
    num_k = min(num_bs, num_users)
    kmeans = KMeans(num_k, n_init=10)
    kmeans.fit(user_copy)
    centre_bs = list(map(lambda x: closest_bs(bs, x), kmeans.cluster_centers_))
    for bs_idx in centre_bs:
        for user_idx in range(num_users):
            if cover_copy[bs_idx][user_idx]:
                cover_num += 1
                selected_bs_index.append(bs_idx)
                for j in range(num_bs):
                    cover_copy[j][user_idx] = 0

    return list(set(selected_bs_index)), cover_num


def in_coverage(x, y, bound):
    return (x[0]-y[0])**2 + (x[1]-y[1])**2 <= bound**2


def max_dis(users):
    num_users = len(users)
    max_distance = 0
    for i in range(num_users-1):
        for j in range(i+1, num_users):
            dis = (users[i][0]-users[j][0])**2 + (users[i][1]-users[j][1])**2
            if max_distance < dis:
                max_distance = dis
    return max_distance


def kmeans_bound(users, bs, cover, bound):
    num_users = len(users)
    num_bs = len(bs)
    if num_users <= 1:
        return [], 0, 0
    selected_bs_index = []
    cover_num = 0
    user_copy = copy.deepcopy(users)  # deleting covered user in each iteration
    low_b = int(math.sqrt(max_dis(user_copy)) / (2 * bound))
    centroids = []
    for num_k in range(low_b, num_bs+1):
        kmeans = KMeans(num_k, n_init=10)
        kmeans.fit(user_copy)
        centroids = kmeans.cluster_centers_
        labels = kmeans.labels_
        in_cover = True
        for u in range(num_users):
            if not in_coverage(users[u], centroids[labels[u]], bound):
                in_cover = False
                break
        if in_cover:
            break

    cover_copy = copy.deepcopy(cover)
    for c in centroids:
        bs_idx = closest_bs(bs, c)
        selected_bs_index.append(bs_idx)
        for u in range(num_users):
            if cover_copy[bs_idx][u] == 1:
                cover_num += 1
                for b in range(num_bs):
                    cover_copy[b][u] = 0

    return list(set(selected_bs_index)), cover_num, num_k


def kmeans_bound_rev(users, bs, cover, bound):
    num_users = len(users)
    num_bs = len(bs)
    if num_users <= 1:
        return [], 0, 0
    selected_bs_index = []
    cover_num = 0
    user_copy = copy.deepcopy(users)  # deleting covered user in each iteration
    low_b = int(math.sqrt(max_dis(user_copy)) / (2 * bound))
    centroids = []
    for num_k in range(num_bs, low_b-1, -1):
        sys.stderr.write("kmeans_bound: %d BS\n"%num_k)
        kmeans = KMeans(num_k, n_init=10)
        kmeans.fit(user_copy)
        centroids = kmeans.cluster_centers_
        labels = kmeans.labels_
        in_cover = False
        for u in range(num_users):
            if not in_coverage(users[u], centroids[labels[u]], bound):
                in_cover = True
                break
        if in_cover:
            break

    if num_k < num_bs:
        num_k -= 1
    kmeans = KMeans(num_k, n_init=10)
    kmeans.fit(user_copy)
    centroids = kmeans.cluster_centers_

    cover_copy = copy.deepcopy(cover)
    for c in centroids:
        bs_idx = closest_bs(bs, c)
        selected_bs_index.append(bs_idx)
        for u in range(num_users):
            if cover_copy[bs_idx][u] == 1:
                cover_num += 1
                for b in range(num_bs):
                    cover_copy[b][u] = 0

    return list(set(selected_bs_index)), cover_num, num_k

def kmeans_cover(users, bs, cover, bound):
    num_users = len(users)
    num_bs = len(bs)
    if num_users <= 1:
        return [], 0, 0
    user_copy = copy.deepcopy(users)  # deleting covered user in each iteration
    # deleting users not covered by any bs
    for i in range(num_users):
        is_cover = False
        for b in range(num_bs):
            if cover[b][i] == 1:
                is_cover = True
                break
        if not is_cover:
            user_copy.remove(users[i])
    # print(len(user_copy))
    # the low bound of BS number
    low_b = int(math.sqrt(max_dis(user_copy)) / (2 * bound))
    cbs = []
    for num_k in range(low_b, num_bs):
        if len(user_copy) > num_k:
            cbs = [closest_bs(bs, c) for c in user_copy]
            break
        kmeans = KMeans(num_k, n_init=10)
        kmeans.fit(user_copy)
        labels = kmeans.labels_
        cbs = [closest_bs(bs, c) for c in kmeans.cluster_centers_]
        in_cover = True
        for u in range(len(user_copy)):
            if not in_coverage(user_copy[u], bs[cbs[labels[u]]], bound):
                in_cover = False
                break
        if in_cover:
            break

    return list(set(cbs)), len(user_copy), num_k-low_b+1


'''
# 1 km * 1 km
area = {'x': 1000, 'y': 1000}
users = []
num_users = 1000
# base station
bs = []
num_bs = 100
# bs * users
cover = []
radius = 100  # m

users, bs, cover, cnum = init_sys(area, num_users, num_bs, radius)

print(num_users, "users")
print(num_bs, "base stations")
print(cnum, "covered users")
print("method", "#BS", "#covered users", "#repeat")

selected_bs_index, cover_num, repeat_time = kmeans_cover(users, bs, cover, radius)
print("kmeans_cover", len(selected_bs_index), cover_num, repeat_time)

selected_bs_index, cover_num = kmeans_bound(users, bs, cover, radius)
print("kmeans_bound", len(selected_bs_index), cover_num)

selected_bs_index, cover_num, repeat_time = kmeans_repeat(users, bs, cover, num_bs)
print("kmeans_repeat", len(selected_bs_index), cover_num, repeat_time)

selected_bs_index, cover_num = kmeans_bs(users, bs, cover)
print("kmeans_bs", len(selected_bs_index), cover_num)

'''
