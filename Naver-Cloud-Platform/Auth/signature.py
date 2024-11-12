import hashlib
import hmac
import base64

def	make_signature(access_key, secret_key, method, uri, timestamp):
    timestamp = str(timestamp)
    secret_key = bytes(secret_key, 'UTF-8')
    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest()).decode()
    return signingKey