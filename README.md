# nmap2md

A little utility to convert nmap XML results to markdown tables.

## Usage

Example which parses nmap XML and outputs Markdown tables

```
python nmap2md.py /path/to/file/test.xml -c "Port,State,Service,Version" --hs 4 --rc "[port.number]/[port.protocol],[state],*[service.name]*,[service.product] [service.version]"
```

Columns and row cells definition should be divided by `,`.

* `-c` is used to define columns. It is possible to write there anything
    * Default: `Port,State,Service,Version`
* `--rc` is used to define **r**ow **c**ells
    * Default: `[port.number]/[port.protocol],[state],[service.name],[service.product] [service.version]`
    * Available options:
        * `[port.number]` Port number (80) 
        * `[port.protocol]` Port protocol (TCP)
        * `[state]` State (open)
        * `[service.name]` Name of the used service (http)
        * `[service.product]` Type of product used on that service (Apache httpd)
        * `[service.version]` Version of the product (2.2.14)
* `--hs` is **h**eader **s**ize. Size variations: from 1 to 6.
    * Default: 0 (disabled)
* `--print-empty` some port scanning results are empty and those are not displayed. However if there is a need to print empty sets, this option allows this.
    * Default: False

## Output example

Example was taken from https://nmap.org/book/output-formats-xml-output.html and used command above:

#### 74.207.244.221

| Port | State | Service | Version |
|------|-------|---------|---------|
| 22/tcp | open | *ssh* | OpenSSH 5.3p1 Debian 3ubuntu7 |
| 80/tcp | open | *http* | Apache httpd 2.2.14 |

## Contributors

Thanks to Brandon Hinkel (https://github.com/b4ndit) for fixing bugs and testing.