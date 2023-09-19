import socket, base64
from urllib import request

CRLF = "\r\n"

def part1():
    target_host = "hw2.csec380.fun"
    target_port = 380
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))
    firstline = "GET /hello HTTP/1.1" + CRLF
    request = firstline + CRLF
    client.send(request.encode())
    httpresponse = client.recv(8192)
    response = httpresponse.decode()
    httpresponse = client.recv(8192)
    response = response + httpresponse.decode()
    client.close()
    return response


def part2():
    target_host = "hw2.csec380.fun"
    target_port = 380
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))
    firstline = "GET /test HTTP/1.1" + CRLF
    secondline = "User-Agent: CSEC-380" + CRLF
    request = firstline + secondline + CRLF
    client.send(request.encode())
    httpresponse = client.recv(8192)
    response = httpresponse.decode()
    httpresponse = client.recv(8192)
    response = response + httpresponse.decode()
    client.close()
    return response

def part3():
    target_host = "hw2.csec380.fun"
    target_port = 380
    username = "alice"
    password = "SecretPassword123!"
    basicEncoding = base64.b64encode((str(username)+":"+str(password)).encode()).decode()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))
    firstline = "GET /basic HTTP/1.1" + CRLF
    secondline = "User-Agent: CSEC-380" + CRLF
    thirdline = f"Authorization: Basic {basicEncoding}" + CRLF
    request = firstline + secondline + thirdline + CRLF
    client.send(request.encode())
    httpresponse = client.recv(8192)
    response = httpresponse.decode()
    httpresponse = client.recv(8192)
    response = response + httpresponse.decode()
    client.close()
    return response

"""
Alice's creds:
username: alice
password: SecretPassword123!
"""

def main():
    separator = "-=-=-=-=-=-=-=-=-\n"
    #print(f"{separator}Part 1:\n\n {part1()}\n")
    #print(f"{separator}Part 2:\n\n {part2()}\n")
    print(f"{separator}Part 3:\n\n {part3()}\n")

if __name__ == "__main__":
    main()