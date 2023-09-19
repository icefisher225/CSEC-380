import socket, base64, time, re

CRLF = "\r\n"


def part3():
    target_host = "hw2.csec380.fun"
    target_port = 380
    username = "alice"
    password = "SecretPassword123!"
    basicEncoding = base64.b64encode(
        (str(username) + ":" + str(password)).encode()
    ).decode()

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


def main():
    separator = "-=-=-=-=-=-=-=-=-\n"
    print(f"{separator}Part 3:\n\n {part3()}\n")


if __name__ == "__main__":
    main()
