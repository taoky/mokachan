# Ref: https://nullprogram.com/blog/2019/03/22/
import asyncio
from asyncio.streams import StreamReader, StreamWriter
import random
import os
import signal


def exit_handler(*_args):
    print("Get SIGTERM, exiting...")
    exit(0)


signal.signal(signal.SIGTERM, exit_handler)


async def handler(_reader: StreamReader, writer: StreamWriter):
    peer_addr: tuple[str, int] = writer.get_extra_info("peername")
    print("Connection from", peer_addr)
    writer.write(b"HTTP/1.1 200 OK\r\n")
    writer.write(b"Content-Type: application/octet-stream\r\n")
    writer.write(b"Content-Length: 1145141919810\r\n\r\n")

    async def connection_logic():
        while True:
            await asyncio.sleep(1)
            byte = random.randint(0, 2**8 - 1)
            writer.write(bytes([byte]))
            try:
                await asyncio.wait_for(writer.drain(), timeout=5)
            except asyncio.TimeoutError:
                print("Bye (timeout)", peer_addr)
                break

    try:
        await asyncio.wait_for(connection_logic(), timeout=60 * 5)
    except asyncio.TimeoutError:
        print("Bye (5-minute timeout exceeded)", peer_addr)
    except ConnectionResetError:
        print("Bye (reset)", peer_addr)
    except Exception as e:
        print("Bye (exception)", peer_addr, e)


async def main():
    server = await asyncio.start_server(
        handler, "0.0.0.0", int(os.environ.get("PORT", 6571))
    )
    async with server:
        try:
            await server.serve_forever()
        except asyncio.CancelledError:
            pass
        finally:
            server.close()
            await server.wait_closed()


asyncio.run(main())
