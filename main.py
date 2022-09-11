import random
import sys
import os
import argparse
from Logger_class import LoggerOut, LoggerIn

flashcards = {}
flashcards_mistake = {}


def add_term():
    print("The card:")
    term = input()
    if term not in flashcards.keys():
        add_definition(term)
        flashcards_mistake[term] = 0
    else:
        print(f'The card "{term}" already exists. Try again:')
        add_term()


def add_definition(term):
    print("The definition of the card:")
    definition = input()
    if definition not in flashcards.values():
        flashcards[term] = definition
        print(f'The pair ("{term}":"{definition}") has been added.')
    else:
        print(f'The definition "{definition}" already exists. Try again:')
        add_definition(term)


def remove_pair():
    print("Which card?")
    card_to_remove = input()
    if card_to_remove in flashcards.keys():
        del flashcards[card_to_remove]
        del flashcards_mistake[card_to_remove]
        print("The card has been removed.")
    else:
        print(f'Can\'t remove "{card_to_remove}": there is no such card.')


def import_file(filename=None):
    counter = 0
    if filename is None:
        print("File name:")
        import_to_file = input()
    else:
        import_to_file = filename
    try:
        with open(import_to_file, "r") as text_file:
            for line in text_file:
                line_list = line.split()
                flashcards[line_list[0]] = line_list[1]
                flashcards_mistake[line_list[0]] = int(line_list[2])
                counter += 1
            print(f"{counter} cards have been loaded.")
    except FileNotFoundError:
        print("File not found.")


def export_file(filename=None):
    if filename is None:
        print("File name:")
        export_to_file = input()
    else:
        export_to_file = filename
    with open(export_to_file, "w") as text_file:
        for k, v in flashcards.items():
            text_file.write(f"{k} {v} {flashcards_mistake[k]}\n")
    print(f"{len(flashcards)} cards have been saved.")


def ask():
    print('How many times to ask?')
    for _ in range(int(input())):
        card, definition = random.choice(list(flashcards.items()))
        print(f'Print the definition of "{card}":')
        answer = input()
        if answer == definition:
            print("Correct!")
        elif answer in flashcards.values():
            flashcards_mistake[card] += 1
            for k, v in flashcards.items():
                if answer == v:
                    your_card = k
                    print(f'Wrong. The right answer is "{definition}",'
                          f' but your definition is correct for "{your_card}"')
        else:
            flashcards_mistake[card] += 1
            print(f'Wrong. The right answer is "{definition}"')


def log_entry():
    print("File name:")
    log_file = input()
    os.rename("default.txt", log_file)
    sys.stdout = LoggerOut(log_file)
    sys.stdin = LoggerIn(log_file)
    print("The log has been saved.")


def hard_card_output():
    try:
        max_mistake = max(flashcards_mistake.values())
        hard_card = [key for key, value in flashcards_mistake.items() if value == max_mistake]
        if max_mistake != 0:
            if len(hard_card) > 1:
                for_printing = ""
                print(f'The hardest cards are ', end="")
                for i in hard_card:
                    for_printing += f'"{i}", '
                print(f"{for_printing[:-2]}. You have {max_mistake} errors answering them.")
            elif len(hard_card) == 1:
                print(f'The hardest card is "{hard_card[0]}". You have {max_mistake} errors answering it.')
        else:
            print("There are no cards with errors.")
    except ValueError:
        print("There are no cards with errors.")


def reset_stats():
    for key in flashcards_mistake.keys():
        flashcards_mistake[key] = 0
    print("Card statistics have been reset.")


def main(export_, import_):
    if import_:
        import_file(import_)

    default_log = 'default.txt'
    sys.stdout = LoggerOut(default_log)
    sys.stdin = LoggerIn(default_log)

    while True:
        actions_dict = {"add": add_term, "remove": remove_pair, "import": import_file, "export": export_file,
                        "ask": ask, "log": log_entry, "hardest card": hard_card_output, "reset stats": reset_stats}
        print("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
        action = input()
        if action == "exit":
            if export_:
                export_file(export_)
            print("Bye bye!")
            exit()
        actions_dict[action]()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--export_to", type=str, help="Enter a file name for the export.")
    parser.add_argument("--import_from", type=str, help="Enter a file name for the import.")
    args = parser.parse_args()

    main(args.export_to, args.import_from)
