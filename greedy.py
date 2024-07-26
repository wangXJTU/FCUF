import copy
from operator import itemgetter
from load_file import load_telcom, load_EUA, load_telcom_cpy

# select the BS covering the most users
def max_cover_first(cover):
    cover_copy = copy.deepcopy(cover)
    cover_num_list = [sum(c) for c in cover_copy]
    selected_bs_index = []
    cover_num = 0
    num_bs = len(cover_copy)
    num_user = len(cover_copy[0])
    while sum(cover_num_list) != 0:
        max_cover = max(cover_num_list)
        max_bs_index = cover_num_list.index(max_cover)
        selected_bs_index.append(max_bs_index)
        cover_num += sum(cover_copy[max_bs_index])
        for u in range(num_user):
            if cover_copy[max_bs_index][u] == 1:
                for b in range(num_bs):
                    cover_copy[b][u] = 0
        cover_num_list = [sum(c) for c in cover_copy]
    return selected_bs_index, cover_num


# select the first BS
def ff(cover):
    cover_copy = copy.deepcopy(cover)
    selected_bs_index = []
    cover_num = 0
    num_bs = len(cover_copy)
    num_user = len(cover_copy[0])
    for bs in range(num_bs):
        covered = sum(cover_copy[bs])
        if covered != 0:
            selected_bs_index.append(bs)
            cover_num += covered
            for u in range(num_user):
                if cover_copy[bs][u] == 1:
                    for b in range(num_bs):
                        cover_copy[b][u] = 0
    return selected_bs_index, cover_num


#  users with the less BSs first
def less_BS_first(cover):
    cover_copy = copy.deepcopy(cover)
    selected_bs_index = []
    cover_num = 0
    num_bs = len(cover_copy)
    num_user = len(cover_copy[0])
    # [user_index, num_bs covering the user]
    cover_bs = [[i, 0] for i in range(num_user)]
    for u in range(num_user):
        cover_bs[u][1] = sum([cover_copy[b][u] for b in range(num_bs)])
    # cover_bs = sorted(cover_bs, key=itemgetter(1))
    cover_bs.sort(key=itemgetter(1))
    while 0 == cover_bs[0][1]:
        cover_bs.pop(0)
    while len(cover_bs) > 0:
        max_bs = [0, 0]
        for b in range(num_bs):
            if 1 == cover_copy[b][cover_bs[0][0]]:
                cnum = sum(cover_copy[b])
                if max_bs[1] < cnum:
                    max_bs = [b, cnum]
        if max_bs[1] > 0:
            selected_bs_index.append(max_bs[0])
            cover_num += max_bs[1]
            # remove the coverage of selected max_bs to its covered users
            # and the coverage of these covered users
            for u in range(num_user):
                # removing user u in cover_copy and cover_bs
                if cover_copy[max_bs[0]][u] == 1:
                    for b in range(num_bs):
                        cover_copy[b][u] = 0
                    for i in range(len(cover_bs)):
                        cbs = cover_bs[i]
                        if cbs[0] == u:
                            cover_bs.pop(i)
                            break
        cover_bs.sort(key=itemgetter(1))

    return selected_bs_index, cover_num


'''
users, bs, cover, cnum = load_EUA()
num_users = len(users)
num_bs = len(bs)


selected_bs_index, cover_num = less_BS_first(cover)
print("less_BS_first", len(selected_bs_index), cover_num / cnum * 100)

selected_bs_index, cover_num = max_cover_first(cover)
print("Greedy", len(selected_bs_index), cover_num / cnum * 100)
'''
