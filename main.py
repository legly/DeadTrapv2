import argparse
import sys
from scanners.fraud import *
from scanners.basicScan import libphonenumbers
from scanners.numVerifyscan import numverifyScan
import scanners.dork as dork
import osint.fb as fb
import osint.linkedin as linkedin
import osint.twitter as twitter 
from logos import banner
import time

__version__ = 'v1.0.2'

scanners = ["spider", "dork"]

yellow =  '\033[1;33m'
green =  '\033[1;32m'
red =   '\033[1;31m'
magenta = '\033[1;35m'
darkwhite = '\033[0;37m'


def get_parser():
    
    parser = argparse.ArgumentParser(description="DEADTRAP {}".format(__version__))
    
    parser.add_argument('-n', '--number', metavar='number', type=str,
                    help='The phone number to scan (E164 or international format)')

    parser.add_argument('-i', '--input', metavar="input_file", type=argparse.FileType('r'),
                    help='Phone number list to scan (one per line)')

    parser.add_argument('-v', '--verbose', action="store_true", help='Shows how the work is done in each step of the scanning process')

    parser.add_argument('-s', '--scanner', metavar="scanner", type=str,
                    help='''The scanner to use [spider, dork]
                    spider - scans each disposable number providing website's source code available on the dukduckgo frontpage to see if the number is available there (no proxy required)
                    dork - uses google dork search results to find out if the number is there in a disposable number providing website available on the front page of duckduckgo (requires proxy)''')

    parser.add_argument('-o', '--osint', action='store_true',
                    help='Use OSINT reconnaissance')

    parser.add_argument('-rep', '--reputation', action='store_true',
                    help='Scan reputation of the phone number')

    parser.add_argument('-q', '--quite', action='store_true',
                    help='Update the project')

    args = parser.parse_args()

    return parser



def main():

    parser = get_parser()
    args = parser.parse_args()

    if not args.quite:
        banner.main()

    if args.number:
        libphonenumbers(args.number)
        numverifyScan(args.number.replace("+", ""))


    elif args.input:
        for line in args.input.readlines():
            libphonenumbers(line)
            numverifyScan(line.replcae("+", ""))
    
    if args.verbose:
        if args.scanner:
            if args.scanner not in scanners:
                print(red + "[!] No such scanner found" + red)

            elif args.scanner == "dork":
                print(green + "\n[*] Scanning for disposable numbers...\n" + green)
                for i in dork.sites():
                    dork.dorkv(args.number, i)
            else:
                print(green +"\n [*] Scanning for disposable numbers.... \n" + green)
                for i in dork.sites():
                    dork.spiderv(args.number, i)
    elif args.scanner:
        if args.scanner not in scanners:
            print("[!] No such scanner found")

        elif args.scanner == "dork":
            print(green +"[*] Scanning for disposable numbers..."+ green)
            for i in dork.sites():
                dork.dork(args.number, i)
            if len(dork.foundnumbers) > 0:
                print(green +"[+] Found matching numbers on the following sites :" , ",".join(dork.foundnumbers) + green)
            else:
                print(red + "[!] No number was found on top disposable number providing websites" + red)
        else:
            print(green + "\n[*] Scanning for disposable numbers..."+ green)
            for i in dork.sites():
                dork.spider(args.number, i)
            if len(dork.foundnumbers) > 0:
                print(green +"[+] Found matching numbers on the following sites :" , ",".join(dork.foundnumbers) + green)
            else:
                print("[!] No number was found on top disposable number providing websites")

    if args.osint:
        print(green + "\n[*] Scanning social media footprints....\n" + green)
        twitter.twitter(args.number)
        time.sleep(1)
        linkedin.linkedin(libphonenumbers.timezoneResult.split("/")[1])
        time.sleep(1)
        fb.is_valid(args.number)
    
    if args.reputation:
        print(green + "\n[*] Scanning for Reputations of the phonenumber...\n"+ green)
        spamcalls(args.number)
        scamcallfighters(args.number)
        urls(args.number, numverifyScan.data["country_code"].lower(), numverifyScan.data["local_format"])
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()  

    