import random
import string
from bs4 import BeautifulSoup
from mechanize import Browser
from urllib.error import HTTPError
import time

url_list = []
url_listb = []

try:
    with open('goodlist.txt', 'r') as f:
        url_list = f.read().splitlines()
    with open('badlist.txt', 'r') as f:
        url_listb = f.read().splitlines()
except FileNotFoundError:
    pass

fire = False
cdown = 0


def save_files():
    print("Writing files...")
    global url_list, url_listb
    with open('goodlist.txt', 'w') as f:
        f.write('\n'.join(url_list))
    with open('badlist.txt', 'w') as f:
        f.write('\n'.join(url_listb))
    return


def do_links():
    global cdown, url_list, url_listb
    cdown = cdown + 1
    # generate random youtube link
    x = ''.join([random.choice(string.ascii_letters + string.digits + "_-") for n in range(11)])
    while x in url_list or x in url_listb:
        print("Generated Duplicate Link; Re-generating")
        x = ''.join([random.choice(string.ascii_letters + string.digits + "_-") for n in range(11)])
    br = Browser()
    try:
        res = br.open("http://www.youtube.com/watch?v=" + x)
        data = res.get_data()
        soup = BeautifulSoup(data, "lxml")
        title = soup.find('title')
        # bad links are titled ' - YouTube'
        # good links have other titles
        if str(title) != "<title> - YouTube</title>":
            print("Title: " + str(title))
            url_list.append("http://www.youtube.com/watch?v=" + x)
            print("CHECK -> http://www.youtube.com/watch?v=" + x)
        else:
            url_listb.append("http://www.youtube.com/watch?v=" + x)

    except HTTPError:
        print("Error ")
        print("ERROR at:: http://www.youtube.com/watch?v=" + x)

    print("TRY: " + str(cdown) + "\nGOOD LINKS: " + str(len(url_list)) + "\nBAD LINKS: " + str(len(url_listb)))
    sleep_time = random.randint(5, 30)
    print("Sleeping " + str(sleep_time) + " seconds...")
    time.sleep(sleep_time)
    do_links()


def main():
    print("Good urls generated with this script so far:")
    print(url_list)
    try:
        do_links()
    except KeyboardInterrupt:
        save_files()


if __name__ == '__main__':
    main()
