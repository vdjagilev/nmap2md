# nmap2md

A little utility to convert nmap XML results to markdown tables. Forked from [Github:vdjagilev/nmap2md](https://github.com/vdjagilev/nmap2md).

## Usage

Example which parses nmap XML and outputs Markdown tables

```
python nmap2md.py /path/to/file/test.xml -c port,state,service,version --hs 4
```

* `-c` is used to define columns (their order will reflect end result)
    * Default: `port,state,service,version`
    * Supported columns:
    * `port`
    * `state`
    * `service`
    * `version`
* `--hs` is **h**eader **s**ize. Size variations: from 1 to 6.
    * Default: 0 (disable)

## Output example

#### 74.207.244.221

| Port | State | Service | Version |
|------|-------|---------|---------|
| 22/tcp | open | ssh     | OpenSSH 5.3p1 Debian 3ubuntu7 |
| 80/tcp | open | http    | Apache httpd 2.2.14  |
