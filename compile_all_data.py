import os
import numpy as np
import pickle 
import matplotlib.pyplot as plt

path = os.path.join(os.getcwd(), "all_data")
rec_files = os.listdir(path)
full_rec = {}

for rec_file in rec_files:
    with open(os.path.join(path, rec_file), "rb") as fp:
        rec = dict(pickle.load(fp))
    p = rec["p"]
    n = rec["n"]
    trials_done = rec["trials_done"]
    hits = rec["hits"]
    if n not in full_rec.keys():
        full_rec[n] = {}
    if p not in full_rec[n].keys():
        full_rec[n][p] = {"trials_done":trials_done, "hits":hits}
    else:
        full_rec[n][p]["trials_done"] += trials_done
        full_rec[n][p]["hits"] += hits
    
# print(full_rec)

corr_length_rec = {}
for n in full_rec.keys():
    p_vals = np.array(sorted(list(full_rec[n].keys())))
    density = []
    corr_length_rec[n] = {}
    for p in p_vals:
        density.append(full_rec[n][p]["hits"]/full_rec[n][p]["trials_done"])
        corr_length_rec[n][p] = -n*(1/np.log(density[-1]))
    density = np.array(density)
    print(p_vals, density)
    plt.plot(p_vals, density, '.-')
    plt.title(f"n = {n}")
    plt.savefig(f"p vs connectivity (n={n}).png")
    plt.close()

    plt.plot(p_vals, -n*(1/np.log(density)), '.-')
    # plt.plot(p_vals, (0.5-p_vals)**(-nu))
    plt.title(f"n = {n}")
    plt.savefig(f"p vs corr_length (n={n}).png")
    plt.close()

with open(os.path.join(os.getcwd(), "data.pkl") , "wb") as fp:
    pickle.dump(corr_length_rec, fp)

    