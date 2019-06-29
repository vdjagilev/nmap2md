# nmap2md

A little utility to convert nmap XML results to markdown tables

## Usage

Example which parses nmap XML and outputs Markdown tables

```
python nmap2md.py /path/to/file/test.xml -c protocol,port,service,product,version --hs 4
```

* `-c` is used to define columns (their order will reflect end result)
    * Supported columns:
    * `port`
    * `protocol`
    * `service`
    * `product`
    * `version`
* `--hs` is **h**eader **s**ize. Size variations: from 1 to 6.

## Output example

#### 74.207.244.221

| Protocol | Port | Service | Product | Version |
|----------|------|---------|---------|---------|
| tcp      | 22   | ssh     | OpenSSH | 5.3p1 Debian 3ubuntu7 |
| tcp      | 80   | http    | Apache httpd | 2.2.14  |