import asyncio

import aiohttp

import api
import file_ids


async def main():
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": "",
    }
    async with aiohttp.ClientSession() as session:
        file_ids = await file_ids.get_file_ids(session)
        mod_files = await api.get_mod_files(session, "https://api.curseforge.com/v1/mods/files", headers, file_ids)
        downloads = (
            asyncio.create_task(api.download_mod_file(session, file.download_url, file.file_name)) for file in mod_files
        )
        downloads_status = await asyncio.gather(*downloads)
        if all(downloads_status):
            print("All downloads finished successfully")
        else:
            print("Error downloading some mods")


if __name__ == "__main__":
    asyncio.run(main())
