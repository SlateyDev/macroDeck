import errno
import select
import socket


class TCPClient:
    def __init__(self):
        # 0 = disconnected
        # 1 = start connect
        # 2 = connect in progress
        # 3 = connection established
        # 4 = connected
        self.host = ""
        self.port = 0
        self.connect_state = 0
        self.attempt_connect = False
        self.last_retrieved_state = 0
        self.not_connected_error = ""
        self.socket: socket.socket = None

    def connect(self, host: str, port: int):
        if self.connect_state != 0:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket = None
            self.connect_state = 0
        self.host = host
        self.port = port
        self.attempt_connect = True

    def process(self):
        if self.attempt_connect and self.connect_state == 0:
            self.attempt_connect = False
            self.connect_state = 1
        elif self.connect_state == 1:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setblocking(False)
            err = self.socket.connect_ex((self.host, self.port))
            if err == errno.EINPROGRESS:
                self.connect_state = 2
            else:
                print(err, errno.errorcode[err])
                self.not_connected_error = f"{err} - {errno.errorcode[err]}"
                self.connect_state = 0
                self.socket = None
        elif self.connect_state == 2:
            # check if socket is ready
            _, writable, _ = select.select([], [self.socket], [], 0)
            if writable:
                err = self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
                if err:
                    print(err, errno.errorcode[err])
                    self.not_connected_error = f"{err} - {errno.errorcode[err]}"
                    self.connect_state = 0
                    self.socket = None
                else:
                    print("connected")
                    self.socket.send(b"GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n")
                    self.connect_state = 3
        elif self.connect_state == 3:
            self.connect_state = 4
        elif self.connect_state == 4:
            readable, _, _ = select.select([self.socket], [], [], 0)
            for read_socket in readable:
                #print("reading data")
                read_data = read_socket.recv(16384)
                if len(read_data):
                    pass
                    #print(read_data)
                else:
                    print("connection closed")
                    err = self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
                    if err:
                        print(err, errno.errorcode[err])
                        self.not_connected_error = f"{err} - {errno.errorcode[err]}"
                    try:
                        self.socket.shutdown(socket.SHUT_RDWR)
                    except OSError:
                        pass
                    self.connect_state = 0
                    self.socket = None

        if self.last_retrieved_state != self.connect_state:
            self.last_retrieved_state = self.connect_state
            return True

        return False

    def close(self):
        self.socket.shutdown(socket.SHUT_RDWR)
