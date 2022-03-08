import json
from dataclasses import dataclass
from enum import IntEnum

import aiofiles
import aiohttp


@dataclass(slots=True)
class FileResponse:
    file_name: str
    download_url: str


async def get_mod_files(
    session: aiohttp.ClientSession, url: str, headers: dict, file_ids: list[int]
) -> list[FileResponse]:
    async with session.post(url, headers=headers, json={"fileIds": file_ids}) as resp:
        return list(
            map(
                lambda item: FileResponse(file_name=item["fileName"], download_url=item["downloadUrl"]),
                json.loads(await resp.text())["data"],
            )
        )


async def download_mod_file(session: aiohttp.ClientSession, url: str, file_name: str) -> int:
    print(f"Downloading {file_name}")
    async with (session.get(url) as file_data, aiofiles.open(f"mods/{file_name}", "wb") as file):
        async for chunk in file_data.content.iter_chunked(1024):
            await file.write(chunk)
    print(f"Finished {file_name}")
    return (file_name, 1)
