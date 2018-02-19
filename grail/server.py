# import asyncio
#
#
# class GrailProtocol(asyncio.Protocol):
#     def __init__(self):
#         self.transport = None
#
#     def connection_made(self, transport):
#         self.transport = transport
#
#     def data_received(self, data):
#         print(data.decode())
#         self.transport.write(data)
#
#
# loop = asyncio.get_event_loop()
# coro = loop.create_server(
#     GrailProtocol,
#     '127.0.0.1', 8181
# )
#
# server = loop.run_until_complete(coro)
#
# try:
#     loop.run_forever()
# except KeyboardInterrupt:
#     pass
#
# server.close()
# loop.run_until_complete(server.wait_closed())
# loop.close()

import asyncio

import asyncpg


async def run(loop):
    conn = await asyncpg.connect("postgres://postgres:y0dsqgfh0km@pg9devel.immo/tracker", loop=loop)
    print("connect done")
    values = await conn.fetch("""SELECT * FROM public.records LIMIT 50""")
    print("f1")
    values1 = await conn.fetch("""SELECT * FROM public.records LIMIT 25""")
    print("fetch done")
    for row in values:
        print(row["id"])

    await conn.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))
print("aaaa")
loop.close()
