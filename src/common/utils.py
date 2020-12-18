from datetime import datetime
from uuid import uuid4


def generate_event_id():
    return datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())