import random
import string
from bs4 import BeautifulSoup
from mechanize import Browser
import pickle
from urllib.error import HTTPError
import time

url_list = []
url_listb = []

try:
    a_list = pickle.load(open('goodlist.txt', 'rb'))
    b_list = pickle.load(open('badlist.txt', 'rb'))
    for line in a_list:
        url_list.append(line)
    for line in b_list:
        url_listb.append(line)
except EOFError:
    pass

fire = False
cdown = 0


def save_files():
    print("Writing files...")
    global url_list, url_listb
    pickle.dump(url_list, open('goodlist.txt', 'wb'))
    pickle.dump(url_listb, open('badlist.txt', 'wb'))
    return

def kill_mode():
    global fire, cdown, url_list, url_listb
    if (fire):
        cdown = cdown + 1
        # generate random youtube link
        x = ''.join([random.choice(string.ascii_letters + string.digits + "_-") for n in range(11)])
        while x in url_list or x in url_listb:
            print("Generated Duplicate Link; Re-generating")
            x = ''.join([random.choice(string.ascii_letters + string.digits + "_-") for n in range(11)])
        br = Browser()
        try:
            res = br.open("http://www.youtube.com/watch?v=" + x)
            time.sleep(2)
            data = res.get_data()
            soup = BeautifulSoup(data, "lxml")
            title = soup.find('title')
            # bad links are titled 'YouTube'
            if str(title) != "<title> - YouTube</title>":
                print("Title: " + str(title))
                url_list.append("http://www.youtube.com/watch?v=" + x)
                print("CHECK -> http://www.youtube.com/watch?v=" + x)
            # good links have other titles
            else:
                url_listb.append("http://www.youtube.com/watch?v="+ x)

        except HTTPError:
            print("Error ")
            print("ERROR at:: http://www.youtube.com/watch?v=" + x)

        print("TRY: " + str(cdown) + "\nGOOD LINKS: " + str(len(url_list)) + "\nBAD LINKS: " + str(len(url_listb)))
    print("Sleeping 45 seconds between attempts...")
    time.sleep(43)
    kill_mode()


def main():
    global fire
    fire = True
    print("Good urls generated with this script so far:")
    print(url_list)
    try:
        kill_mode()
    except KeyboardInterrupt:
        save_files()


if __name__ == '__main__':
    main()
