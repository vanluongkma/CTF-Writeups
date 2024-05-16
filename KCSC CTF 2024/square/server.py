from os import urandom
from aes import AES
import socket
import threading

flag = 'KCSC{s0m3_r3ad4ble_5tr1ng_like_7his}'

menu = ('\n\n|---------------------------------------|\n' +
            '| Welcome to KCSC Square!               |\n' +
            '| I know it\'s late now but              |\n' +
            '| Happy Reunification Day :D            |\n' +
            '|---------------------------------------|\n' +
            '| [1] Get ciphertext                    |\n' +
            '| [2] Guess key ^__^                    |\n' +
            '| [3] Quit X__X                         |\n' +
            '|---------------------------------------|\n')

bye = ( '[+] Closing Connection ..\n'+
        '[+] Bye ..\n')

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        key = urandom(16)
        chal = AES(key)
        client.send(menu.encode())
        for i in range(8888):
            try:
                client.send(b'> ')
                choice = client.recv(size).strip()
                if choice == b'1':
                    client.send(b'Plaintext in hex: ')
                    hex_pt = client.recv(size).strip().decode()
                    try:
                        pt = bytes.fromhex(hex_pt)
                        assert len(pt) == 16
                    except:
                        client.send(b'Something wrong in your plaintext' + b'\n')
                        continue
                    client.send(chal.encrypt(pt).hex().encode() + b'\n')
                elif choice == b'2':
                    client.send(b'Key in hex: ')
                    hex_key = client.recv(size).strip().decode()
                    try:
                        guess_key = bytes.fromhex(hex_key)
                        assert guess_key == key
                    except:
                        client.send(b'Wrong key, good luck next time =)))' + b'\n')
                        client.close()
                    client.send(b'Nice try, you got it :D!!!! Here is your flag: ' + flag.encode() + b'\n')
                    client.close()
                elif choice == b'3':
                    client.send(bye.encode())
                    client.close()
                else:
                    client.send(b'Invalid choice!!!!\n')
                    client.close()
            except:
                client.close()
                return False
        client.send(b'No more rounds\n')
        client.close()

if __name__ == "__main__":
    ThreadedServer('',2004).listen()