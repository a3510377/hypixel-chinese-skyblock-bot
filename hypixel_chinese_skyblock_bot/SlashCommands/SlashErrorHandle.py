import logging

import disnake
from disnake.ext import commands

from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_setting_json
from hypixel_chinese_skyblock_bot.Core.Logger import Logger

bot_logger = Logger(__name__)


class SlashErrorHandle(CodExtension):
    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: disnake.AppCommandInteraction, error: commands.CommandError):
        if inter is not None:
            user_name = inter.author.name
        else:
            user_name = '未知使用者'

        bot_logger.log_message(logging.ERROR, f'{user_name} 使用 slash command 出現錯誤 : {error}')

        channel = self.bot.get_channel(get_setting_json('ErrorMessageChannel'))

        if isinstance(error, commands.CommandNotFound):
            message = '未知指令!'

        elif isinstance(error, commands.CommandOnCooldown):
            message = f'此指令在冷卻中。 請在 {round(error.retry_after, 1)} 秒後重試'

        elif isinstance(error, commands.MissingPermissions):
            message = '你沒有權限使用該指令!'

        elif isinstance(error, commands.UserInputError):
            message = '你的輸入內容有誤, 請檢查你的輸入內容!'

        else:
            message = '運行該命令時發生未知錯誤!'

        embed = disnake.Embed(
            title='錯誤狀況',
            description=message,
            color=0xe74c3c
        )

        await channel.send(embed=embed, delete_after=20.0)


def setup(pybot):
    pybot.add_cog(SlashErrorHandle(pybot))
