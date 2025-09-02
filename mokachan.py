# Ref: https://nullprogram.com/blog/2019/03/22/
import asyncio
from asyncio.streams import StreamReader, StreamWriter
import random
import os
import signal
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def exit_handler(*_args):
    print("Get SIGTERM, exiting...")
    exit(0)


signal.signal(signal.SIGTERM, exit_handler)


async def handler(_reader: StreamReader, writer: StreamWriter):
    peer_addr: tuple[str, int] = writer.get_extra_info("peername")
    random_large_size = str(random.randint(10**6, 10**12)).encode()
    logger.info("Connection from: %s", peer_addr)
    writer.write(b"HTTP/1.1 200 OK\r\n")
    writer.write(b"Content-Type: application/octet-stream\r\n")
    writer.write(b"Content-Length:" + random_large_size + b"\r\n\r\n")

    async def connection_logic():
        while True:
            await asyncio.sleep(1)
            byte = random.randint(0, 2**8 - 1)
            writer.write(bytes([byte]))
            try:
                await asyncio.wait_for(writer.drain(), timeout=5)
            except asyncio.TimeoutError:
                logger.info("Bye (timeout): %s", peer_addr)
                break

    try:
        await asyncio.wait_for(connection_logic(), timeout=60 * 5)
    except asyncio.TimeoutError:
        logger.info("Bye (5-minute timeout exceeded): %s", peer_addr)
    except ConnectionResetError:
        logger.info("Bye (reset): %s", peer_addr)
    except Exception as e:
        logger.info("Bye (exception): %s", peer_addr, e)


async def main():
    server = await asyncio.start_server(
        handler, os.environ.get("HOST", "127.0.0.1"), int(os.environ.get("PORT", 6571))
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
