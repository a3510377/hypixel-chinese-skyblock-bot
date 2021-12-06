from hypixel_chinese_skyblock_bot.Core.Common import get_setting_json


class UserData:
    def __init__(self, user):
        self.id = user

        self.discord = ''

        self.uuid = ''

        self.api = {}

        self.profile = {}

        self.skyblock_api = {}

        self.dung_class_level = {
            'healer': 0,
            'mage': 0,
            'berserk': 0,
            'archer': 0,
            'tank': 0
        }

        self.dung_level = {
            'catacombs': 0
        }

        self.slayer_is_max = {
            7: False,
            8: False,
            9: False
        }

        self.skill_is_max = {
            'taming': False,
            'farming': False,
            'mining': False,
            'combat': False,
            'foraging': False,
            'fishing': False,
            'enchanting': False,
            'alchemy': False,
            'carpentry': False
        }

    def set_dung_class_level(self, dung_class, exp):
        xp_to_level_list = get_setting_json('dungeon_xp_to_level')

        for i in range(50, 0, -1):
            if exp >= xp_to_level_list[str(i)]:
                self.dung_class_level[dung_class] = i
                break

        else:
            self.dung_class_level[dung_class] = -1

    def get_dung_class_level(self, dung_class):
        return self.dung_class_level[dung_class]

    def set_dung_level(self, dung, exp):
        xp_to_level_list = get_setting_json('dungeon_xp_to_level')

        for i in range(50, 0, -1):
            if exp >= xp_to_level_list[str(i)]:
                self.dung_level[dung] = i
                break

        else:
            self.dung_level[dung] = -1

    def get_dung_level(self, dung):
        return self.dung_level[dung]

    def get_dung_class_is_max(self, dung_class):
        return self.dung_class_level[dung_class] >= 50

    def set_slayer_level_is_max(self, num, boolean):
        if 7 <= num <= 9:
            self.slayer_is_max[num] = boolean

    def get_slayer_level_is_max(self, num):
        return self.slayer_is_max[num]

    def set_skill_level_is_max(self, skill, boolean):
        if skill in self.skill_is_max:
            self.skill_is_max[skill] = boolean

    def get_skill_level_is_max(self, skill):
        return self.skill_is_max[skill]