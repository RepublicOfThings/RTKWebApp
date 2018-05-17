import random
import os
import re


def generate_secret_key(chars='abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'):
    return ''.join(random.SystemRandom().choice(chars) for i in range(50))


def change_secret_key(dir="RTKWebApp", file="settings.py"):
    path = os.path.join(dir, file)
    key = generate_secret_key()
    data = open(path).read()
    data = re.sub(r'__DEFAULT_SECRET_KEY__', key, data)
    # data = data.format(key=key)
    open(path, "w").write(data)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", help="Directory of settings file.", default="RTKWebApp")
    parser.add_argument("--file", help="Create and configure a target app.", default="settings.py")
    args = parser.parse_args()
    change_secret_key(dir=args.dir, file=args.file)
