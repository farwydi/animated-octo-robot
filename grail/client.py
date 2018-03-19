import asyncio

from protocol import GrailProtocol

SERVER_PORT = 61589


async def tcp_echo_client(message, loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', SERVER_PORT,
                                                   loop=loop)

    writer.write(GrailProtocol.pack("REG"))
    writer.write(GrailProtocol.pack("farwydi", 35))

    print('Close the socket')
    writer.close()


message = 'HELLO'
loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(message, loop))
loop.close()
