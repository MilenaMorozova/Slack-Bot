import logging

from flask import Flask, request

from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

from bot_manifest.constants import SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET
from storage.users_storage import GithubToSlackUsersStorage
from storage.repository_storage import RepositoryStorage

logging.basicConfig(level=logging.DEBUG)

app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

users_storage = GithubToSlackUsersStorage()
repository_storage = RepositoryStorage()


@app.middleware
def log_request(logger, body, next):
    logger.debug(body)
    return next()


@app.command("/mention-me")
def mention_slack_user(ack, body):
    slack_username = body["user_name"]
    github_username = body["text"]
    users_storage.add_github_username(github_username, slack_username)
    ack(f"<@{slack_username}> you are successfully subscribed!")


@app.command("/stop-mention-me")
def stop_mention_slack_user(ack, body):
    slack_username = body["user_name"]
    users_storage.delete_github_user(slack_username)
    ack(f"<@{slack_username}> you are successfully unsubscribed!")


@app.command("/subscribe-channel")
def subscribe_channel(ack, body):
    channel_id = body["channel_id"]
    github_repository = body["text"]
    repository_storage.add_repository_to_channel(channel_id, github_repository)
    ack(f"<This channel are successfully subscribed to repository <{github_repository}>!")


@app.command("/unsubscribe-channel")
def unsubscribe_channel(ack, body):
    channel_id = body["channel_id"]
    github_repository = body["text"]
    repository_storage.unsubscribe_channel_from_repository(channel_id, github_repository)
    ack(f"<This channel are successfully unsubscribed to repository <{github_repository}>!")


@app.command("/unsubscribe-channel-from-all-repositories")
def unsubscribe_channel_from_all_repositories(ack, body):
    channel_id = body["channel_id"]
    repository_storage.unsubscribe_channel_from_all_repository(channel_id)
    ack(f"This channel are successfully unsubscribed from all repositories")


@app.command("/channel-repositories")
def channel_is_subscribed_to_repositories(ack, body):
    channel_id = body["channel_id"]
    repositories = repository_storage.get_repositories_by_channel_id(channel_id)
    if not repositories:
        ack("No repository are subscribed")
    ack("\n".join(["Repositories:"] + repositories))


@flask_app.route("/slack/command/<command>", methods=["POST"])
def slack_command(command):
    return handler.handle(request)


if __name__ == '__main__':
    flask_app.run(port=3000)
