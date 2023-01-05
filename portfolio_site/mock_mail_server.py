from aiosmtpd.controller import Controller

from aiosmtpd.smtp import Envelope


class MockHandler:
    async def handle_RCPT(self, server, session, envelope: Envelope, address: str, rcpt_options):
        if address.endswith('@localhost'):
            envelope.rcpt_tos.append(address)
            return '250 OK'
        else:
            return '550 Invalid recipient domain'

    async def handle_DATA(self, server, session, envelope: Envelope):
        print(f'Received message:\n{envelope.content.decode("utf8")}')
        return '250 Message accepted for delivery'



print('Starting mail server')
mock_server = Controller(MockHandler())
mock_server.start()
