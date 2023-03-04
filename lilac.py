import requests, time, msmcauth, colorama, json

defaults = {
    "reqs": 3,
    "delay": 20,
}

def main(input_data=False):

    file_content = {}

    if input_data == False:
        use_colour = input("Use color (May not work with some terminals)? (y/n): ").lower() == "y"
    
        email = input(colour(use_colour, "[?] Email: ", colorama.Fore.MAGENTA))
        password = input(colour(use_colour, "[?] Password: ", colorama.Fore.MAGENTA))

        username = input(colour(use_colour, "[?] Username: ", colorama.Fore.MAGENTA))

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
        print(colour(use_colour, "[+] Logged in successfully!", colorama.Fore.GREEN))
    except:
        print(colour(use_colour, "[!] Login failed! Can you confirm that your email and password are correct?", colorama.Fore.RED))
        return

    if input_data == False:
        reqs_str = input(colour(use_colour, "[?] Requests per minute (Press enter for default): ", colorama.Fore.MAGENTA))
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
            print(colour(use_colour, "[+] Saved data to lilac_data.json", colorama.Fore.GREEN))

    

    bearer = login.access_token

    while True:
        
        if time.strftime("%H:%M") == "00:00":
            bearer = msmcauth.login(email, password).access_token
            

        r = requests.put(f'https://api.minecraftservices.com/minecraft/profile/name/{username}', headers={
            "Authorization": f"Bearer {bearer}",
        })
        if r.status_code == 200:
            print(colour(use_colour, f"[+] Successfully changed username to {username} at {time.strftime('%H:%M:%S')}", colorama.Fore.GREEN))
            if input_data:
                return True
            else:
                input(colour(use_colour, "[!] Press enter to exit", colorama.Fore.GREEN))
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