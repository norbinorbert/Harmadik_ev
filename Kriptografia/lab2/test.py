import json
import crypto

# load config
config = json.load(open("config.json", "r"))
block_size = 16
key = config["key"]
iv = config["iv"].encode("utf-8")
padding = config["padding"]
file_name = config["file_name"]
file_extension = file_name.split('.')[1]

# read input and add padding
input_file = open(file_name, "rb")
data = input_file.read()
data = getattr(crypto, padding)(data, block_size)
padding = "remove_" + padding

# encrypt using desired mode
result = crypto.ecb(data, key, "AES", block_size, True, iv)
# decrypt
result = crypto.ecb(result, key, "AES", block_size, False, iv)
# remove the padding
result = getattr(crypto, padding)(result)
# output result after the encrypt + decrypt operation
output_file = open("output_ecb_AES." + file_extension, "wb")
output_file.write(result)

# encrypt using desired mode
result = crypto.cbc(data, key, "AES", block_size, True, iv)
# decrypt
result = crypto.cbc(result, key, "AES", block_size, False, iv)
# remove the padding
result = getattr(crypto, padding)(result)
# output result after the encrypt + decrypt operation
output_file = open("output_cbc_AES." + file_extension, "wb")
output_file.write(result)

# encrypt using desired mode
result = crypto.cfb(data, key, "AES", block_size, True, iv)
# decrypt
result = crypto.cfb(result, key, "AES", block_size, False, iv)
# remove the padding
result = getattr(crypto, padding)(result)
# output result after the encrypt + decrypt operation
output_file = open("output_cfb_AES." + file_extension, "wb")
output_file.write(result)

# encrypt using desired mode
result = crypto.ofb(data, key, "AES", block_size, True, iv)
# decrypt
result = crypto.ofb(result, key, "AES", block_size, False, iv)
# remove the padding
result = getattr(crypto, padding)(result)
# output result after the encrypt + decrypt operation
output_file = open("output_ofb_AES." + file_extension, "wb")
output_file.write(result)

# encrypt using desired mode
result = crypto.ctr(data, key, "AES", block_size, True, iv)
# decrypt
result = crypto.ctr(result, key, "AES", block_size, False, iv)
# remove the padding
result = getattr(crypto, padding)(result)
# output result after the encrypt + decrypt operation
output_file = open("output_ctr_AES." + file_extension, "wb")
output_file.write(result)

block_size = config["block_size"] // 8
# encrypt using desired mode
result = crypto.ecb(data, key, "vigenere", block_size, True, iv)
# decrypt
result = crypto.ecb(result, key, "vigenere", block_size, False, iv)
# remove the padding
result = getattr(crypto, padding)(result)
# output result after the encrypt + decrypt operation
output_file = open("output_ecb_vigenere." + file_extension, "wb")
output_file.write(result)

# encrypt using desired mode
result = crypto.cbc(data, key, "vigenere", block_size, True, iv)
# decrypt
result = crypto.cbc(result, key, "vigenere", block_size, False, iv)
# remove the padding
result = getattr(crypto, padding)(result)
# output result after the encrypt + decrypt operation
output_file = open("output_cbc_vigenere." + file_extension, "wb")
output_file.write(result)

# encrypt using desired mode
result = crypto.cfb(data, key, "vigenere", block_size, True, iv)
# decrypt
result = crypto.cfb(result, key, "vigenere", block_size, False, iv)
# remove the padding
result = getattr(crypto, padding)(result)
# output result after the encrypt + decrypt operation
output_file = open("output_cfb_vigenere." + file_extension, "wb")
output_file.write(result)

# encrypt using desired mode
result = crypto.ofb(data, key, "vigenere", block_size, True, iv)
# decrypt
result = crypto.ofb(result, key, "vigenere", block_size, False, iv)
# remove the padding
result = getattr(crypto, padding)(result)
# output result after the encrypt + decrypt operation
output_file = open("output_ofb_vigenere." + file_extension, "wb")
output_file.write(result)

# encrypt using desired mode
result = crypto.ctr(data, key, "vigenere", block_size, True, iv)
# decrypt
result = crypto.ctr(result, key, "vigenere", block_size, False, iv)
# remove the padding
result = getattr(crypto, padding)(result)
# output result after the encrypt + decrypt operation
output_file = open("output_ctr_vigenere." + file_extension, "wb")
output_file.write(result)
