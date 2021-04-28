from users.models import User
from backend_test.celery import app


@app.task
def send_menu_link_to_all_users(base_url):
    # TODO: filter chilean employees
    for user in User.objects.all():
        # TODO: send messages in bulk?
        user.send_menu_link_to_slack(base_url)
