# x9

# Usage
```
usage: x9 [-h] [-u URL] [-l LIST] [-p PARAMETERS] -v VALUE [-o OUTPUT] [-c CHUNK] [-s SILENT] [-gs {normal,ignore,combine,all}]
          [-vs {replace,suffix}]

x9 is a tool for generating a URL list

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL input.
  -l LIST, --list LIST  List of URLs.
  -p PARAMETERS, --parameters PARAMETERS
                        Parameters wordlist to file.
  -v VALUE, --value VALUE
                        Value for parameters to fuzz.
  -o OUTPUT, --output OUTPUT
                        Output result.
  -c CHUNK, --chunk CHUNK
                        Chunk to parameters to fuzz. [default: 15]
  -s SILENT, --silent SILENT
                        Silent mode.
  -gs {normal,ignore,combine,all}, --generate_strategy {normal,ignore,combine,all}
                        Select the mode strategy from the available choice: normal: Remove all parameters and put the wordlist combine: Pitchfork      
                        combine on the existing parameters ignore: Don't touch the URL and put the wordlist all: All in one method
  -vs {replace,suffix}, --value_strategy {replace,suffix}
                        Select the mode strategy from the available choices: replace: Replace the value with gathered value suffix: Append the value   
                        to the end of the parameters
```

# Example Command

```
echo "https://domain.tld?p=debug&id=123" | x9 -p url,file,q -v '"voorivexinjected",<b/voorivexinjected'
```
