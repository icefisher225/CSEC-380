import socket, base64, time

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
    request += "ContentLength: 0" + CRLF
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


def part6():
    target_host = "hw2.csec380.fun"
    target_port = 380
    username = "alice"
    password = "SecretPassword123!"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    formattedstring = f"username={username}&password={password}"

    request = f"POST /delayedPostLogin HTTP/1.1" + CRLF
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

    # print(response1)

    client.close()
    print("Authenticated, waiting 35 seconds to proceed to authorized content...")
    time.sleep(35)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))

    # second connection????
    request = f"POST /delayedPostSecurePage HTTP/1.1" + CRLF
    request += "User-Agent: CSEC-380" + CRLF
    request += f"Cookie: session={response1.split('session=')[1].split(';')[0]}" + CRLF
    request += "ContentLength: 0" + CRLF
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


def part7():
    target_host = "hw2.csec380.fun"
    target_port = 380
    username = "alice"
    password = "SecretPassword123!"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    formattedstring = f"username={username}&password={password}"

    request = f"POST /jsonLogin HTTP/1.1" + CRLF
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

    # print(response1)

    client.close()

    api_key = str(response1).split(',"key":"')[1].split('"')[0]
    formattedapi_key = f"apikey={api_key}"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))

    # second connection????
    request = f"POST /jsonSecurePage HTTP/1.1" + CRLF
    request += "User-Agent: CSEC-380" + CRLF
    request += f"Cookie: session={response1.split('session=')[1].split(';')[0]}" + CRLF
    request += f"Content-Length: {len(formattedapi_key)}" + CRLF
    request += "Content-Type: application/x-www-form-urlencoded" + CRLF
    request += CRLF
    request += formattedapi_key + CRLF

    # connection logic
    client.send(request.encode())
    httpresponse2 = client.recv(8192)
    response2 = httpresponse2.decode()
    httpresponse2 = client.recv(8192)
    response2 = response2 + httpresponse2.decode()

    client.close()

    return response1, response2


"""
Alice's creds:
username: alice
password: SecretPassword123!
"""


def main():
    separator = "-=-=-=-=-=-=-=-=-\n"

    # Part 1 - Simple HTTP Request
    # print(f"{separator}Part 1:\n\n {part1()}\n")

    # Part 2 - User-Agent
    # print(f"{separator}Part 2:\n\n {part2()}\n")

    # Part 3 - Basic Auth
    # print(f"{separator}Part 3:\n\n {part3()}\n")

    # Part 4 - GET Params
    # foo = part4()
    # print(
    #     f"{separator}\nPart 4.1:\n\n{foo[0]}\n\n{separator}\nPart 4.2:\n\n{foo[1]}\n \n"
    # )

    # Part 5 - POST
    # bar = part5()
    # print(
    #    f"{separator}\nPart 5.1:\n\n{bar[0]}\n\n{separator}\nPart 5.2:\n\n{bar[1]}\n \n"
    # )

    # Part 6 - POST with a delay
    # baz = part6()
    # print(
    #     f"{separator}\nPart 6.1:\n\n{baz[0]}\n\n{separator}\nPart 6.2:\n\n{baz[1]}\n \n"
    # )

    # Part 7 - JSON Keys/API
    qux = part7()
    print(
        f"{separator}\nPart 7.1:\n\n{qux[0]}\n\n{separator}\nPart 7.2:\n\n{qux[1]}\n \n"
    )

    # Part 8 - Bye Bye Captcha
    # quux = part8()


if __name__ == "__main__":
    main()
