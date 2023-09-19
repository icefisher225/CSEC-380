import socket, base64, time, re

CRLF = "\r\n"


def part8():
    target_host = "hw2.csec380.fun"
    target_port = 380
    username = "alice"
    password = "SecretPassword123!"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    formattedstring = f"username={username}&password={password}"

    request = f"POST /captchaLogin HTTP/1.1" + CRLF
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

    # Recieve and calculate captcha

    captcha = str(response1).split("Connection: close\r\n\r\n")[1]

    pattern = r"[^\d\+\-\*\/]"

    cleaned_captcha = re.sub(pattern, "", captcha)

    # print(f"Captcha = {cleaned_captcha}")

    captcha_sol = eval(cleaned_captcha)
    formattedcaptcha_sol = f"solution={captcha_sol}"

    # print(captcha_sol)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))

    # second connection????
    request = f"POST /captchaValidate HTTP/1.1" + CRLF
    request += "User-Agent: CSEC-380" + CRLF
    request += f"Cookie: session={response1.split('session=')[1].split(';')[0]}" + CRLF
    request += f"Content-Length: {len(formattedcaptcha_sol)}" + CRLF
    request += "Content-Type: application/x-www-form-urlencoded" + CRLF
    request += CRLF
    request += formattedcaptcha_sol + CRLF

    # connection logic
    client.send(request.encode())
    httpresponse2 = client.recv(8192)
    response2 = httpresponse2.decode()
    httpresponse2 = client.recv(8192)
    response2 = response2 + httpresponse2.decode()

    client.close()

    # print(response2)

    # Finally, make the connection.
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))

    # second connection????
    request = f"POST /captchaSecurePage HTTP/1.1" + CRLF
    request += "User-Agent: CSEC-380" + CRLF
    request += f"Cookie: session={response1.split('session=')[1].split(';')[0]}" + CRLF
    request += f"Content-Length: 0" + CRLF
    request += "Content-Type: application/x-www-form-urlencoded" + CRLF
    request += CRLF

    client.send(request.encode())

    httpresponse3 = client.recv(8192)
    response3 = httpresponse3.decode()
    httpresponse3 = client.recv(8192)
    response3 = response3 + httpresponse3.decode()

    client.close()
    # print(response3)

    return response1, response2, response3


def main():
    separator = "-=-=-=-=-=-=-=-=-\n"
    quux = part8()
    print(
        f"{separator}\nPart 8.1:\n\n{quux[0]}\n\n{separator}\nPart 8.2:\n\n{quux[1]}\n\n{separator}\nPart 8.3:\n\n{quux[2]}\n \n"
    )


if __name__ == "__main__":
    main()
