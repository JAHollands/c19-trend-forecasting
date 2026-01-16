from src.extract import extract
from src.transform import transform
from src.model import model

def main():
    extract()
    transform()
    model()

if __name__ == "__main__":
    main()