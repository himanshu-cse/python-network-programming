import socket
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

target = "127.0.0.1"
port = 8000
path = "/"

total_requests = 1000
workers = 10
timeout = 3

lock = threading.Lock()
success = 0
failed = 0

def send_request():
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {target}:{port}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode("ascii")

    with socket.create_connection((target, port), timeout=timeout) as sock:
        sock.sendall(request)
        return sock.recv(1024)


def worker():
    global success, failed

    try:
        send_request()
        with lock:
            success += 1
    except OSError as exc:
        with lock:
            failed += 1
        print(f"Request failed: {exc}")


with ThreadPoolExecutor(max_workers=workers) as executor:
    futures = [executor.submit(worker) for _ in range(total_requests)]

    for future in as_completed(futures):
        future.result()

print(f"Done. Successful: {success}, Failed: {failed}")