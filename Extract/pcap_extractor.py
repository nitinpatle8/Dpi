# #!/usr/bin/python
# from __future__ import print_function
# import sys
# import scapy
# from scapy.all import *
# import io
# import os
# from os import path

# REPORTING_TIME=10
# OUTPUT_FILE_NAME="pcap_stats_per_"+str(REPORTING_TIME)+"sec.csv"
# report_count=0

# class PktStats:
#     def reset_interval_stats(self):
#         self.tx_bytes = 0
#         self.rx_bytes = 0
#         self.tx_pkts = 0
#         self.rx_pkts = 0
#         self.tx_Bps = 0
#         self.rx_Bps = 0
#         self.start_time = 0
#         self.end_time = 0

#     def __init__(self):
#         self.reset_interval_stats()

#     def set_local_ip(self, ip):
#         print("Local IP: {}".format(ip))
#         self.local_ip = ip

#     def get_pkt_direction(self, pkt):
#         if (pkt[IP].src == self.local_ip):
#             return 0#uplink
#         else:
#             return 1#downlink

#     def update_pkt_stats(self, pkt):
#         if TCP in pkt:
#             pkt_bytes = len(pkt[TCP].payload)
#         elif UDP in pkt:
#             pkt_bytes = len(pkt[UDP].payload)
#         else:
#             print("Non TCP/UDP packet found")
#             return

#         pkt_direction = self.get_pkt_direction(pkt)

#         if pkt_direction == 0: #UPLINK
#             self.tx_bytes += pkt_bytes
#             self.tx_pkts  += 1
#         else:
#             self.rx_bytes += pkt_bytes
#             self.rx_pkts  += 1

#         if self.start_time == 0:
#             self.start_time = pkt.time

#         self.end_time = pkt.time

#     def update_interval_stats(self):
#         self.tx_Bps = self.tx_bytes / REPORTING_TIME #byte per second
#         self.rx_Bps = self.rx_bytes / REPORTING_TIME #byte per second

#     def show(self):
#         global report_count
#         report_count += 1
#         print("{} {} {} : Tx Bytes {}, Tx Pkts {}, Rx Bytes {}, Rx Pkts {}".format(report_count, self.start_time, self.end_time, self.tx_bytes, self.tx_pkts, self.rx_bytes, self.rx_pkts))

# pkt_stats = PktStats()

# class StatsWriter:
#     def write_header(self):
#         header='filename,protocol,'

#         if self.write_tx_pkts:
#             header+='tx_pkts,'
#         if self.write_rx_pkts:
#             header+='rx_pkts,'
#         if self.write_tx_bytes:
#             header+='tx_bytes,'
#         if self.write_rx_bytes:
#             header+='rx_bytes,'
#         if self.write_tx_Bps:
#             header+='tx_Bps,'
#         if self.write_rx_Bps:
#             header+='rx_Bps,'

#         self.fd.write(header)

#     def __init__(self, fname):
#         self.fd = io.open(fname, 'w', encoding='utf8')
#         self.write_tx_pkts = 0
#         self.write_tx_bytes = 0
#         self.write_tx_Bps = 0 #Bytes Per Second
#         self.write_rx_pkts = 0
#         self.write_rx_bytes = 0
#         self.write_rx_Bps = 1 #Bytes Per Second
#         self.write_header()

#     def start_new_record(self, pcap_name, protocol):
#         record = '\n' + pcap_name + "," + protocol + ","
#         self.fd.write(record)

#     def update_interval_data(self, interval_stats):
#         record = ""

#         if self.write_tx_pkts:
#             record += "{},".format(interval_stats.tx_pkts)
#         if self.write_rx_pkts:
#             record += "{},".format(interval_stats.rx_pkts)
#         if self.write_tx_bytes:
#             record += "{},".format(interval_stats.tx_bytes)
#         if self.write_rx_bytes:
#             record += "{},".format(interval_stats.rx_bytes)
#         if self.write_tx_Bps:
#             record += "{},".format(interval_stats.tx_Bps)
#         if self.write_rx_Bps:
#             record += "{},".format(interval_stats.rx_Bps)
        
#         #record+="\n"

#         self.fd.write(record)

# csv_writer = StatsWriter(OUTPUT_FILE_NAME)

# def show_progress_bar(current, total):
#     print("\rProcessing: {} / {}".format(current, total), end="")

# def measure_stats(pkt):
#     pkt_stats.update_pkt_stats(pkt)

# def report_stats():#
#     pkt_stats.update_interval_stats()
#     #pkt_stats.show()
#     csv_writer.update_interval_data(pkt_stats)
#     pkt_stats.reset_interval_stats()

# def extract_features(pcap_name):
#     pkt_count = 0
#     print("Reading pcap file {}, wait for a while".format(pcap_name))
#     pkts = rdpcap(pcap_name)
#     total_pkts = len(pkts)

#     print("summary: pkts {}, duration= {}, total pkts={}".format(len(pkts), pkts[len(pkts)-1].time - pkts[0].time, total_pkts))

#     start_time = pkts[0].time
#     next_report_time = start_time + REPORTING_TIME

#     if TCP in pkts[0]:
#         protocol = TCP
#     elif UDP in pkts[0]:
#         protocol = UDP
#     else:
#         print("Pcap with unknown protocol, skipping {}".format(pcap_name))
#         return

#     csv_writer.start_new_record(pcap_name, protocol)
#     pkt_stats.reset_interval_stats()
#     local_ip = (pkts[0])[IP].src #treat first pkt as uplink pkt
#     pkt_stats.set_local_ip(local_ip)
        
#     for pkt in pkts:
#         pkt_count += 1

#         while pkt.time > next_report_time:
#     #        print("Time to report: {} {}".format(pkt.time, next_report_time))
#             report_stats()
#             next_report_time += REPORTING_TIME

#         measure_stats(pkt)
#         show_progress_bar(pkt_count, total_pkts)

# #        if (pkt_count == 1):
# #            break;
#     print("\n, completed processing of {}".format(pcap_name))

# def process_pcaps_in_dir(dir_name):
#     files = os.listdir(dir_name)

#     total_files = len(files)
#     done_count = 0
#     print("total files in the directory: {}".format(total_files))

#     os.chdir(dir_name)
#     for pcap in files:
#         done_count+=1
#         if pcap.endswith('.pcap') or pcap.endswith('.pcapng'):
#             print("File: {} ({}/{})".format(pcap, done_count, total_files))
#             extract_features(pcap)

# if __name__ == "__main__":
#     pcap_or_dir_name = sys.argv[1]   

#     if path.isfile(pcap_or_dir_name): 
#         extract_features(pcap_or_dir_name)

#     elif path.isdir(pcap_or_dir_name):
#         process_pcaps_in_dir(pcap_or_dir_name)

#     else:
#         print("File/Directory not found: {}".format(pcap_or_dir_name))

#     print("Outputfile created: {}".format(OUTPUT_FILE_NAME))
