import json
from Crypto.Cipher import AES


# padding modes
def zero_padding(data: bytes, block_size: int) -> bytes:
    return data + b"\x00" * (block_size - len(data) % block_size)


def remove_zero_padding(data: bytes) -> bytes:
    return data.rstrip(b"\x00")


def des_padding(data: bytes, block_size: int) -> bytes:
    padding_len = block_size - len(data) % block_size
    return data + b"\x01" + b"\x00" * (padding_len - 1)


def remove_des_padding(data: bytes) -> bytes:
    return data.rstrip(b"\x00").rstrip(b"\x01")


def schneier_padding(data: bytes, block_size: int) -> bytes:
    padding_len = block_size - len(data) % block_size
    return data + bytes([padding_len] * padding_len)


def remove_schneier_padding(data: bytes) -> bytes:
    padding_len = data[-1]
    return data[:-padding_len]


# encrypt modes
def ecb(data: bytes, key: str, algorithm: str, block_size: int, encrypt: bool, iv: bytes) -> bytes:
    global functions
    if algorithm == "AES":
        cipher = AES.new(key.encode("utf-8"), AES.MODE_ECB)
        return cipher.encrypt(data) if encrypt else cipher.decrypt(data)

    algorithm = algorithm + "_encrypt" if encrypt else algorithm + "_decrypt"
    result = [0] * len(data)
    for i in range(0, len(data), block_size):
        result[i:i + block_size] = functions[algorithm](data[i:i + block_size], key)
    return bytes(result)


def cbc(data: bytes, key: str, algorithm: str, block_size: int, encrypt: bool, iv: bytes) -> bytes:
    global functions
    if algorithm == "AES":
        cipher = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv)
        return cipher.encrypt(data) if encrypt else cipher.decrypt(data)

    algorithm = algorithm + "_encrypt" if encrypt else algorithm + "_decrypt"
    result = [0] * len(data)
    for i in range(0, len(data), block_size):
        result[i:i + block_size] = functions[algorithm](bytes(a ^ b for a, b in zip(data[i:i + block_size], iv)), key) \
            if encrypt else bytes(a ^ b for a, b in zip(functions[algorithm](data[i:i + block_size], key), iv))
        iv = bytes(result[i:i + block_size]) if encrypt else bytes(data[i:i + block_size])
    return bytes(result)


def cfb(data: bytes, key: str, algorithm: str, block_size: int, encrypt: bool, iv: bytes) -> bytes:
    global functions
    if algorithm == "AES":
        cipher = AES.new(key.encode("utf-8"), AES.MODE_CFB, iv)
        return cipher.encrypt(data) if encrypt else cipher.decrypt(data)

    algorithm = algorithm + "_encrypt"
    result = [0] * len(data)
    for i in range(0, len(data), block_size):
        result[i:i + block_size] = bytes(a ^ b for a, b in zip(functions[algorithm](iv, key), data[i:i + block_size]))
        iv = bytes(result[i:i + block_size]) if encrypt else bytes(data[i:i + block_size])
    return bytes(result)


def ofb(data: bytes, key: str, algorithm: str, block_size: int, encrypt: bool, iv: bytes) -> bytes:
    global functions
    if algorithm == "AES":
        cipher = AES.new(key.encode("utf-8"), AES.MODE_OFB, iv)
        return cipher.encrypt(data) if encrypt else cipher.decrypt(data)

    algorithm = algorithm + "_encrypt"
    result = [0] * len(data)
    for i in range(0, len(data), block_size):
        output = functions[algorithm](iv, key)
        result[i:i + block_size] = bytes(a ^ b for a, b in zip(output, data[i:i + block_size]))
        iv = output
    return bytes(result)


def ctr(data: bytes, key: str, algorithm: str, block_size: int, encrypt: bool, iv: bytes) -> bytes:
    global functions
    if algorithm == "AES":
        cipher = AES.new(key.encode("utf-8"), AES.MODE_CTR, nonce=iv[0:8])
        return cipher.encrypt(data) if encrypt else cipher.decrypt(data)

    algorithm = algorithm + "_encrypt"
    result = [0] * len(data)
    for i in range(0, len(data), block_size):
        counter = int.from_bytes(iv) + (i // block_size)
        n = counter.to_bytes(len(iv))
        result[i:i + block_size] = bytes(a ^ b for a, b in zip(functions[algorithm](n, key), data[i:i + block_size]))
    return bytes(result)


# custom algorithms
def vigenere_encrypt(data: bytes, key: str) -> bytes:
    key = (key * (len(data) // len(key) + 1))[0:len(data)]
    return bytes((byte + ord(key_char)) % 256 for byte, key_char in zip(data, key))


def vigenere_decrypt(data: bytes, key: str) -> bytes:
    key = (key * (len(data) // len(key) + 1))[0:len(data)]
    return bytes((byte - ord(key_char)) % 256 for byte, key_char in zip(data, key))


def main():
    global functions
    # load config
    config = json.load(open("config.json", "r"))
    block_size = config["block_size"] // 8
    algorithm = config["algorithm"]
    # for AES, block_size needs to be 16 bytes (128 bits)
    if algorithm == "AES":
        block_size = 16
    key = config["key"]
    mode = config["mode"]
    iv = config["iv"].encode("utf-8")
    padding = config["padding"]
    file_name = config["file_name"]
    # read input and add padding
    input_file = open(file_name, "rb")
    data = input_file.read()
    input_file.close()
    data = functions[padding](data, block_size)

    # encrypt using desired mode
    result = functions[mode](data, key, algorithm, block_size, True, iv)
    # decrypt
    result = functions[mode](result, key, algorithm, block_size, False, iv)

    # remove the padding
    padding = "remove_" + padding
    result = functions[padding](result)

    # output result after the encrypt + decrypt operation
    file_extension = file_name.split('.')[1]
    output_file = open("output." + file_extension, "wb")
    output_file.write(result)
    output_file.close()


functions = locals()
if __name__ == "__main__":
    main()
