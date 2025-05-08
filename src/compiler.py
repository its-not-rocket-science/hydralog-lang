from lexer import tokenize

def main():
    with open("examples/low_pass_filter.hyd") as f:
        source = f.read()
    tokens = tokenize(source)
    for token in tokens:
        print(token)

if __name__ == "__main__":
    main()
