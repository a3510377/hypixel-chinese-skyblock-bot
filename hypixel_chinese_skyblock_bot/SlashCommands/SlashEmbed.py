import logging

import disnake
from disnake.ext import commands

from CoreFunction.Common import CodExtension, get_setting_json
from CoreFunction.Logger import Logger

bot_logger = Logger(__name__)


class SlashEmbed(CodExtension):
    @commands.slash_command(
        guild_ids=[int(get_setting_json('ServerId'))],
        name='embed',
        description='Build a embed'
    )
    async def embed(self,
                    inter: disnake.AppCommandInteraction,
                    title: str = commands.Param(description='Makes the title of the embed', default=None),
                    description: str = commands.Param(description='Makes the description', default=None),
                    color: str = commands.Param(description='Makes the description', default=None),
                    picture: str = commands.Param(description='The picture url of the embed', default=None)
                    ):
        await inter.response.defer()

        if color is not None:
            try:
                color = await commands.ColorConverter().convert(inter, color)
            except KeyError:
                bot_logger.log_message(logging.ERROR, f'顏色錯誤')

                color = None

        else:
            color = disnake.Color.default()

        embed = disnake.Embed(color=color)

        if title is not None:
            embed.title = title

        if description is not None:
            embed.description = description

        if picture is not None:
            embed.set_image(url=picture)

        await inter.edit_original_message(embed=embed)


def setup(pybot):
    pybot.add_cog(SlashEmbed(pybot))
