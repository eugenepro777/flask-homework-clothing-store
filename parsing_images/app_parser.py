import os
import time
import threading
import multiprocessing
import asyncio
import argparse
import requests
import aiohttp

IMAGE_FOLDER = './parsing_images/images'


def download_image_sync(url):
    response = requests.get(url)
    if not os.path.exists(IMAGE_FOLDER):
        os.mkdir(IMAGE_FOLDER)
    if response.status_code == 200:
        save_path = os.path.join(IMAGE_FOLDER, os.path.basename(url))
        with open(save_path, "wb") as f:
            f.write(response.content)


async def download_image_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if not os.path.exists(IMAGE_FOLDER):
                os.mkdir(IMAGE_FOLDER)
            if response.status == 200:
                save_path = os.path.join(IMAGE_FOLDER, os.path.basename(url))
                with open(save_path, "wb") as f:
                    f.write(await response.read())


async def download_images_asynchronous(urls):
    await asyncio.gather(*(download_image_async(url) for url in urls))
