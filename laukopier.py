import time
import praw
from dotenv import dotenv_values
import logging
import logging.handlers

config = dotenv_values(".env")

log = logging.getLogger("bot")
log.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(levelname)s: %(message)s')
log_formatter_file = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_std_err_handler = logging.StreamHandler()
log_std_err_handler.setFormatter(log_formatter)
log.addHandler(log_std_err_handler)
if config["LOG_FILENAME"] is not None:
    log_file_handler = logging.handlers.RotatingFileHandler(
        config["LOG_FILENAME"],
        maxBytes=int(config["LOG_FILE_MAXSIZE"]),
        backupCount=int(config["LOG_FILE_BACKUPCOUNT"])
    )
    log_file_handler.setFormatter(log_formatter_file)
    log.addHandler(log_file_handler)

client = praw.Reddit(
    client_id=config["CLIENT_ID"],
    client_secret=config["CLIENT_SECRET"],
    password=config["PASSWORD"],
    user_agent=config["USER_AGENT"],
    username=config["USERNAME"]
)


def valid_submission(client, submission):
    # Self posts in BOLA never need to be copied.
    if submission.is_self:
        return False

    url = submission.url


def main():
    bola = client.subreddit("bestoflegaladvice")
    while True:
        try:
            stream = bola.stream.submissions(skip_existing=True)
        except KeyboardInterrupt:
            break
        except Exception as e:
            log.error("Exception %s", e, exc_info=True)
            log.info("Sleep for 15 seconds.")
            time.sleep(15)



if __name__ == "__main__":
    main()