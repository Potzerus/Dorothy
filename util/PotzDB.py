import csv


def get(file, header: str, value) -> list:
    reader = csv.reader(file.read().split("\n"))
    headers = reader.__next__()
    print(headers)
    for i, _header in enumerate(headers):
        if header == _header:
            header = i
            break
    results = []
    if not isinstance(header, str):
        for line in reader:
            if line[header] == value:
                results.append({_header:element for _header,element in zip(headers,line)})
    return results


if __name__ == "__main__":
    print(get(open("Test.csv"), "Name", "Oda"))
