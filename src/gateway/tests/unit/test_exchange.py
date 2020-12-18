from gateway.services import exchange


class TaskLog:
    def send(self, msg):
        print(msg)


class MsgSender:
    def send(self, msg):
        return msg


def test_exchange():
    exc = exchange.get_exchange('test_exchange')
    log = TaskLog()
    exc.attach(log)
    msg_sender = MsgSender()
    exc.attach(msg_sender)
    msg_sender.send('test message')
    exc.detach(msg_sender)
    exc.detach(log)

