import json
import logging
from dataclasses import asdict

import pulsar

from common.domain_events import DomainEvent

client = pulsar.Client('pulsar://localhost:6650')
producer = client.create_producer('my-topic')

logger = logging.getLogger(__name__)


def publish(channel, event: DomainEvent):
    logging.debug('publishing: channel=%s, event=%s', channel, event)
    producer.publish(channel, json.dumps(asdict(event)))
