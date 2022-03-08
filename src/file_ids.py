import re

import aiohttp
from bs4 import BeautifulSoup


async def get_file_ids(session: aiohttp.ClientSession) -> list[int]:
    mod_id_pattern = re.compile(r"(\/)(\d{7})")

    async with session.get("https://github.com/TeamAOF/All-of-Fabric-5/blob/main/MODLIST.md") as mods_ids_file:
        soup = BeautifulSoup(await mods_ids_file.text(), "lxml")
        mods_list = soup.select_one("#readme > article > ul")
        mods = mods_list.find_all("li")

        return list(
            map(
                lambda mod: int(mod.group(2)),
                filter(lambda mod_id: mod_id is not None, mod_id_pattern.finditer(str(mods))),
            )
        )
