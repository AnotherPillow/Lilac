from win10toast import ToastNotifier
from lilac import main as lilac
import os,json,sys

def notify(title, msg):
    toaster = ToastNotifier()
    toaster.show_toast(title=title, msg=msg, duration=5)

if not os.path.exists("lilac_data.json"):
    notify("Lilac", "Please setup Lilac first!")
    sys.exit()

input_data = json.load(open("lilac_data.json"))

notify("Lilac", f"Starting Lilac, attempting to get username {input_data['username']}")
if lilac(input_data):
    notify("Lilac", f"Successfully changed username to {input_data['username']}")