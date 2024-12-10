import socket
import threading
import json
import logging

public_keys = {}
logging.basicConfig(level=logging.INFO)


def handle_client(conn, addr):
    logging.info(f"[KeyServer] Client connected: {addr}")
    data = conn.recv(4096)
    request = json.loads(data.decode())

    if request["type"] == "register":
        public_keys[request["client_id"]] = request["public_key"]
        logging.info(f"[KeyServer] Registered new public key for client [{request["client_id"]}]")
    elif request["type"] == "get_key":
        response = {
            "public_key": public_keys.get(request["client_id"], None)
        }
        logging.info(f"[KeyServer] Sent public key of [{request["client_id"]}] to another client")
        conn.send(json.dumps(response).encode())

    conn.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 5000))
    server.listen(5)
    logging.info("[KeyServer] Listening on localhost:5000")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    start_server()
