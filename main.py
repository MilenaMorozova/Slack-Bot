# from flask import Flask, request
#
# from datetime import datetime
#
# from github_api.app import add_routs, get_event_controller
#
#
# TOKEN = "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"
# REPO_NAME = "MilenaMorozova/Slack-Bot"
#
#
# app = Flask(__name__)
#
# add_routs(app)
#
# event = get_event_controller()
#
# event.on_open_pull_request.append(lambda x: print(x.title + 'Opened'))
# event.on_edit_pull_request.append(lambda x: print(x.title + 'Edited'))

from datetime import datetime, timedelta

if __name__ == '__main__':
    a = datetime.now().timestamp()
    pass
    # app.run(port=80)
