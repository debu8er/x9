# x9

# Usage
```
usage: x9.py [-h] [-u URL] [-l LIST] [-p PARAMETERS] -v VALUE [-o OUTPUT]
             [-c CHUNK] [-s SILENT] [-gs {normal,ignore,combine,all}]

X9 is a tool for generate url list

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     url input.
  -l LIST, --list LIST  list url.
  -p PARAMETERS, --parameters PARAMETERS
                        parameters wordlist to file.
  -v VALUE, --value VALUE
                        Value For Parameters to fuzz.
  -o OUTPUT, --output OUTPUT
                        output result.
  -c CHUNK, --chunk CHUNK
                        Chunk to parameters to fuzz. [defult: 15]
  -s SILENT, --silent SILENT
                        Silent mode.
  -gs {normal,ignore,combine,all}, --generate_strategy {normal,ignore,combine,all}
                        Select the mode strategy from the available choice:
                        normal: Remove all parameters and put the wordlist
                        combine: Pitchfork combine on the existing parameters
                        ignore: Don't touch the URL and put the wordlist all:
```
