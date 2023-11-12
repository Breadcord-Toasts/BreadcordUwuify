from collections.abc import Sequence
from typing import Any

import discord
import discord.abc
import uwuify

import breadcord


def owoify(text: str) -> str:
    return uwuify.uwu(text)


def uwuify_embed(embed: discord.Embed) -> discord.Embed:
    if embed.title:
        embed.title = owoify(embed.title)
    if embed.description:
        embed.description = owoify(embed.description)
    if embed.footer:
        embed.set_footer(text=owoify(embed.footer.text))
    if embed.author:
        embed.set_author(name=owoify(embed.author.name))
    if hasattr(embed, "_fields"):
        # noinspection PyProtectedMember
        embed._fields = [
            {
                key: owoify(value)
                for key, value in field.items()
            }
            for field in embed._fields
        ]
    return embed


async def uwu_send(
    self,
    content: str = None,
    *args: Any,
    embed: discord.Embed | None = None,
    embeds: Sequence[discord.Embed] | None = None,
    **kwargs: Any
) -> discord.Message:
    if embed is not None:
        embed = uwuify_embed(embed)
    if embeds is not None:
        embeds = [uwuify_embed(embed) for embed in embeds]

    # noinspection PyUnresolvedReferences
    return await self._original_send(
        owoify(content) if content else content,
        *args,
        embed=embed,
        embeds=embeds,
        **kwargs
    )


class ColonThree(breadcord.module.ModuleCog):
    async def cog_load(self) -> None:
        discord.abc.Messageable._original_send = discord.abc.Messageable.send
        discord.abc.Messageable.send = uwu_send

    # noinspection PyProtectedMember,PyUnresolvedReferences
    async def cog_unload(self) -> None:
        discord.abc.Messageable.send = discord.abc.Messageable._original_send
        del discord.abc.Messageable._original_send


async def setup(bot: breadcord.Bot):
    await bot.add_cog(ColonThree("colon_three"))
