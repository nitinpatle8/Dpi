#!/usr/bin/python

from scapy.all import *
from os import path
from scapy.all import *
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

chat_pcap = rdpcap("../pcapfiles/videostreaming/youtube_4K_pc_videostreaming_6.7-1.2_41.pcap");

pcap1 = chat_pcap

time1 = pcap1[0].time

t = []

# print(pkt.payload)

# print(pcap1.plot(lambda x:[x.time- time1, len(x)]))

l = [0 for i in range(60*10)]

bin = [i/10 for i in range(60*10)]

for pkt in pcap1:
    ti = (int)(round(pkt.time-time1, 1))
    if (ti < 60):
        l[ti*10]+=len(pkt)


# plt.hist2d(t, l);

print(len(l), len(bin))
# plt.bar(bin, l)

z = []
y = []

for pkt in pcap1:
    z.append((int)(round(pkt.time-time1,1)))
    y.append(len(pkt))

plt.scatter(z, y)

plt.show()


