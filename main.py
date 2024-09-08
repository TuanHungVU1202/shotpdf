from service.input_simulator import *


def main():
    json_data = parse_json_file('resources/single_key.json')
    print("Content of single_key.json:")
    print(json_data)


if __name__ == "__main__":
    main()