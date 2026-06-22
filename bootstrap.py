from api.ask import ask
from services.response_composer import compose_response


def main():
    print("VASUKI v2 ACTIVE")
    print("Type a request. Type 'exit' or 'quit' to close.")

    while True:
        try:
            query = input("VASUKI> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nVASUKI stopped.")
            break

        if not query:
            continue

        if query.lower() in {"exit", "quit"}:
            print("VASUKI stopped.")
            break

        result = ask(query)
        print()
        print(compose_response(result))
        print()


if __name__ == "__main__":
    main()
