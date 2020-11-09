import sys

def main(csv_filename: str, illegal_list_filename: str) -> None:
    with open(illegal_list_filename) as f:
        illegal_list = f.read().split()
    with open(csv_filename) as f:
        for line in f:
            if any(map(lambda e: e in line, illegal_list)):
                continue
            print(line, end="")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python {} <target.csv> <illegal SGF list>".format(sys.argv[0]))
        sys.exit(0)
    main(sys.argv[1], sys.argv[2])