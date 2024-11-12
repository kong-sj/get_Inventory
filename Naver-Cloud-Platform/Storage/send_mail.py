def main(args):
    import hashlib
    import hmac
    import base64
    import time
    import requests
    from auth_Key import ncloud_accesskey, ncloud_secretkey

    def	make_signature(access_key, secret_key, method, uri, timestamp):
        timestamp = str(timestamp)
        secret_key = bytes(secret_key, 'UTF-8')
        message = method + " " + uri + "\n" + timestamp + "\n" + access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest()).decode()
        return signingKey

    def send_request(url, headers, method, data):
        r = requests.request(method, url, headers=headers, json=data)
        if r.status_code != 200:
            print('ERROR! {} {}'.format(r.status_code, r.text))
        return r.text

    def send_mail(bucket_name, object_name, t, event_type):
        timestamp = int(time.time()*1000)
        host = 'https://mail.apigw.ntruss.com'
        path = '/api/v1/mails'
        method = 'POST'
        headers = {
            "Content-Type": "application/json",
            "x-ncp-apigw-timestamp": str(timestamp),
            "x-ncp-iam-access-key": ncloud_accesskey,
            "x-ncp-apigw-signature-v2": make_signature(ncloud_accesskey, ncloud_secretkey, method, path, timestamp)
        }
        body = {
          "senderAddress": "no_reply@company.com",
          "title": "alert: ${object_name}",
          "body": 'bucket: ${bucket_name} / path: ${object_name} / time: ${time} / event_type: ${event_type}',
          "recipients": [
            {
              "address": "sjhong@mz.co.kr",
              "name": "Seongjoon Hong",
              "type": "R",
              "parameters": {
                "bucket_name": bucket_name,
                "object_name": object_name,
                "time": t,
                "event_type": event_type
              }
            }
          ],
          "individual": True,
          "advertising": False
        }
        send_request(host+path, headers, method, body)

    print('data: {}'.format(str(args)))
    bucket_name = args.get("container_name", "")
    object_name  = args.get("object_name", "")
    event_type = args.get("event_type", "")

    t = args.get("timestamp_finish", "")
    send_mail(bucket_name, object_name, t, event_type)
    return args