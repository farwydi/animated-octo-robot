import asyncio
import os.path
import sqlite3

from protocol import GrailProtocol

SERVER_PORT = 61589


async def handle_echo(reader, writer):
    while True:
        command = GrailProtocol.un_puck(await reader.read(15))

        if len(command) == 0:
            break

        print(f"CMD {command}")

        if command == "REG":
            login = GrailProtocol.un_puck(await reader.read(35))
            print(f"login: {login}")

            c_db.execute("INSERT INTO users (login, user_public_key, secret_key) VALUES (?, 'a', 'b')", (login,))
            conn_db.commit()

    # addr = writer.get_extra_info('peername')
    # print("Received %r from %r" % (message, addr))
    #
    # print("Send: %r" % message)
    # writer.write(data)
    # await writer.drain()
    #
    print("Close the client socket")
    writer.close()


if __name__ == '__main__':

    if not os.path.isfile('users.db'):
        conn_db = sqlite3.connect('users.db')
        c_db = conn_db.cursor()
        c_db.execute("""CREATE TABLE users (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            user_public_key TEXT NOT NULL UNIQUE,
            secret_key TEXT NOT NULL UNIQUE
        )""")
        conn_db.commit()
    else:
        conn_db = sqlite3.connect('users.db')
        c_db = conn_db.cursor()

    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_echo, '127.0.0.1', SERVER_PORT, loop=loop)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

    conn_db.close()
