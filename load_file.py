import numpy as np

#
# 1 Latitude or Longitude --> 1000 m
def load_EUA(num_users=1000000, num_bs=100000, radius=1000, meter_per_degree=111111):
    users = np.loadtxt("users.csv", dtype=float, delimiter=',', skiprows=1)
    np.random.shuffle(users)
    users = np.delete(users, np.s_[num_users:], 0)
    num_users = users.shape[0]

    max_loc = np.max(users, axis=0)
    min_loc = np.min(users, axis=0)

    users = (users - min_loc) * meter_per_degree

    bs = np.loadtxt("site.csv", dtype=float, delimiter=',', skiprows=1)
    np.random.shuffle(bs)

    filt = (bs <= max_loc+radius/meter_per_degree) * (bs >= min_loc-radius/meter_per_degree)
    bs = bs[np.all(filt, axis=1)]
    bs = np.delete(bs, np.s_[num_bs:], 0)

    num_bs = bs.shape[0]
    print(num_users, num_bs)

    bs = (bs - min_loc) * meter_per_degree

    cover_flag = [False]*num_users
    cover = []
    for i in range(num_bs):
        dis = np.sum((users - bs[i]) ** 2, axis=1)
        c = (dis <= radius**2)
        cover.append(c.astype(int).tolist())
        cover_flag = cover_flag + c

    return users.tolist(), bs.tolist(), cover, sum(cover_flag)

'''
num_users = 1000000
num_bs = 10000
radius = 100
users, bs, cover, cnum = load_EUA(num_users, num_bs, radius)
num_bs = len(bs)
num_users = len(users)
print(num_users, num_bs, cnum)

plt.figure(figsize=(10, 10), dpi=80)
plt.xticks([])
plt.yticks([])
plt.scatter([u[0] for u in users], [u[1] for u in users], marker='o', c='none', edgecolors='b')
plt.scatter([b[0] for b in bs], [b[1] for b in bs], marker='^', c='none', edgecolors='r')
plt.show()
'''
