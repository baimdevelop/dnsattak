import socket
import random

# Fungsi untuk membuat permintaan DNS
def create_dns_request():
    transaction_id = random.randint(0, 65535)
    flags = 0x0100  # Standar Query
    questions = 1
    answer_rrs = 0
    authority_rrs = 0
    additional_rrs = 0
    query_name = b'\x03www\x06google\x03com\x00'  # www.google.com
    query_type = 1  # A record
    query_class = 1  # IN class

    dns_request = (
        transaction_id.to_bytes(2, byteorder='big') +
        flags.to_bytes(2, byteorder='big') +
        questions.to_bytes(2, byteorder='big') +
        answer_rrs.to_bytes(2, byteorder='big') +
        authority_rrs.to_bytes(2, byteorder='big') +
        additional_rrs.to_bytes(2, byteorder='big') +
        query_name +
        query_type.to_bytes(2, byteorder='big') +
        query_class.to_bytes(2, byteorder='big')
    )
    return dns_request

def send_dns_request(server_ip, port=53, num_requests=10):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)  # Set timeout untuk koneksi

    server_up = False  # Menandakan apakah server aktif atau tidak

    for i in range(num_requests):
        request = create_dns_request()
        sock.sendto(request, (server_ip, port))

        try:
            response, _ = sock.recvfrom(1024)
            print(f"Received {len(response)} bytes from {server_ip} (Request {i + 1})")
            server_up = True  # Jika berhasil menerima respons, server aktif
        except socket.timeout:
            print(f"Request {i + 1} timed out")

    sock.close()

    if server_up:
        print(f"Server {server_ip} is up and responding.")
    else:
        print(f"Server {server_ip} is down or not responding.")

if __name__ == "__main__":
    # Meminta input dari pengguna
    server_ip = input("Masukkan IP server DNS yang akan diuji: ")
    num_requests = int(input("Masukkan jumlah permintaan yang akan dikirim: "))

    send_dns_request(server_ip, num_requests=num_requests)
