import time
import praw
import os
from prawcore import exceptions
from dotenv import load_dotenv
from loguru import logger

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))
ignored_subreddits = ["legaladviceofftopic"]
logger.add("laukopier.log")

client = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    password=os.getenv("BOTPASSWORD"),
    user_agent=os.getenv("USER_AGENT"),
    username=os.getenv("BOTNAME")
)


def valid_submission(submission, target):
    # Self posts in BOLA never need to be copied.
    if submission.is_self:
        return False

    if target.subreddit in ignored_subreddits:
        return False

    if not target.is_self:
        return False

    return True


def format_message(self_text, title):
    body = self_text.split("\n\n")
    newbody = []
    for element in body:
        newbody.append("\n \n> " + element)

    body = "".join(newbody)

    header = "**Reminder:** Do not participate in threads linked here." \
             " If you do, you may be banned from both subreddits." \
             "\n\n --- \n\n" \
             "Title: " + title + "\n\n" + "Body: \n\n"
    footer = "\n\n This bot was created to capture original threads" \
             " and is not affiliated with the mod team." \
             "\n\n [Concerns? Bugs?](https://www.reddit.com/message/compose/?to=GrahamCorcoran)" \
             " | [Laukopier 2.1](https://github.com/GrahamCorcoran/Laukopier)"

    return f"{header}{body}{footer}"


def main():
    logger.info("Started successfully.")
    bola = client.subreddit(os.getenv("TARGET_SUBREDDIT"))

    while True:
        try:
            for submission in bola.stream.submissions(skip_existing=True):
                target = client.submission(url=submission.url)
                if valid_submission(submission, target):
                    message = format_message(target.selftext, target.title)
                    laukopier_comment = submission.reply(message)
                    laukopier_comment.mod.distinguish(sticky=True)
                    logger.info(f"Replied: {target.title}")

        except KeyboardInterrupt:
            break
        except exceptions.PrawcoreException:
            logger.exception("Sleep for 60 seconds.")
            time.sleep(60)
        except Exception:
            logger.exception("PROGRAM FAILED")
            raise


if __name__ == "__main__":
    main()
