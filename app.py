import logging

from flask import Flask, request

from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from typing import List

from bot_manifest.constants import SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET
from message_template.message_builder import MessageBuilder
from storage.users_storage import GithubToSlackUsersStorage
from storage.repository_storage import RepositoryStorage
from github_api import add_routs, get_event_controller, PullRequest, User

logging.basicConfig(level=logging.DEBUG)

app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

flask_app = Flask(__name__)
add_routs(flask_app)
handler = SlackRequestHandler(app)

users_storage = GithubToSlackUsersStorage()
repository_storage = RepositoryStorage()

message_builder = MessageBuilder()


@app.middleware
def log_request(logger, body, next):
    logger.debug(body)
    return next()


@app.command("/mention-me")
def mention_slack_user(ack, body):
    slack_user_id = body["user_id"]
    github_username = body["text"]
    users_storage.add_github_username(github_username, slack_user_id)
    ack(f"<@{slack_user_id}> you are successfully subscribed!")


@app.command("/stop-mention-me")
def stop_mention_slack_user(ack, body):
    slack_user_id = body["user_id"]
    users_storage.delete_github_user(slack_user_id)
    ack(f"<@{slack_user_id}> you are successfully unsubscribed!")


@app.command("/subscribe-channel")
def subscribe_channel(ack, body):
    channel_id = body["channel_id"]
    github_repository = body["text"]
    repository_storage.add_repository_to_channel(channel_id, github_repository)
    ack(f"This channel are successfully subscribed to repository <{github_repository}>!")


@app.command("/unsubscribe-channel")
def unsubscribe_channel(ack, body):
    channel_id = body["channel_id"]
    github_repository = body["text"]
    repository_storage.unsubscribe_channel_from_repository(channel_id, github_repository)
    ack(f"This channel are successfully unsubscribed to repository <{github_repository}>!")


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


def convert_reviewers(reviewers: List[User]):
    slack_reviewers = []
    for reviewer in reviewers:
        if users_storage.is_subscribed_github_user(reviewer.login):
            slack_user_id = users_storage.get_slack_user_id_by_github_username(reviewer.login)
            slack_reviewers.append(f"<@{slack_user_id}>")
        else:
            slack_reviewers.append(reviewer.login)

    return slack_reviewers


def send_pr_info_to_channels(pull_request: PullRequest):
    channels = repository_storage.get_channels_by_repository_name(pull_request.repo_full_name)
    reviewers = convert_reviewers(pull_request.reviewers)

    message_blocs = message_builder \
        .set_link_to_pull_request(pull_request.url) \
        .set_pull_request_title(pull_request.title) \
        .set_author(pull_request.author.login) \
        .set_repo_name(pull_request.repo_full_name) \
        .set_create_date(pull_request.created.strftime("%Y-%m-%d %H:%M UTC+0")) \
        .set_update_date(pull_request.updated.strftime("%Y-%m-%d %H:%M UTC+0")) \
        .set_reviewers(reviewers) \
        .build()

    for channel in channels:
        response = app.client.chat_postMessage(
            channel=channel,
            blocks=message_blocs,
            link_names=True
        )
        print(response)


event_controller = get_event_controller()
event_controller.on_open_pull_request.append(send_pr_info_to_channels)
event_controller.on_edit_pull_request.append(send_pr_info_to_channels)


@flask_app.route("/slack/command/<command>", methods=["POST"])
def slack_command(command):
    return handler.handle(request)


if __name__ == '__main__':
    flask_app.run(port=3000)
