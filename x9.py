import argparse
from urllib.parse import urlparse, parse_qs, urlencode

def append_hello_to_params(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    for key in query_params:
        query_params[key] = [value + args.value for value in query_params[key]]

    modified_query = urlencode(query_params, doseq=True)
    modified_url = parsed_url._replace(query=modified_query).geturl()

    return modified_url


def create_hello_params_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    for key in query_params:
        query_params[key] = args.value + query_params[key][0]

    modified_query = urlencode(query_params, doseq=True)
    modified_url = parsed_url._replace(query=modified_query).geturl()

    return modified_url

def param(value,chunk,url):
    with open(args.parameters) as f:
        lines = f.readlines()

    lists = []
    final = []

    for i in range(0, len(lines), chunk):
        sublist = lines[i:i+chunk]
        lists.append(sublist)


    for s in range(0,len(lists)):
        query_dict = {}
        for p in lists[s]:

            query_dict[p.replace('\n','')] = value

            query = urlencode(query_dict)

        # Check url have parameters or not
        parsed_url = urlparse(url)
        hpon = bool(parsed_url.query)
        
        if hpon == True:
            param1 = f'{url}&{query}'
        else:
            param1 = f'{url}?{query}'

        final.append(param1)

    return final

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="X9 is a tool for generate url list")

    parser.add_argument("-u", "--url", help='url input.')

    parser.add_argument("-l", "--list", help='list url.')

    parser.add_argument("-p", "--parameters", help='parameters wordlist to file.')

    parser.add_argument("-v", "--value", required=True, help='Value For Parameters to fuzz.')

    parser.add_argument("-o", "--output", help='output result.')

    parser.add_argument("-c", "--chunk", help='Chunk to parameters to fuzz. [defult: 15]')

    parser.add_argument("-s", "--silent", help='Silent mode.')

    parser.add_argument('-gs', '--generate_strategy', choices=['normal', 'ignore', 'combine', 'all'], default='all', help="""Select the mode strategy from the available choice:
    normal: Remove all parameters and put the wordlist
    combine: Pitchfork combine on the existing parameters
    ignore: Don't touch the URL and put the wordlist
    all: All in one method""")

    args = parser.parse_args()

    def gs_normal():
        if not args.silent and args.list and args.parameters:
            with open(args.list, "r") as f:
                for url in f:
                    parsed_url = urlparse(url)
                    modified_url = parsed_url._replace(query='').geturl()
                    for i in param(args.value, int(args.chunk),modified_url):
                        print(i)
            if args.url and args.list and args.parameters:
                parsed_url = urlparse(args.url)
                modified_url = parsed_url._replace(query='').geturl()
                for i in param(args.value, int(args.chunk),modified_url):
                    print(i)


        if args.output and args.list and args.parameters:
            with open(args.output,"w") as o:
                with open(args.list, "r") as f:
                    for url in f:
                        parsed_url = urlparse(url)
                        modified_url = parsed_url._replace(query='').geturl()
                        for i in param(args.value, int(args.chunk),modified_url):
                            o.write(i+'\n')

            if args.url and args.list and args.parameters:
                with open(args.output,"w") as o:
                    parsed_url = urlparse(args.url)
                    modified_url = parsed_url._replace(query='').geturl()
                    for i in param(args.value, int(args.chunk),modified_url):
                        o.write(i+'\n')


    def gs_combine():
        if not args.silent:
            if args.list:

                with open(args.list, "r") as f:
                    for url in f:

                        print(append_hello_to_params(url))
                        print(create_hello_params_url(url))
            if args.url:
                        print(append_hello_to_params(args.url))
                        print(create_hello_params_url(args.url))

        if args.output:
            w = "w"
            if args.generate_strategy == "all":
                w = "a"
            if args.list:
                with open(args.output,w) as o:
                    with open(args.list, "r") as f:
                        for url in f:
                            o.write(append_hello_to_params(url)+'\n')
                            o.write(create_hello_params_url(url)+'\n')
            if args.url:
                w = "w"
                if args.generate_strategy == "all":
                    w = "a"
                with open(args.output,w) as o:
                    o.write(append_hello_to_params(args.url)+'\n')
                    o.write(create_hello_params_url(args.url)+'\n')
            


    def gs_ignore():
        if not args.silent and args.list and args.parameters:
            with open(args.list, "r") as f:
                for url in f:
                    for i in param(args.value, int(args.chunk),url):
                        print(i.replace('\n',''))
            if args.url:
                for i in param(args.value, int(args.chunk),args.url):
                    print(i.replace('\n','')+'\n')

        if args.output and args.list and args.parameters:
            w = "w"
            if args.generate_strategy == "all":
                w = "a"
            with open(args.output,w) as o:
                with open(args.list, "r") as f:
                    for url in f:
                        for i in param(args.value, int(args.chunk),url):
                            o.write(i.replace('\n','')+'\n')
            if args.url and args.list and args.parameters:
                w = "w"
                if args.generate_strategy == "all":
                    w = "a"
                with open(args.output,w) as o:
                    for i in param(args.value, int(args.chunk),args.url):
                        o.write(i.replace('\n','')+'\n')


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
