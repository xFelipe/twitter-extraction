from api import search_tweets
from persistence import save


if __name__ == "__main__":
    for index, result in enumerate(search_tweets("Lula")):
        save(result)
        if index > 4:
            break
