import sys, time, io, requests
import datetime


def speed_test(size=5, ipv="ipv4", port=80):
    if size == 1024:
        size = "1GB"
    else:
        size = f"{size}MB"

    url = f"http://{ipv}.download.thinkbroadband.com:{port}/{size}.zip"

    with io.BytesIO() as f:
        start = time.perf_counter()
        r = requests.get(url, stream=True)
        total_length = r.headers.get('content-length')
        dl = 0
        if total_length is None:  # no content length header
            f.write(r.content)
        else:
            for chunk in r.iter_content(1024):
                dl += len(chunk)
                f.write(chunk)
                done = int(30 * dl / int(total_length))
                sys.stdout.write(
                    "\r[%s%s] %s Mbps" % ('=' * done, ' ' * (30 - done), dl // (time.perf_counter() - start) / 100000))

    print(f"\n{size} = {(time.perf_counter() - start):.2f} seconds")
    print()

if __name__ == "__main__":
    speed_test(100)
