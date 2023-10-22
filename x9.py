import argparse
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import time
import sys
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def append_hello_to_params(url,value):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    
    output = []
    if "," in value:
        for i in value.split(","):

            for key in query_params:
                query_params[key] = [value + i for value in query_params[key]]

            modified_query = urlencode(query_params, doseq=True)
            modified_url = parsed_url._replace(query=modified_query).geturl()
            output.append(modified_url)

    else:
        for key in query_params:
            query_params[key] = [valuee + value for valuee in query_params[key]]

        modified_query = urlencode(query_params, doseq=True)
        modified_url = parsed_url._replace(query=modified_query).geturl()
        output.append(modified_url)

    return output


def create_hello_params_url(url,value):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    output = []
    if "," in value:
        for i in value.split(","):

            for key in query_params:
                query_params[key] = i + query_params[key][0]

            modified_query = urlencode(query_params, doseq=True)
            modified_url = parsed_url._replace(query=modified_query).geturl()

            output.append(modified_url)
    
    else:
        for key in query_params:
            query_params[key] = value + query_params[key][0]

        modified_query = urlencode(query_params, doseq=True)
        modified_url = parsed_url._replace(query=modified_query).geturl()

        output.append(modified_url)

    return output


def param(value, chunk, url):
    lists = []
    final = []

    if "," in args.parameters:
        lines = args.parameters.split(',')
        for i in range(0, len(lines), int(chunk)):
            sublist = lines[i:i + int(chunk)]
            lists.append(sublist)

    if os.path.exists(args.parameters):
        with open(args.parameters) as f:
            lines = f.readlines()
            for i in range(0, len(lines), int(chunk)):
                sublist = lines[i:i + int(chunk)]
                lists.append(sublist)
    
    if not os.path.exists(args.parameters) and not "," in args.parameters:
        lists.append(args.parameters)


    if "," in value:
        for value in value.split(','):
            for s in range(0, len(lists)):
                query_dict = {}
                
                for p in lists[s]:
                    query_dict[p.replace('\n', '')] = value
                    query = urlencode(query_dict)

                parsed_url = urlparse(url)
                hpon = bool(parsed_url.query)

                if hpon:
                    param1 = f'{url}&{query}'
                else:
                    param1 = f'{url}?{query}'

                final.append(param1)


    else:
        for s in range(0, len(lists)):
            query_dict = {}
            
            for p in lists[s]:
                query_dict[p.replace('\n', '')] = value
                query = urlencode(query_dict)

            parsed_url = urlparse(url)
            hpon = bool(parsed_url.query)

            if hpon:
                param1 = f'{url}&{query}'
            else:
                param1 = f'{url}?{query}'

            final.append(param1)
    return final


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="x9 is a tool for generating a URL list")

    parser.add_argument("-u", "--url", help='URL input.')
    parser.add_argument("-l", "--list", help='List of URLs.')
    parser.add_argument("-p", "--parameters", help='Parameters wordlist to file.')
    parser.add_argument("-v", "--value", required=True, help='Value for parameters to fuzz.')
    parser.add_argument("-o", "--output", help='Output result.')
    parser.add_argument("-c", "--chunk", help='Chunk to parameters to fuzz. [default: 15]')
    parser.add_argument("-s", "--silent", help='Silent mode.')
    parser.add_argument('-gs', '--generate_strategy', choices=['normal', 'ignore', 'combine', 'all'], default='all',
                        help="""Select the mode strategy from the available choice:
    normal: Remove all parameters and put the wordlist
    combine: Pitchfork combine on the existing parameters
    ignore: Don't touch the URL and put the wordlist
    all: All in one method""")
    parser.add_argument('-vs', '--value_strategy', choices=['replace', 'suffix'], default='replace', help="""Select the mode strategy from the available choices:
        replace: Replace the value with gathered value
        suffix: Append the value to the end of the parameters""")
    args = parser.parse_args()

    if args.chunk:
        chunk = args.chunk
    else:
        chunk = 15

    stdin = not sys.stdin.isatty()
    input_urls = [line.strip() for line in sys.stdin.readlines()] if stdin else []

    def gs_normal():
        if args.parameters:
            urls = [args.url] if args.url else []
            if args.list:
                with open(args.list, "r") as f:
                    urls += [url.strip() for url in f.readlines()]

            if stdin:
                urls += input_urls

            for url in urls:
                parsed_url = urlparse(url)
                modified_url = parsed_url._replace(query='').geturl()
                for i in param(args.value, int(chunk), modified_url):
                    print(i)

            if args.output:
                with open(args.output, "w") as o:
                    for url in urls:
                        parsed_url = urlparse(url)
                        modified_url = parsed_url._replace(query='').geturl()
                        for i in param(args.value, int(chunk), modified_url):
                            o.write(i + '\n')

    def gs_combine():
        if args.parameters:
            urls = [args.url] if args.url else []

            if args.list:
                with open(args.list, "r") as f:
                    urls += [url.strip() for url in f.readlines()]

            if stdin:
                urls += input_urls

            for url in urls:
                parsed_url = urlparse(url)
                query_params = parse_qs(parsed_url.query)

                if args.value_strategy == "replace":
                    for key in query_params:
                        query_params[key] = [args.value]

                    updated_query = urlencode(query_params, doseq=True)
                    modified_url = urlunparse(parsed_url._replace(query=updated_query))

                    for i in param(args.value, int(chunk), modified_url):
                        print(i)
                elif args.value_strategy == "suffix":
                    for modified_url in append_hello_to_params(url, args.value):
                        for i in param(args.value, int(chunk), modified_url):
                            print(i)
                    for modified_url in create_hello_params_url(url, args.value):
                        for i in param(args.value, int(chunk), modified_url):
                            print(i)

            if args.output:
                with open(args.output, "w") as o:

                    for url in urls:
                        parsed_url = urlparse(url)
                        query_params = parse_qs(parsed_url.query)

                        if args.value_strategy == "replace":
                            for key in query_params:
                                query_params[key] = [args.value]

                            updated_query = urlencode(query_params, doseq=True)
                            modified_url = urlunparse(parsed_url._replace(query=updated_query))

                            for i in param(args.value, int(chunk), modified_url):
                                o.write(i + '\n')
                        elif args.value_strategy == "suffix":
                            for modified_url in append_hello_to_params(url, args.value):
                                for i in param(args.value, int(chunk), modified_url):
                                    o.write(i + '\n')
                            for modified_url in create_hello_params_url(url, args.value):
                                for i in param(args.value, int(chunk), modified_url):
                                    o.write(i + '\n')
    def gs_ignore():
        if args.parameters:
            urls = [args.url] if args.url else []
            if args.list:
                with open(args.list, "r") as f:
                    urls += [url.strip() for url in f.readlines()]

            if stdin:
                urls += input_urls

            for url in urls:
                for i in param(args.value, chunk, url):
                    print(i.replace('\n', ''))

            if args.output:
                mode = "a" if args.generate_strategy == "all" else "w"
                with open(args.output, mode) as o:
                    for url in urls:
                        for i in param(args.value, chunk, url):
                            o.write(i.replace('\n', '') + '\n')

    if not args.silent:
        print(bcolors.FAIL + "       ___")
        print(bcolors.FAIL + "__  __/ _ \ ")
        print(bcolors.OKGREEN + "\ \/ / (_) |")
        print(bcolors.ENDC + " >  < \__, |")
        print(bcolors.OKBLUE + "/_/\_\  /_/")
        time.sleep(1)
        print(bcolors.BOLD + "********** Made by debug (Discord: debu8er) **********\n")

    if args.generate_strategy == "all":
        gs_normal()
        gs_combine()
        gs_ignore()

    if args.generate_strategy == "normal":
        gs_normal()

    if args.generate_strategy == "combine":
        gs_combine()

    if args.generate_strategy == "ignore":
        gs_ignore()
1234
