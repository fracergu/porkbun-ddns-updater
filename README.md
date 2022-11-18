# Porkbun DDNS update script made in Python

## Requeriments

1. Install requests with pip

```bash
pip install requests
```

2. Cofigure your porkbun API_KEY, SECRET_API_KEY and DOMAIN_NAME in the script
3. Make the script executable if necessary

```bash
$ chmod +x porkbun-ddns-updater.py
```

4. (Optional) move the script to /usr/local/bin to make it available globally

```bash
$ sudo mv porkbun-ddns-updater.py /usr/local/bin/porkbun-ddns-updater
```

---

## Flags

- **--all**: update all existing records
- **--records**: update all records with the given name
  - Records must be separated by commas
  - Wildcard should be surrounded by quotes: '\*'
  - To refer to de main record, use an empty string: ''
- **--sleep**: (Optional) time to wait before updating the records
- **--ttl**: (Optional) TTL for the records, 600 is the minimum value and it will be set as default.

Flags **--all** and **--records** are mutually exclusive

---

## Usage

```bash
$ porkbun-ddns-updater --all | --records <records> [--sleep <seconds>] [--ttl <seconds>]
```

---

## Usage examples

- Update all records

```bash
$ porkbun-ddns-updater --all
```

- Update wildcard, main and www records

```bash
$ porkbun-ddns-updater --records "*","",www
```

- Update all records with a 5 minutes delay and a TTL of 3600 seconds

```bash
$ porkbun-ddns-updater --all --sleep 300 --ttl 3600
```

---

## Operation

At the time of development, the Porkbun API is in Beta. I have found that the endpoint for editing records does not work as described in their [documentation](https://porkbun.com/api/json/v3/documentation#DNS%20Edit%20Record%20by%20Domain%20and%20ID), or I have not been able to properly understand how it works, making it impossible to use it.
Instead of using this, the delete and create endpoints are used, this causes the records to be changed at the object level, but does not affect the purpose of updating the public IP to which they are directed.
If at some point it is solved or you know of a solution to the problem, feel free to open a PR.
