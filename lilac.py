import pip

try:
    import requests, time, msmcauth, colorama, json, os
except ModuleNotFoundError:
    
    print("[ ] Installing requirements...")
    pip.main(['install', 'colorama'])
    
    import colorama
    colour = lambda text, colour=colorama.Fore.RESET, reset=colorama.Fore.RESET, enable=True: text if not enable else colour + text + reset

    print(colour("[+] Installed colorama", colorama.Fore.GREEN))
    pip.main(['install', 'requests'])
    
    print(colour("[+] Installed requests", colorama.Fore.GREEN))
    pip.main(['install', 'msmcauth'])
    
    print(colour("[+] Installed msmcauth", colorama.Fore.GREEN))
    print(colour("[+] Installed requirements!", colorama.Fore.GREEN))

    import requests, time, msmcauth, json, os

def colour(text, colour=colorama.Fore.RESET, reset=colorama.Fore.RESET, enable=True):
    if enable:
        return colour + text + reset
    return text


defaults = {
    "reqs": 3,
    "delay": 20,
}

if os.name == "nt":
    colorama.just_fix_windows_console()


def main(input_data=False):

    file_content = {}

    if input_data == False:
    
        email = input(colour("[?] Email: ", colorama.Fore.MAGENTA))
        password = input(colour("[?] Password: ", colorama.Fore.MAGENTA))

        username = input(colour("[?] Username: ", colorama.Fore.MAGENTA))

        file_content["email"] = email
        file_content["password"] = password
        file_content["username"] = username

    else:
        use_colour=False
        email = input_data["email"]
        password = input_data["password"]
        username = input_data["username"]

    
    try:
        login = msmcauth.login(email, password)
        print(colour("[+] Logged in successfully!", colorama.Fore.GREEN))
    except:
        print(colour("[!] Login failed! Can you confirm that your email and password are correct?", colorama.Fore.RED))
        return

    if input_data == False:
        reqs_str = input(colour("[?] Requests per minute (Press enter for default): ", colorama.Fore.MAGENTA))
        reqs = int(reqs_str) if reqs_str != "" else defaults["reqs"]
        delay = 60 / reqs

        file_content["reqs"] = reqs
    else:
        reqs = input_data["reqs"]
        delay = 60 / reqs

    # Save data to file
    if file_content != {}:
        with open("lilac_data.json", "w") as f:
            json.dump(file_content, f)
            print(colour("[+] Saved data to lilac_data.json", colorama.Fore.GREEN))

    

    bearer = login.access_token

    while True:
        
        if time.strftime("%H:%M") == "00:00":
            bearer = msmcauth.login(email, password).access_token
            

        r = requests.put(f'https://api.minecraftservices.com/minecraft/profile/name/{username}', headers={
            "Authorization": f"Bearer {bearer}",
        })
        if r.status_code == 200:
            print(colour(f"[+] [{colour(str(r.status_code), colorama.Fore.CYAN, colorama.Fore.GREEN)}] Successfully changed username to {username} at {time.strftime('%H:%M:%S')}", colorama.Fore.GREEN))
            if input_data:
                return True
            else:
                input(colour("[!] Press enter to exit", colorama.Fore.GREEN))
            break
        elif r.status_code == 403 or r.status_code == 429:
            print(colour(f"[!] [{colour(str(r.status_code), colorama.Fore.CYAN, colorama.Fore.RED)}] Failed to change username to {username} at {time.strftime('%H:%M:%S')}", colorama.Fore.RED))
        else:
            print(colour(f"[!] Unknown error occured at {time.strftime('%H:%M:%S')}", colorama.Fore.RED))
            print(colour(f"    Status code: {r.status_code}", colorama.Fore.RED))
            print(colour(f"    Response: {r.text}", colorama.Fore.RED))
        time.sleep(delay)


if __name__ == '__main__':
    main()