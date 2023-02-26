import random
import string
from bs4 import BeautifulSoup
from mechanize import Browser
from urllib.error import HTTPError
import time
import argparse

url_list = []
url_listb = []

try:
    with open('goodlist.txt', 'r') as f:
        url_list = [line.strip() for line in f]
    with open('badlist.txt', 'r') as f:
        url_listb = [line.strip() for line in f]
except FileNotFoundError:
    pass

fire = False
cdown = 0
minmax = []


def save_files():
    print("\n Writing files goodlist.txt and badlist.txt")
    with open('goodlist.txt', 'w') as f:
        f.write('\n'.join(url_list))
    with open('badlist.txt', 'w') as f:
        f.write('\n'.join(url_listb))
    return


def get_video_info(video_url):
    br = Browser()
    try:
        res = br.open(video_url)
        data = res.get_data()
        soup = BeautifulSoup(data, "lxml")
        title = soup.find('title').text
        status_tag = soup.find('meta', {'itemprop': 'unlisted'})
        status = True if status_tag is not None else False
        if status:
            print("\n Title: " + title)
            print(" Video unlisted: " + str(status))
        return title, status
    except HTTPError:
        print("\n* Error ")
        print("* ERROR at:: " + video_url)
        return None, None


def do_links(minmax):
    global cdown, url_list, url_listb
    cdown += 1
    # generate random youtube link
    video_id = ''.join([random.choice(string.ascii_letters + string.digits + "_-") for n in range(11)])
    video_url = "http://www.youtube.com/watch?v=" + video_id
    while video_url in url_list or video_url in url_listb:
        print("[ Generated Duplicate Link; Re-generating ]")
        video_id = ''.join([random.choice(string.ascii_letters + string.digits + "_-") for n in range(11)])
        video_url = "http://www.youtube.com/watch?v=" + video_id

    title, status = get_video_info(video_url)
    if status:
        url_list.append(str(video_url) + " Unlisted: " + str(status))
        print(" GOOD URL -> " + video_url)
    else:
        url_listb.append(video_url)
        print(" BAD URL  -> " + video_url)

    print("\n   TRY: " + str(cdown) +
          "\n   GOOD LINKS: " + str(len(url_list)) +
          "\n   BAD LINKS: " + str(len(url_listb)) + "\n")
    if minmax != [0, 0]:
        sleep_time = random.randint(minmax[0], minmax[1])
        print("Waiting " + str(sleep_time) + " seconds...")
        time.sleep(sleep_time)
    do_links(minmax)


def main():
    parser = argparse.ArgumentParser(
        prog='yule3.py',
        description='Scrape YouTube for random links and check if unlisted.',
        epilog='www.phatkid.art')
    parser.add_argument('--timer', nargs=2, type=int, default=[0, 0], help='timer min max in seconds')
    args = parser.parse_args()
    global minmax
    if args.timer != [0, 0]:
        try:
            if args.timer[1] >= args.timer[0]:
                minmax = [args.timer[0], args.timer[1]]
            else:
                minmax = [args.timer[1], args.timer[0]]
        except:
            return
    else:
        minmax = [0, 0]
    print("Timer set to min max " + str(minmax))
    print("* goodlist.txt:" + str(url_list) + "\n")
    try:
        do_links(minmax)
    except KeyboardInterrupt:
        save_files()


if __name__ == '__main__':
    main()
