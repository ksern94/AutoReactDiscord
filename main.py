import sys
import os
import argparse
import json
import subprocess

import time
import re


from lib.core import AutoDiscord

if __name__ == "__main__":

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-bg", "--background", help="Run browser in background", action='store_true')

    args = parser.parse_args()
    # end of arguments

    # Loads user configurations from config.json
    with open('config.json', 'r') as u:
        config = json.load(u)
    # end with
    
    bot = AutoDiscord()

    isHeadless = False
    if(args.background):
        isHeadless = True

    browser = bot.launch_browser(isHeadless)

    while True:
        #infinite loop
        for discord_info in config["discord_urls"]:
            url = discord_info["url"]
            server_name = discord_info["server_name"]

            print(f"Going to Server: {server_name}")
            bot.go_to_discord_server(browser, url)
        #end for
    # end while

    input("Press the <ENTER> key to end...")
# end __main__
