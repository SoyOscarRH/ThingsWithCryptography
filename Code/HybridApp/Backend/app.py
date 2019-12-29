import json
import base64

from hashlib import sha256
from secrets import token_bytes
from rsa import RSA
from aes import AES
from flask import Flask, flash, jsonify, redirect, render_template, request

codes = {
    "n": "GFD",
    "key": "BCD",
    "message": "DAF",
    "iv": "GFA",
    "sign": "CGB",
    "text": "ABW",
    "privateKey": "XWT",
    "publicKey": "SHW",
    "doingStuff": "SHJ",
    "doingSign": "SKQ",
    "modPublic": "OPE",
    "modPrivate": "PQE",
    "public": "YEE",
    "private": "PEE",
}


def from_str_to_bytes(text): return text.encode("utf-8")


def from_bytes_to_str(blob): return str(blob, "utf-8")


def from_str_to_bytes_aes(text): return base64.b64decode(text.encode("utf8"))


def from_bytes_to_str_aes(blob): return base64.b64encode(blob).decode("utf8")


templates, static = "../FrontEnd", "../FrontEnd/Distribution"
app = Flask(__name__, static_folder=static, template_folder=templates)


@app.route('/get_keys')
def get_keys():
    solver = RSA()
    private, public = str(solver.private_key), str(solver.public_key)
    return jsonify({codes['n']: str(solver.n), codes['privateKey']: private, codes['publicKey']: public})


@app.route('/createCipher', methods=["POST"])
def create_cipher():
    try:
        # Create AES key
        random_key = token_bytes(16)
        init_vector = token_bytes(16)

        machine = AES(random_key)

        # Get data
        data: dict = request.json
        text = str(data.get(codes['text']))

        # Encode text using AES
        solver = RSA(empty_value=True)
        message, key, iv = text, "0", "0"
        if data.get(codes["doingStuff"]):
            message = machine.encrypt_cbc(from_str_to_bytes(text), init_vector)
            message = from_bytes_to_str_aes(message)

            # Prepare RSA for encrypt the key
            solver.n = int(data.get(codes["modPublic"]))
            solver.public_key = int(data.get(codes["public"]))

            # Do RSA
            key = solver.encrypt(from_bytes_to_str_aes(random_key))
            key = [str(c) for c in key]

            iv = solver.encrypt(from_bytes_to_str_aes(init_vector))
            iv = [str(c) for c in iv]

        # sign the thing
        sign = "0"
        if data.get(codes["doingSign"]):
            # Prepare RSA for encrypt the sign
            solver.n = int(data.get(codes["modPrivate"]))
            solver.public_key = int(data.get(codes["private"]))

            text = data.get(codes["text"]).encode('utf-8')
            raw_sign = str(sha256(text).hexdigest())
            sign = solver.encrypt(raw_sign)
            sign = [str(c) for c in sign]

        return jsonify({codes["message"]: message, codes["key"]: key, codes["iv"]: iv, codes["sign"]: sign})

    except Exception as e:
        print(e)
        return jsonify({"error": "Error ciphering the message :c"})


@app.route('/destroyCipher', methods=["POST"])
def destroy_cipher():
    try:
        # Get data
        data: dict = request.json

        # Prepare RSA for decrypt the key
        solver = RSA(empty_value=True)
        key, iv = "0", "0"
        if (data.get(codes["key"]) != "0"):
            solver.n = int(data.get(codes["modPrivate"]))
            solver.private_key = int(data.get(codes["private"]))

            # Decode key, iv using RSA
            key = solver.decrypt([int(c) for c in data.get(codes["key"])])
            iv = solver.decrypt([int(c) for c in data.get(codes["iv"])])

            key = from_str_to_bytes_aes(key)
            iv = from_str_to_bytes_aes(iv)

    except Exception as e:
        print(e)
        return jsonify({"error": "Error decrypting the key :c 1"})
    try:
        message = data.get(codes["text"])
        if (data.get(codes["key"]) != "0"):
            # Prepare AES
            machine = AES(key)

            # Decode message using AES
            blob = from_str_to_bytes_aes(data.get(codes["text"]))

            message = machine.decrypt_cbc(blob, iv)
            message = from_bytes_to_str(message)

    except Exception as e:
        print(e)
        return jsonify({"error": "Error decrypting the message :c 2"})
    try:
        if (data.get(codes["sign"]) != "0"):

            # Prepare RSA for decrypt the sign
            solver.n = int(data.get(codes["modPublic"]))
            solver.private_key = int(data.get(codes["public"]))

            # Check sign
            sign = solver.decrypt([int(c) for c in data.get(codes["sign"])])
            assert(sign == str(sha256(message.encode('utf-8')).hexdigest()))

        return jsonify({codes["message"]: message})

    except Exception as e:
        print(e)
        return jsonify({"error": "Error cheking the sign of the message :c 3"})


@app.route('/')
def index(): return render_template('index.html')


if __name__ == '__main__':
    app.run()
