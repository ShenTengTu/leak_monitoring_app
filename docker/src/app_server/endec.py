import logging
import binascii
import base64
import json
import x_msgpack

logger = logging.getLogger("app_server")


def bin_to_hex(b: bytes, sep: str = ":"):
    n = len(b)
    if n == 1:
        return f"0x{b.hex()}"
    return sep.join(b[i : i + 1].hex() for i in range(n - 1))


class _JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return bin_to_hex(obj)
        return json.JSONEncoder.default(self, obj)


_json_encoder = _JSONEncoder()


class Decode:
    @staticmethod
    def base64(s: str):
        """Base64 string to binary. Return None if decode failed."""
        try:
            return base64.standard_b64decode(s)
        except binascii.Error:
            return None

    @staticmethod
    def x_msgpack(b: bytes):
        return x_msgpack.deserialize(b)


class Encode:
    @staticmethod
    def json(obj):
        return _json_encoder.encode(obj)
