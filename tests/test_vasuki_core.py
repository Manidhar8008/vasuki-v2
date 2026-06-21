from api.ask import ask

TEST_QUERIES = [
    "system status health check",
    "GitHub repository status and latest commit",
    "plan a project to improve Vasuki",
    "mentor me to learn Python",
    "search my memory for hello",
]

def main():
    passed = 0

    for query in TEST_QUERIES:
        print("\n" + "=" * 70)
        print("QUERY:", query)

        try:
            result = ask(query)
            print("TOOLS:", result.get("selected_tools"))
            print("RESULT:", result.get("results"))
            passed += 1
        except Exception as error:
            print("FAILED:", type(error).__name__, str(error))

    print("\n" + "=" * 70)
    print(f"VASUKI CORE TEST: {passed}/{len(TEST_QUERIES)} completed")

if __name__ == "__main__":
    main()
