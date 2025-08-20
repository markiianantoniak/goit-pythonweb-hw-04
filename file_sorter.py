import argparse
import asyncio
import logging
import os
from pathlib import Path

import aiofiles.os
import shutil



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)


async def copy_file(src: Path, dest_folder: Path):
    try:
        ext = src.suffix.lower()[1:] or "no_extension"
        target_dir = dest_folder / ext
        await aiofiles.os.makedirs(target_dir, exist_ok=True)

        target_path = target_dir / src.name

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, shutil.copy2, src, target_path)

        logging.info(f"Файл {src} → {target_path}")

    except Exception as e:
        logging.error(f"Помилка копіювання {src}: {e}")


async def read_folder(src_folder: Path, dest_folder: Path):
    tasks = []

    for root, _, files in os.walk(src_folder):
        for file in files:
            file_path = Path(root) / file
            tasks.append(copy_file(file_path, dest_folder))

    await asyncio.gather(*tasks)


async def main():
    parser = argparse.ArgumentParser(
        description="Сортує файли за розширеннями у цільовій папці."
    )
    parser.add_argument(
        "source", type=str, help="Вихідна папка (source folder)"
    )
    parser.add_argument(
        "output", type=str, help="Цільова папка (output folder)"
    )

    args = parser.parse_args()

    src_folder = Path(args.source)
    dest_folder = Path(args.output)

    if not src_folder.exists():
        logging.error(f"Вихідна папка {src_folder} не існує")
        return

    await read_folder(src_folder, dest_folder)


if __name__ == "__main__":
    asyncio.run(main())
