import csv

INPUT_DIR = "./input"
OUTPUT_DIR = "./output"

CSV_DELIMITER = ","
FILENAME = "rnas_groups.csv"

# increase number of char readable in a single str
csv.field_size_limit(100000000)


def read_file(filename):
    with open(filename, mode="r", encoding='ANSI') as csvfile:
        datareader = csv.DictReader(csvfile, delimiter=CSV_DELIMITER)

        for row in datareader:
            yield row


def parse_member_cns(member_line_data):
    member_cns = list()

    try:
        split_line = member_line_data.split(";")
    except AttributeError:
        return member_cns

    for item in split_line:
        member_cns.append(
            item[4:item.find(",")]
        )

    return member_cns


def remap_member_per_line():
    remapped_lines = list()
    for line in read_file(f"{INPUT_DIR}/{FILENAME}"):
        cns = parse_member_cns(line["member"])
        for cn in cns:
            remapped_lines.append({
                "cn": line['cn'],
                "member": cn
            })

    return remapped_lines


def write_file(data: list):
    headers = data[0].keys()

    with open(f"{OUTPUT_DIR}/{FILENAME}", mode="w", encoding='utf8', newline='') as csvfile:
        datawriter = csv.DictWriter(csvfile, fieldnames=headers, delimiter=CSV_DELIMITER)
        datawriter.writeheader()
        datawriter.writerows(data)


if __name__ == '__main__':
    remapped_lines = remap_member_per_line()
    write_file(remapped_lines)
