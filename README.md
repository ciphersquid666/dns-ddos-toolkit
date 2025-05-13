# Adaptive DNS DDoS Toolkit ⚡️🌐

<p align="center">
  <img src="https://media0.giphy.com/media/5YcpdtrcwIARW/100.gif?cid=6c09b952hhbwxg3a8lmou4ls26k0j2kf5wqgh3tjngqbwoil&ep=v1_gifs_search&rid=100.gif&ct=g" alt="Toolkit DDoS GIF">
</p>

A flexible and adaptive toolkit for performing DNS-based DDoS attacks, with various attack types including DNS Flood, DNS Amplification, NXDOMAIN, DNS Hijacking, and DRDoS. This tool is intended for educational and testing purposes only on systems where you have explicit permission.

**Author**: Teleguard ID THMYULYWN  
**Repository**: [https://github.com/ciphersquid666/dns-ddos-toolkit](https://github.com/ciphersquid666/dns-ddos-toolkit)

---

## Features 🌟
- **Multiple Attack Types**: Choose from DNS Flood, DNS Amplification, NXDOMAIN, DNS Hijacking, or DRDoS.
- **Customizable Options**: Adjust target IP, duration, attack type, and more.
- **Intelligent Monitoring**: Analyze the vulnerability of your target in real-time with packet loss and latency checks.
- **Multi-threading**: Perform the attack with multiple threads for higher efficiency.

## Installation 🛠️

### Requirements 📦

To run this script, you need the following Python libraries:

- `scapy`: For crafting network packets.
- `termcolor`: For colored terminal output.
- `numpy`: For calculating latency statistics.

### Install Dependencies 📥

1. Clone the repository:

   ```bash
   git clone https://github.com/ciphersquid666/dns-ddos-toolkit.git
   cd dns-ddos-toolkit
Install the required dependencies:
bash
pip install -r requirements.txt
After installing the dependencies, you're all set to start the tool! 🎉
Run the Tool 🏃‍♂️
Once everything is set up, you can start the attack with the following command:
bash
python3 ddos_toolkit.py <attack_type> <target_ip> [options]
Replace <attack_type> with one of the available options (dns_amplification, dns_flood, nxdomain, dns_hijacking, or drdos) and <target_ip> with the target IP address.
Example Command 💡
To run a DNS Flood attack on the target IP 192.168.1.1:
bash
python3 ddos_toolkit.py dns_flood 192.168.1.1
Available Options ⚙️
attack_type: The attack type, which can be one of the following: dns_amplification, dns_flood, nxdomain, dns_hijacking, or drdos.
--target-port: Specify the port for the attack (default is 53).
--duration: Duration of the attack in seconds (default is 60 seconds).
--threads: Number of threads for the attack (default is 10 threads).
--dns-server: DNS server used for DNS Amplification or DRDoS (default is 8.8.8.8).
--fake-ip: Fake IP address for hijacking attacks (default is 192.168.1.100).
--no-spoofing: Disable IP spoofing (useful for testing on Android).
Disclaimer ⚠️
This toolkit is NOT intended for malicious use. Ensure you have explicit permission to perform any kind of security testing on the target systems. Unauthorized usage may lead to legal consequences.
License 📄
This project is licensed under the MIT License. See the LICENSE file for more information.
If you have any questions or need further assistance, feel free to create an issue on the GitHub repository! 🚀

### Notes
- The content is based on the provided `README.md`, with the repository URL updated to `https://github.com/ciphersquid666/dns-ddos-toolkit`.
- Added the author information (Teleguard ID THMYULYWN) at the top, as requested.
- Ensured proper Markdown formatting for GitHub, including a clickable link for the repository and the LICENSE file.
- The file is ready to be copied and pasted into the `README.md` of the repository.

