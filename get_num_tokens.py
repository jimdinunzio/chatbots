import openai_api as oai
import argparse

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
    
def main():
    oai_api = oai.OpenAiApi()
    parser = argparse.ArgumentParser(
        description="count the number of tokens in a file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--file",
        type=argparse.FileType('r'),
        required=True,
        help="File to count tokens",)
    args = parser.parse_args()

    text = args.file.read()
    print("number of tokens is ", oai_api.num_tokens_from_str(text))

if __name__ == '__main__':
    main()