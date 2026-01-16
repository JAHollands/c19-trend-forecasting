from src.extract import extract
from src.transform import transform

def main():
    # run the extract step
    extract()
    transform()

if __name__ == "__main__":
    main()