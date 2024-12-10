import os

import client


def main():
    client.register_new_public_key()
    client.get_public_key()
    client.get_public_key()
    client.register_new_public_key()
    client.get_public_key()


if __name__ == "__main__":
    main()
