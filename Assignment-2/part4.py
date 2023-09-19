import socket, base64, time, re

CRLF = "\r\n"


def part4():
    target_host = "hw2.csec380.fun"
    target_port = 380
    username = "alice"
    password = "SecretPassword123!"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    firstline = f"GET /getLogin?username={username}&password={password} HTTP/1.1" + CRLF
    secondline = "User-Agent: CSEC-380" + CRLF
    request = firstline + secondline + CRLF

    # below is actual connection logic
    client.connect((target_host, target_port))
    client.send(request.encode())
    httpresponse = client.recv(8192)
    response1 = httpresponse.decode()
    httpresponse = client.recv(8192)
    response1 = response1 + httpresponse.decode()

    client.close()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))

    # second connection????
    firstline2 = f"GET /getSecurePage HTTP/1.1" + CRLF
    secondline2 = "User-Agent: CSEC-380" + CRLF
    thirdline2 = (
        f"Cookie: session={response1.split('session=')[1].split(';')[0]}" + CRLF
    )
    # print(f"3l2 = {thirdline2}")
    request2 = firstline2 + secondline2 + thirdline2 + CRLF
    # print(f"request2={request2}")

    # connection logic
    client.send(request2.encode())
    httpresponse2 = client.recv(8192)
    response2 = httpresponse2.decode()
    httpresponse2 = client.recv(8192)
    response2 = response2 + httpresponse2.decode()

    client.close()
    return response1, response2


def main():
    separator = "-=-=-=-=-=-=-=-=-\n"
    foo = part4()
    print(
        f"{separator}\nPart 4.1:\n\n{foo[0]}\n\n{separator}\nPart 4.2:\n\n{foo[1]}\n \n"
    )


if __name__ == "__main__":
    main()
