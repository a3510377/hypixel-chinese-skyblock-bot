import discord
from discord.ext import commands
from hypixel_chinese_skyblock_bot.Core.Common import CodExtension, get_hypixel_api, get_setting_json, \
    get_verify_id_list, get_hypixel_skyblock_api
from hypixel_chinese_skyblock_bot.Core.UserData import UserData


class VerifyDungeoneer(CodExtension):

    @commands.command()
    async def verifydung(self, ctx):
        # check is player has been verified
        if get_setting_json('VerifyIdRole') in [y.name.lower() for y in ctx.message.author.roles]:
            role = discord.utils.get(ctx.message.author.guild.roles, name=get_setting_json('DungeoneerRole'))

            await ctx.author.add_roles(role)

            player = get_verify_id_list(ctx.message.author)

            player_api = get_hypixel_api(player)

            print('> verify player dungeoneer : ' + str(ctx.message.author))

            # check get hypixel api is successes
            if player_api['success']:
                print('> get hypixel api success')

                # try to get profile data and max class data
                try:
                    player_dung_max_level = player_api['player']['achievements']['skyblock_dungeoneer']

                    print('- ' + str(player_dung_max_level))

                    player_uuid = player_api['player']['uuid']

                    player_profile = player_api['player']['stats']['SkyBlock']['profiles']

                    # loop for checking all profile
                    for profileId in player_profile:
                        is_class_level_get_success = False

                        is_dung_level_get_success = False

                        print('- 正在驗證'
                              + player_profile[profileId]['cute_name']
                              )

                        player_data = UserData(player)

                        embed = discord.Embed(
                            title='驗證處理中',
                            description='正在驗證 -> '
                                        + player_profile[profileId]['cute_name'],
                            color=0xf1c40f
                        )

                        embed.set_author(
                            name=ctx.message.author.name,
                            icon_url=ctx.message.author.avatar_url
                        )

                        await ctx.send(embed=embed, delete_after=10.0)

                        # try to get skyblock api
                        try:
                            skyblock_api = get_hypixel_skyblock_api(profileId)

                            print('> get api success')

                            # check get skyblock api is successes
                            if skyblock_api['success']:
                                dung_api = skyblock_api['profile']['members'][player_uuid]['dungeons']

                                # get dungeon classes level
                                try:
                                    for dungClass in dung_api['player_classes']:
                                        class_exp = dung_api['player_classes'][dungClass]['experience']

                                        print('- ' + dungClass + ' : ' + str(class_exp))

                                        player_data.set_dung_class_level(dungClass, class_exp)

                                    is_class_level_get_success = True

                                except:
                                    print('> fail at get class level')

                                # get dungeon level
                                try:
                                    for dung in player_data.dungLevel:
                                        dung_exp = dung_api['dungeon_types'][dung]['experience']

                                        print('- ' + dung + ' : ' + str(dung_exp))

                                        player_data.set_dung_level(dung, dung_exp)

                                        dung_level = player_data.get_dung_level(dung)

                                        if dung_level > player_dung_max_level:
                                            player_dung_max_level = dung_level

                                    is_dung_level_get_success = True

                                except:
                                    print('> fail at get dung level')

                            else:
                                print('>　Please wait a little bit and try again')

                                embed = discord.Embed(
                                    title='驗證失敗，請稍後重試',
                                    description=player_profile[profileId]['cute_name'] + ' -x-> Dungeoneer',
                                    color=0xe74c3c
                                )

                                embed.set_author(
                                    name=ctx.message.author.name,
                                    icon_url=ctx.message.author.avatar_url
                                )

                                await ctx.send(embed=embed, delete_after=20.0)

                        except:
                            print('> fail to get skyblock api in ' + str(player_profile[profileId]['cute_name']))

                        # create embed
                        try:
                            if is_class_level_get_success and is_dung_level_get_success:
                                desc = ':trophy: 最高地下城等級 : ' \
                                       + str(player_dung_max_level) \
                                       + '\n\n===============\n\n:island: 島嶼職業等級 :\n\n'

                                for dungClass in player_data.dungClassLevel:
                                    print('- '
                                          + dungClass
                                          + ' : '
                                          + str(player_data.get_dung_class_level(dungClass))
                                          )

                                    dung_class_list = get_setting_json('dung_class_list')

                                    desc = desc + ' - ' \
                                                + dung_class_list[dungClass] \
                                                + ' : ' \
                                                + str(player_data.get_dung_class_level(dungClass)) \
                                                + '\n\n'

                                desc += '===============\n\n:classical_building: 地下城等級 : \n\n'

                                for dung in player_data.dungLevel:
                                    print(dung
                                          + ' : '
                                          + str(player_data.get_dung_level(dung))
                                          )

                                    dung_list = get_setting_json('dung_list')

                                    desc = desc + ' - ' \
                                                + dung_list[dung] \
                                                + ' : ' \
                                                + str(player_data.get_dung_level(dung)) \
                                                + '\n\n'

                                embed = discord.Embed(
                                    title=player_profile[profileId]['cute_name'] + ' 已更新地下城',
                                    description=str(desc),
                                    color=0x00ff00
                                )

                                embed.set_author(
                                    name=ctx.message.author.name,
                                    icon_url=ctx.message.author.avatar_url
                                )

                                await ctx.send(embed=embed)

                            else:
                                embed = discord.Embed(
                                    title='驗證 '
                                          + player_profile[profileId]['cute_name'] + ' 失敗，請打開該島api',
                                    description=player_profile[profileId]['cute_name'] + ' -x-> Dungeoneer',
                                    color=0xe74c3c
                                )

                                embed.set_author(
                                    name=ctx.message.author.name,
                                    icon_url=ctx.message.author.avatar_url
                                )

                                await ctx.send(embed=embed, delete_after=20.0)

                        except:
                            print('> fail at create index embed')

                    # give role
                    try:
                        for i in range(10):
                            if i < 5:
                                i = str(i)

                                role = discord.utils.get(ctx.message.author.guild.roles, name='< ' + i)

                                await ctx.author.remove_roles(role)

                            i = str(i)

                            role = discord.utils.get(ctx.message.author.guild.roles, name=i + ' >')

                            await ctx.author.remove_roles(role)
                        if player_dung_max_level >= 50:
                            role = discord.utils.get(ctx.message.author.guild.roles,
                                                     name=get_setting_json('cata50'))

                            await ctx.author.add_roles(role)

                        else:
                            role = discord.utils.get(ctx.message.author.guild.roles,
                                                     name='< ' + str(player_dung_max_level // 10))

                            await ctx.author.add_roles(role)

                            role = discord.utils.get(ctx.message.author.guild.roles,
                                                     name=str(player_dung_max_level % 10) + ' >')

                            await ctx.author.add_roles(role)

                    except:
                        print('> fail at give role')


                except:
                    print('> The player do not open the social media')

                    embed = discord.Embed(
                        title='驗證失敗，請先打開 hypixel discord api',
                        description=str(ctx.message.author) + ' -x-> Dungeoneer',
                        color=0xe74c3c
                    )

                    embed.set_author(
                        name=ctx.message.author.name,
                        icon_url=ctx.message.author.avatar_url
                    )

                    await ctx.send(embed=embed, delete_after=20.0)
            else:
                print('> Please wait a little bit and try again')

                print('> fail reason : ' + player_api['cause'])

                embed = discord.Embed(
                    title='驗證失敗，請稍後重試',
                    description=str(ctx.message.author) + ' -x-> Dungeoneer\n\n' + '原因 : ' + player_api['cause'],
                    color=0xe74c3c
                )

                embed.set_author(
                    name=ctx.message.author.name,
                    icon_url=ctx.message.author.avatar_url
                )

                await ctx.send(embed=embed, delete_after=20.0)

        else:
            print('> Require verify id')

            embed = discord.Embed(
                title='你未登記id，請先登記id',
                description=str(ctx.message.author) + ' -x-> Dungeoneer',
                color=0xe74c3c
            )

            embed.set_author(
                name=ctx.message.author.name,
                icon_url=ctx.message.author.avatar_url
            )

            await ctx.send(embed=embed, delete_after=20.0)

        await ctx.message.delete()


def setup(pybot):
    pybot.add_cog(VerifyDungeoneer(pybot))
