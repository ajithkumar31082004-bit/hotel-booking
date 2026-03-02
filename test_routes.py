import time, urllib.request as req
time.sleep(1)
urls = [
    'http://127.0.0.1:5000/login',
    'http://127.0.0.1:5000/dashboard',
]
for url in urls:
    try:
        r = req.Request(url, headers={'User-Agent': 'test'})
        resp = req.urlopen(r, timeout=5)
        code = resp.getcode()
        content = resp.read().decode('utf-8', errors='ignore')
        has_gold = '#d4af37' in content
        has_demo = 'fillDemo' in content or 'demo-pill' in content
        print(f"OK {code} gold={has_gold} demo={has_demo} - {url}")
    except urllib.error.HTTPError as e:
        print(f"FAIL {e.code} - {url}")
    except Exception as e:
        print(f"ERROR - {url}: {e}")
