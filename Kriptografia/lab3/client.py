import random
import socket
import json
import threading
import logging

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
import crypto

client_id = os.getpid()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind(("localhost", client_id))
client_socket.setblocking(False)
client_socket.listen(5)
peer_id = None
peer_public_key = None
peer_socket = None
private_key = None
algorithm = None
mode = None
padding = None
block_size = None
my_half = None
common_key = None
message_thread = None
sent_bye = None
my_ciphers = json.loads(open("ciphers1.json", "r").read())
long_message = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi eget elementum ipsum. Sed mollis 
elementum auctor. Aenean sollicitudin metus non mauris tristique lacinia. Aenean congue ultricies velit eget 
fermentum. Praesent at facilisis tellus. Donec feugiat semper eros id volutpat. Etiam gravida dapibus pharetra. 
Suspendisse ac eros at ex lobortis molestie. Phasellus imperdiet malesuada nisl, id faucibus nisl accumsan ut. Cras 
ullamcorper maximus mi. Etiam vehicula posuere ligula, ut venenatis diam. Ut at urna commodo, tempus libero non, 
aliquet ligula. Etiam a sapien neque. Nunc mattis aliquet placerat. Donec pulvinar non felis sed facilisis. Aenean a 
odio et massa volutpat faucibus. Donec id lacinia justo. Nam ut hendrerit quam, et bibendum diam. Suspendisse 
volutpat auctor massa, sed tempor dui lobortis ac. Vivamus volutpat enim velit, nec iaculis nunc convallis non. Sed 
pellentesque accumsan urna, et lacinia sem pharetra ac. Vivamus porttitor pharetra vehicula. Aliquam scelerisque 
tempus tortor non hendrerit. Vestibulum sit amet sapien aliquet, sodales ipsum vitae, volutpat justo. Nam posuere ut 
tortor ut egestas. Pellentesque in ornare massa. Phasellus lacinia eleifend sem id sodales.

Curabitur nibh diam, vulputate id neque commodo, interdum dapibus eros. Donec gravida massa vel dui efficitur, 
at gravida ligula varius. Nam semper elit dui, id imperdiet felis dapibus id. Suspendisse potenti. Vestibulum in 
varius magna. Proin quis fringilla leo, in posuere nibh. Quisque efficitur viverra libero, et pharetra risus bibendum 
sit amet. Aliquam laoreet justo non faucibus venenatis. Phasellus eget ullamcorper eros, quis malesuada est. Nullam 
mollis nibh tellus, eu mollis ligula faucibus a."""

logging.basicConfig(level=logging.INFO)


def generate_rsa_keypair():
    global client_id
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    logging.info(f"[{client_id}] Generated RSA keypair")
    return private_key, public_key


def register_new_public_key():
    global client_id, private_key
    private_key, public_key = generate_rsa_keypair()
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(("localhost", 5000))

    request = {
        "type": "register",
        "client_id": client_id,
        "public_key": public_key.decode("latin-1")
    }

    conn.send(json.dumps(request).encode())
    logging.info(f"[{client_id}] Registered new public key at KeyServer")
    conn.close()


def get_public_key_of_peer():
    global client_id, peer_public_key, peer_id
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(("localhost", 5000))

    request = {
        "type": "get_key",
        "client_id": peer_id
    }

    conn.send(json.dumps(request).encode())
    data = conn.recv(4096)
    response = json.loads(data.decode())
    conn.close()
    logging.info(f"[{client_id}] Got public key of client [{peer_id}]: {response["public_key"]}")
    peer_public_key = response["public_key"]
    if peer_public_key is None:
        peer_id = None


def encrypt_with_rsa(message: bytes) -> bytes:
    global peer_public_key
    rsa_key = RSA.import_key(peer_public_key.encode("latin-1"))
    cipher = PKCS1_OAEP.new(rsa_key)
    chunk_size = rsa_key.size_in_bytes() - 2 * SHA256.digest_size - 2
    chunks = [message[i:i + chunk_size] for i in range(0, len(message), chunk_size)]
    encrypted_chunks = [cipher.encrypt(chunk) for chunk in chunks]
    return b''.join(encrypted_chunks)


def decrypt_with_rsa(message: bytes) -> bytes:
    global private_key
    rsa_key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    chunks = [message[i:i + 256] for i in range(0, len(message), 256)]
    decrypted_chunks = [cipher.decrypt(chunk) for chunk in chunks]
    return b''.join(decrypted_chunks)


def encrypt_with_common_algorithm(message: bytes) -> bytes:
    global algorithm, mode, common_key, block_size
    return crypto.encrypt(message, common_key.decode("latin-1"), padding, algorithm, mode, block_size, common_key)


def decrypt_with_common_algorithm(message: bytes) -> bytes:
    global algorithm, mode, common_key, block_size
    return crypto.decrypt(message, common_key.decode("latin-1"), padding, algorithm, mode, block_size, common_key)


def receive_messages():
    global peer_id, client_socket, peer_socket, algorithm, mode, padding, block_size, my_half, common_key, sent_bye
    while peer_socket is None:
        try:
            peer_socket, _ = client_socket.accept()
        except BlockingIOError:
            pass
    while True:
        try:
            peer_socket.getpeername()
            break
        except OSError:
            pass
    while True:
        try:
            data = peer_socket.recv(65536)
            if not data:
                continue
            decrypted = decrypt_with_rsa(data) if common_key is None else decrypt_with_common_algorithm(data)
            message = json.loads(decrypted.decode())
            match message["type"]:
                case "hello":
                    peer_id = int(message["client_id"])
                    get_public_key_of_peer()
                    block_cipher_list = message["data"]
                    logging.info(f"[{client_id}] Received Hello from [{peer_id}]")
                    send_ack(block_cipher_list)
                case "ack":
                    chosen_block_cipher = message["data"]
                    logging.info(f"[{client_id}] Received Ack from [{peer_id}]")
                    algorithm = chosen_block_cipher["algorithm"]
                    mode = chosen_block_cipher["mode"]
                    padding = chosen_block_cipher["padding"]
                    block_size = chosen_block_cipher["block_size"]
                    logging.info(f"[{client_id}] Algorithm chosen: {algorithm} with {mode} mode, "
                                 f"{padding} padding and {block_size} block size")
                    if algorithm is None:
                        algorithm = "None"
                        peer_socket.close()
                        break
                case "half":
                    if my_half is None:
                        send_half_key()
                    peer_half = message["data"].encode("latin-1")
                    common_key = my_half + peer_half if client_id < peer_id else peer_half + my_half
                    logging.info(f"[{client_id}] Got half key from [{peer_id}] and chose common key")
                case "msg":
                    logging.info(f"[{client_id}] Received message from [{peer_id}]: {message["data"]}")
                case "bye":
                    message = {
                        "client_id": client_id,
                        "type": "bye"
                    }
                    if not sent_bye:
                        sent_bye = True
                        peer_socket.send(encrypt_with_common_algorithm(json.dumps(message).encode()))
                        logging.info(f"[{client_id}] Sent bye to [{peer_id}]")
                    peer_socket.close()
                    exit(0)
        except BlockingIOError:
            pass
        except ConnectionResetError:
            logging.info(f"[{client_id}] Socket connection was closed by [{peer_id}]")
            return
        except ConnectionAbortedError:
            logging.info(f"[{client_id}] Closed socket connection with [{peer_id}]")
            return


def get_public_key():
    global client_id, peer_id
    if peer_id is None:
        try:
            peer_id = int(input("ID of the other client: "))
            if peer_id == client_id:
                print("You can't ask for your own public key")
                peer_id = None
                return
            get_public_key_of_peer()
        except ValueError:
            print("Please give a number next time")


def send_hello():
    global peer_id, peer_socket, client_id, my_ciphers
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_socket.connect(("localhost", peer_id))
    message = {
        "client_id": client_id,
        "type": "hello",
        "data": my_ciphers
    }
    peer_socket.send(encrypt_with_rsa(json.dumps(message).encode()))
    logging.info(f"[{client_id}] Sent Hello to [{peer_id}]")


def send_ack(block_cipher_list):
    global peer_id, peer_socket, algorithm, mode, padding, block_size
    choose_algorithm(block_cipher_list)
    message = {
        "client_id": client_id,
        "type": "ack",
        "data": {
            "algorithm": algorithm,
            "mode": mode,
            "padding": padding,
            "block_size": block_size
        }
    }
    peer_socket.send(encrypt_with_rsa(json.dumps(message).encode()))
    if algorithm is None or algorithm == "None":
        peer_socket.close()
        exit(1)
    logging.info(f"[{client_id}] Sent Ack to [{peer_id}]")


def choose_algorithm(block_cipher_list):
    global algorithm, mode, padding, my_ciphers, block_size
    for cipher in my_ciphers:
        if cipher in block_cipher_list:
            algorithm = cipher["algorithm"]
            mode = cipher["mode"]
            padding = cipher["padding"]
            block_size = cipher["block_size"]
            break
    logging.info(f"[{client_id}] Algorithm chosen: {algorithm} with {mode} mode, "
                 f"{padding} padding and {block_size} block size")


def send_half_key():
    global client_id, peer_id, peer_socket, my_half
    my_half = bytes([random.randint(0, 255) for _ in range(8)])
    message = {
        "client_id": client_id,
        "type": "half",
        "data": my_half.decode("latin-1")
    }
    peer_socket.send(encrypt_with_rsa(json.dumps(message).encode()))
    logging.info(f"[{client_id}] Sent half key to [{peer_id}]")


def send_message_to_peer():
    global peer_id, peer_socket, algorithm, common_key, long_message
    if peer_id is None:
        return
    if peer_socket is None:
        send_hello()
    while algorithm is None:
        pass
    if algorithm == "None":
        exit(1)
    if common_key is None:
        send_half_key()
    while common_key is None:
        pass

    # data = input("Your message: ")
    message = {
        "client_id": client_id,
        "type": "msg",
        "data": long_message
    }
    peer_socket.send(encrypt_with_common_algorithm(json.dumps(message).encode()))
    logging.info(f"[{client_id}] Sent message to [{peer_id}]")


def send_bye():
    global client_id, peer_id, peer_socket, sent_bye
    if peer_socket is None:
        return
    message = {
        "client_id": client_id,
        "type": "bye"
    }
    peer_socket.send(encrypt_with_common_algorithm(json.dumps(message).encode()))
    sent_bye = True
    logging.info(f"[{client_id}] Sent bye to [{peer_id}]")


def main():
    global peer_id, message_thread, sent_bye
    register_new_public_key()
    threading.Thread(target=receive_messages).start()
    while True:
        if sent_bye:
            break
        print("Choose an option", flush=True)
        print("1. Register new public key")
        if peer_id is None:
            print("2. Get public key of another client")
        if peer_id is not None:
            print(f"3. Send message to client [{peer_id}]")
        print("0. Exit")
        print("Any other input will refresh the options")
        try:
            option = input("Choose an option: ")
        except ValueError:
            break
        if sent_bye:
            break
        match option:
            case "1":
                register_new_public_key()
            case "2":
                get_public_key()
            case "3":
                try:
                    send_message_to_peer()
                except OSError:
                    break
            case "0":
                try:
                    send_bye()
                except OSError:
                    break
                break


if __name__ == "__main__":
    main()
