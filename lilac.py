import requests, time, msmcauth, colorama

defaults = {
    "reqs": 3,
    "delay": 20,
}

def main():

    use_colour = input("Use color (May not work with some terminals)? (y/n): ").lower() == "y"
    
    email = input(colour(use_colour, "[?] Email: ", colorama.Fore.MAGENTA))
    password = input(colour(use_colour, "[?] Password: ", colorama.Fore.MAGENTA))

    username = input(colour(use_colour, "[?] Username: ", colorama.Fore.MAGENTA))

    
    try:
        login = msmcauth.login(email, password)
        print(colour(use_colour, "[+] Logged in successfully!", colorama.Fore.GREEN))
    except:
        print(colour(use_colour, "[!] Login failed! Can you confirm that your email and password are correct?", colorama.Fore.RED))
        return

    reqs_str = input(colour(use_colour, "[?] Requests per minute: ", colorama.Fore.MAGENTA))
    reqs = int(reqs_str) if reqs_str != "" else defaults["reqs"]
    delay = 60 / reqs

    bearer = login.access_token

    while True:
        
        if time.strftime("%H:%M") == "00:00":
            bearer = msmcauth.login(email, password).access_token
            

        r = requests.put(f'https://api.minecraftservices.com/minecraft/profile/name/{username}', headers={
            "Authorization": f"Bearer {bearer}",
        })
        if r.status_code == 200:
            print(colour(use_colour, f"[+] Successfully changed username to {username} at {time.strftime('%H:%M:%S')}", colorama.Fore.GREEN))
            break
        elif r.status_code == 403:
            print(colour(use_colour, f"[!] Failed to change username to {username} at {time.strftime('%H:%M:%S')}", colorama.Fore.RED))
        else:
            print(colour(use_colour, f"[!] Unknown error occured at {time.strftime('%H:%M:%S')}", colorama.Fore.RED))
            print(colour(use_colour, f"    Status code: {r.status_code}", colorama.Fore.RED))
            print(colour(use_colour, f"    Response: {r.text}", colorama.Fore.RED))
        time.sleep(delay)

def colour(enable, text, colour=colorama.Fore.RESET):
    if enable:
        return colour + text + colorama.Fore.RESET
    return text


if __name__ == '__main__':
    main()