import os
from posixpath import expanduser

from os import path
import sys
import os.path
import sys

from scapy.all import *
from scapy.utils import RawPcapReader, rdpcap
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, UDP, TCP

# this pcap_operation file is to get files from folder 
# and pass that list to pcap2csv generator

def listDir(dir):

    filenames = [os.path.join(dir, file) for file in os.listdir(dir)]

    return filenames

# ip_address = '192.168.43.153'
# ip_address = '2001:4860:4864:6::1d'
ip_address = ['192.168.43.153', '2001:4860:4864:6::1d']
def pcap2csv(in_pcap, out_csv):
    
    frame_num = 0
    ignored_packets = 0

    print(in_pcap)
    pkt1 = rdpcap(in_pcap)
  
    pkt = pkt1[0]
    try:

        if IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            if(ip_address[0] == src_ip):
                up_down = 1
            else:
                up_down = 0
            l3_proto = 4
        else:
            src_ip = pkt['IPv6'].src
            dst_ip = pkt['IPv6'].dst
            if(ip_address[1] == src_ip):
                up_down = 1
            else:
                up_down = 0
            l3_proto = 6
        if TCP in pkt:
            sport=pkt[TCP].sport
            dport=pkt[TCP].dport
            pkt_len = len(pkt[TCP])
            proto = 6
        elif UDP in pkt:
            sport=pkt[UDP].sport
            dport=pkt[UDP].dport
            pkt_len = len(pkt[UDP])
            proto = 17
        else:
            return False
        
        print("before time ")
        time = pkt.time
        print("after time")
        # print(pkt[IP].chksum)
        # print(time)
        # print(ip_pkt[TCP].options[2][1][0])
        # print(f"1. timestamp is {time}")
        
    except:
        print('in except block')
        return False
    
    #       |   |   |   |    |   |   |   |   |   o-----> {9}  total pkt length
    #       |   |   |   |    |   |   |   |   o---------> {8}  dst port        -     ---------
    #       |   |   |   |    |   |   |   o-------------> {7}  dst ip address           ---------
    #       |   |   |   |    |   |   o-----------------> {6}  src port                ------ 
    #       |   |   |   |    |   o---------------------> {5}  src ip address -----------------
    #       |   |   |   |    o-------------------------> {4}  text description ------------
    #       |   |   |   o------------------------------> {3}  L4 protocol  
    #       |   |   o----------------------------------> {2}  highest protocol -----------------
    #       |   o--------------------------------------> {1}  time  ------------------
    #       o------------------------------------------> {0}  frame number --------------


def files2csv(filenames):
    
    for filename in filenames:
        filecsv = filename.removesuffix('.pcap')
        filecsv = filecsv + '.csv'
       
        pcap2csv(filename, filecsv)

        
def __main__():
   
    try:
        if path.isfile(sys.argv[1]): 
            print("entered here")
            files2csv([str(sys.argv[1])])

        elif path.isdir(sys.argv[1]):
            # print(sys.argv[1])
            filenames = listDir(str(sys.argv[1]))
            files2csv(filenames)
        
        print("successful converstion to csv")
    except:
        print("some error occured")
        exit(0)

__main__()


#!/usr/bin/env python3



#--------------------------------------------------

# def render_csv_row(pkt_sc, fh_csv):
    
#     l = list(sc.expand(pkt_sc))

#     if(len(l) < 3):
#         return False
    
#     if l[2] == 'UDP':
#         udp_pkt_sc = pkt_sc[UDP]
#         l4_payload_bytes = bytes(udp_pkt_sc.payload)
#         l4_proto_name = 'UDP'
#         l4_sport = udp_pkt_sc.sport
#         l4_dport = udp_pkt_sc.dport
#     elif l[2] == 'TCP':
#         tcp_pkt_sc = pkt_sc[TCP]
#         l4_payload_bytes = bytes(tcp_pkt_sc.payload)
#         l4_proto_name = 'TCP'
#         l4_sport = tcp_pkt_sc.sport
#         l4_dport = tcp_pkt_sc.dport
#     else:
#         # Currently not handling packets that are not UDP or TCP
#         print('Ignoring non-UDP/TCP packet')
#         return False

#     # Each line of the CSV has this format
#     fmt = '{0}|{1}|{2}({3})|{4}|{5}|{6}|{7}|{8}|{9}|{10}'
#     #       |   |   |   |    |   |   |   |   |   |   |
#     #       |   |   |   |    |   |   |   |   |   |   o-> {10} L4 payload hexdump
#     #       |   |   |   |    |   |   |   |   |   o-----> {9}  total pkt length
#     #       |   |   |   |    |   |   |   |   o---------> {8}  dst port
#     #       |   |   |   |    |   |   |   o-------------> {7}  dst ip address
#     #       |   |   |   |    |   |   o-----------------> {6}  src port
#     #       |   |   |   |    |   o---------------------> {5}  src ip address
#     #       |   |   |   |    o-------------------------> {4}  text description
#     #       |   |   |   o------------------------------> {3}  L4 protocol
#     #       |   |   o----------------------------------> {2}  highest protocol
#     #       |   o--------------------------------------> {1}  time
#     #       o------------------------------------------> {0}  frame number

#     # Example:
#     # 1|0.0|DNS(UDP)|Standard query 0xf3de A www.cisco.com|192.168.1.116:57922|1.1.1.1:53|73|f3de010000010000000000000377777705636973636f03636f6d0000010001

#     print(fmt.format(pkt_sc.no,               # {0}
#                      pkt_sc.time,             # {1}
#                      pkt_sc.protocol,         # {2}
#                      l4_proto_name,           # {3}
#                      pkt_sc.info,             # {4}
#                      pkt_sc.source,           # {5}
#                      l4_sport,                # {6}
#                      pkt_sc.destination,      # {7}
#                      l4_dport,                # {8}
#                      pkt_sc.length,
#                                # {9}
#                      l4_payload_bytes.hex()), # {10}
#           file=fh_csv)

#     return True
    #--------------------------------------------------



