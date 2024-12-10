def main(args):
    import time
    from Auth.auth_Key import ncloud_accesskey, ncloud_secretkey
    from Auth.signature import make_signature
    from send_request import send_request

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