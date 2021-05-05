import time
import praw
from dotenv import dotenv_values
import logging
import logging.handlers

config = dotenv_values(".env")
ignored_subreddits = ["legaladvice", "legaladviceofftopic"]

# Logging info.
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


def valid_submission(submission, target):
    # Self posts in BOLA never need to be copied.
    if submission.is_self:
        return False

    if target.subreddit in ignored_subreddits:
        return False

    return True


def format_message(self_text, title):
    body = self_text.split("\n\n")
    newbody = []
    for element in body:
        newbody.append("\n \n> " + element)

    header = "**Reminder:** Do not participate in threads linked here." \
             " If you do, you may be banned from both subreddits." \
             "\n\n --- \n\n" \
             "Title: " + title + "\n\n" + "Body: \n\n"
    footer = "\n\n This bot was created to capture threads missed by LocationBot" \
             " and is not affiliated with the mod team." \
             "\n\n [Concerns? Bugs?](https://www.reddit.com/message/compose/?to=laukopier)" \
             " | [GitHub](https://github.com/GrahamCorcoran/Laukopier)"

    return f"{header}{newbody}{footer}"


def main():
    bola = client.subreddit("bestoflegaladvice")
    while True:
        try:
            for submission in bola.stream.submissions(skip_existing=True):
                target = client.submission(url=submission.url)
                if valid_submission(submission, target):
                    message = format_message(target.self_text, target.title)

        except KeyboardInterrupt:
            break
        except Exception as e:
            log.error("Exception %s", e, exc_info=True)
            log.info("Sleep for 15 seconds.")
            time.sleep(15)


if __name__ == "__main__":
    main()
