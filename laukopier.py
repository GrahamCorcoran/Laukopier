import praw
import database
from dotenv import dotenv_values


def initialize():
    config = dotenv_values(".env")
    reddit = praw.Reddit(
        client_id=config["CLIENT_ID"],
        client_secret=config["CLIENT_SECRET"],
        password=config["PASSWORD"],
        user_agent=config["USER_AGENT"],
        username=config["USERNAME"]
    )

    return reddit


def main():
    client = initialize()



if __name__ == "__main__":
    main()