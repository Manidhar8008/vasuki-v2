from api.ask import AskAPI

def main():
    api = AskAPI()

    print("VASUKI v2 ACTIVE")

    while True:
        q = input("VASUKI> ")
        if q in ["exit", "quit"]:
            break

        print(api.ask(q))


if __name__ == "__main__":
    main()
