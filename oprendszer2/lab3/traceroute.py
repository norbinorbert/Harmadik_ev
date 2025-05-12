import argparse
import socket
import time
from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr1


# convert ip to hostname
def get_hostname(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return f" ({hostname})" if hostname else " ()"
    except (socket.herror, socket.gaierror):
        return " ()"


def traceroute(target, max_hops, timeout):
    print(f"Tracing route to {target} over a maximum of {max_hops} hops.")

    # send packets with increasing ttl
    for ttl in range(1, max_hops + 1):
        packet = IP(dst=target, ttl=ttl) / ICMP()

        start_time = time.time()
        reply = sr1(packet, timeout=timeout, verbose=0)
        elapsed_ms = (time.time() - start_time) * 1000

        if reply is None:
            print(f"{ttl}. * Request timed out.")
            continue
        elif reply.type == 0:  # Echo Reply
            print(f"{ttl}. {elapsed_ms:.0f}ms {reply.src}{get_hostname(reply.src)}")
            print(f"Reached destination at {reply.src}")
            break
        elif reply.type == 11:  # Time to Live exceeded in Transit
            print(f"{ttl}. {elapsed_ms:.0f}ms {reply.src}{get_hostname(reply.src)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trace the route to a network host.")
    parser.add_argument("target_name", help="Target hostname or IP address")
    parser.add_argument("-m", type=int, default=30,
                        help="Maximum number of hops to search for target.")
    parser.add_argument("-w", type=int, default=4000,
                        help="Wait timeout milliseconds for each reply.")

    args = parser.parse_args()

    timeout_sec = args.w / 1000

    traceroute(args.target_name, max_hops=args.m, timeout=timeout_sec)
