#!/usr/bin/env python3

from logging import error
from os import supports_bytes_environ
import os.path
import sys
from scapy.all import *
from scapy.utils import RawPcapReader
from scapy.layers.inet import IP, UDP, TCP
import deletecsv as dl
#--------------------------------------------------

# ip address in string format
# pkt , fh_csv, ip_address, srno, category[3], starting_time, last_relative_time
def render_csv_row(pkt, fh_csv, ip_address, srno, category, starting_time, last_relative_time):

    try:

        if IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            if(src_ip in ip_address):
                up_down = 1
            else:
                up_down = 0
            l3_proto = 4
        else:
            # src_ip = pkt['IPv6'].src
            # dst_ip = pkt['IPv6'].dst
            # if(ip_address[1] == src_ip):
            #     up_down = 1
            # else:
            #     up_down = 0
            # l3_proto = 6
            raise Exception('this packet using IPv6 address')
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
        
        time = pkt.time - starting_time

        if(time >= last_relative_time):
            return False  
        # print(pkt[IP].chksum)
        # print(time)
        # print(ip_pkt[TCP].options[2][1][0])
        # print(f"1. timestamp is {time}")
        
    except:
        print('in except block may be using IPv6')
        raise Exception("this packet can't be processed")
        return False

    # Each line of the CSV has this format
    fmt = '{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|{8}|{9}|{10}'
    #       |   |   |   |    |   |   |   |   |  |    
    #       |   |   |   |    |   |   |   |   |  |    
    #       |   |   |   |    |   |   |   |   |  o------> {10}  category 
    #       |   |   |   |    |   |   |   |   o---------> {9}  dst port
    #       |   |   |   |    |   |   |   o-------------> {8}  src port
    #       |   |   |   |    |   |   o-----------------> {7}  dst ip address
    #       |   |   |   |    |   o---------------------> {6}  src ip address
    #       |   |   |   |    o-------------------------> {5}  L4 protocol
    #       |   |   |   o------------------------------> {4}  L3 protocol
    #       |   |   o----------------------------------> {3}  pkt length L4
    #       |   o--------------------------------------> {2}  time
    #       o------------------------------------------> {1}  upstream/downstream
    #       o------------------------------------------> {0} sr_no

    # Example:
    

    print(fmt.format( srno,                     # {0} 
                        up_down,               # {1}
                     time,             # {2}
                     pkt_len,         # {3}
                     l3_proto,           # {4}
                     proto,             # {5}
                     src_ip,           # {6}
                     dst_ip,                # {7}
                     sport,      # {8}
                     dport,                # {9}
                     category,        #{10}
                    ), 
          file=fh_csv)

    return True
    #--------------------------------------------------

def pcap2csv(in_pcap, out_csv, ip_address, last_relative_time):
    """Main entry function called from main to process the pcap and
    generate the csv file.
    in_pcap = name of the input pcap file (guaranteed to exist)
    out_csv = name of the output csv file (will be created)
    This function walks over each packet in the pcap file, and for
    each packet invokes the render_csv_row() function to write one row
    of the csv.
    """
    frame_num = 0
    ignored_packets = 0
    
    with open(out_csv, 'w') as fh_csv:
        # Open the pcap file with scapy's RawPcapReader, and iterate over
        # each packet. In each iteration get the PyShark packet as well,
        # and then call render_csv_row() with both representations to generate
        # the CSV row.
        srno = 1
        category = os.path.basename(out_csv).split('_')
        # print(category)
        pkts = rdpcap(in_pcap)
        starting_time = pkts[0].time
       
        for pkt in pkts:
            try:
                frame_num += 1
                
                if not render_csv_row(pkt , fh_csv, ip_address, srno, category[3], starting_time, last_relative_time):
                    ignored_packets += 1
                else:
                    srno += 1
                
            except:
                print("some error while processing this pcap file")
              
                return False

    print('{} packets read, {} packets not written to CSV'.
          format(frame_num, ignored_packets))
    return True
#--------------------------------------------------

def check_files(pcap, csv):
    "main entry"
    if not os.path.exists(pcap):
        print('Input pcap file "{}" does not exist'.format(pcap),
              file=sys.stderr)
        return False

    if os.path.exists(csv):
        print('Output csv file "{}" already exists, '
              'won\'t overwrite'.format(csv),
              file=sys.stderr)
        return False
    return True
