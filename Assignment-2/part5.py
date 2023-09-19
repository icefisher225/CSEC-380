import socket, base64, time, re

CRLF = "\r\n"


def part5():
    target_host = "hw2.csec380.fun"
    target_port = 380
    username = "alice"
    password = "SecretPassword123!"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    formattedstring = f"username={username}&password={password}"

    request = f"POST /postLogin HTTP/1.1" + CRLF
    request += "User-Agent: CSEC-380" + CRLF
    request += f"Content-Length: {len(formattedstring)}" + CRLF
    request += "Content-Type: application/x-www-form-urlencoded" + CRLF
    request += CRLF
    request += formattedstring + CRLF

    # below is actual connection logic
    client.connect((target_host, target_port))
    client.send(request.encode())
    httpresponse = client.recv(8192)
    response1 = httpresponse.decode()
    httpresponse = client.recv(8192)
    response1 = response1 + httpresponse.decode()

    print(response1)

    client.close()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))

    # second connection????
    request = f"POST /postSecurePage HTTP/1.1" + CRLF
    request += "User-Agent: CSEC-380" + CRLF
    request += f"Cookie: session={response1.split('session=')[1].split(';')[0]}" + CRLF
    request += "Content-Length: 0" + CRLF
    request += "Content-Type: application/x-www-form-urlencoded" + CRLF
    request += CRLF

    # connection logic
    client.send(request.encode())
    httpresponse2 = client.recv(8192)
    response2 = httpresponse2.decode()
    httpresponse2 = client.recv(8192)
    response2 = response2 + httpresponse2.decode()

    client.close()
    return response1, response2


def main():
    separator = "-=-=-=-=-=-=-=-=-\n"
    bar = part5()
    print(
        f"{separator}\nPart 5.1:\n\n{bar[0]}\n\n{separator}\nPart 5.2:\n\n{bar[1]}\n \n"
    )


if __name__ == "__main__":
    main()
