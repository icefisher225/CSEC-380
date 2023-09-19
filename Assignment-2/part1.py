import socket, base64, time, re

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


def main():
    separator = "-=-=-=-=-=-=-=-=-\n"
    print(f"{separator}Part 1:\n\n {part1()}\n")


if __name__ == "__main__":
    main()
