import datetime

"""
format for txt files
[name], [start date], [importance(1-5)]
"""


def parse_file(filename: str) -> list[str]:
    with open(filename, "r") as f:
        lines = f.read().strip().splitlines()
    return lines


def parse_lines(lines: list[str]) -> list[dict]:
    lines = [line.split(",") for line in lines]
    lines = [
        {
            "id": i,
            "name": line[1],
            "start_date": datetime.datetime.strptime(line[2], "%Y-%m-%d").date(),
            "importance": int(line[3]),
        }
        for i, line in enumerate(lines)
    ]
    return lines


def write_lines(filename: str, lines: list[dict]) -> None:
    with open(filename, "w") as f:
        for i in lines:
            f.write(get_fields_as_str(i, sep=","))


def get_fields_as_str(fields: dict, sep: str = " ", end: str = "\n") -> str:
    return (
        sep.join(
            [
                str(fields["id"]),
                str(fields["name"]),
                str(fields["start_date"]),
                str(fields["importance"]),
            ]
        )
        + end
    )


def parse_importance(importance: str) -> int:
    if importance.isdigit():
        return int(importance)
    if not importance:
        print("no importance given - defaulting to 3")
        return 3
    print("! please enter valid importance, must be integer or nothing")
    return -1


def get_entry() -> tuple[str, datetime.datetime, int]:
    name = input("Enter name: ")
    while True:
        start_date = input("Enter start date [DD-MM-YYYY]: ")
        # try:
        start_date = datetime.datetime.strptime(start_date, "%d-%m-%Y").date()
        # except ValueError:
        #     print("! please enter valid date")
        #     continue
        break

    while True:
        importance = input("Enter importance [1-5][enter - default]: ")
        importance = parse_importance(importance)
        if importance != -1:
            break

    return name, start_date, importance


def add_entry(
    source: list[dict], name: str, start_date: datetime.datetime, importance: int
) -> None:
    source.append(
        {
            "id": len(source),
            "name": name,
            "start_date": start_date,
            "importance": importance,
        }
    )


def display_entries(source: list[dict]) -> None:
    today = datetime.date.today()
    result = ""
    for entry in source:
        result += f"{entry['id']}: {entry['name']} - {(entry['start_date'] - today).days} days away\n"

    print(result)


def remove_entry(source, entry: int) -> None:
    source.pop(entry)


def main():
    lines = parse_file("exams.txt")
    lines = parse_lines(lines)
    display_entries(lines)
    while True:
        command = input("> ").strip()
        command = command.split(" ")
        keyword = command.pop(0)
        match keyword:
            case "add":
                if not command:
                    name, start_date, importance = get_entry()
                else:
                    name, start_date = command[0], command[1]
                    if not len(command) < 3:
                        importance = parse_importance(command[2])
                    else:
                        importance = 3

                    if importance == -1:
                        print("! please enter valid importance")
                        continue
                add_entry(lines, name, start_date, importance)

            case "exit":
                break

            case "edit":
                pass

            case "display":
                display_entries(lines)

            case "rm":
                if not command:
                    id = int(input("Enter id: "))
                else:
                    id = int(command[0])
                remove_entry(lines, id)

    write_lines("exams.txt", lines)


if __name__ == "__main__":
    main()
