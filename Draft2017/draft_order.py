import numpy as np

teams = np.array(["Adam", "Chase", "David", "Michael",
                  "Petr", "Samir", "Scott", "Wyatt"])

order_seed, conf_seed = 345, 9173
rng1 = np.random.RandomState(order_seed)
rng2 = np.random.RandomState(conf_seed)

order = rng1.permutation(8)
conf = rng2.permutation(8)

print "Draft Order:\n", teams[order], "\n"
print "Conference 1:\n", teams[conf[:4]], "\n"
print "Conference 2:\n", teams[conf[4:]]
