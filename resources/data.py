from lib import *


class User:
    @staticmethod
    def get(user_id):
        return DATABASE['users'].get(user_id)
    
    @staticmethod
    def set(user_id, data):
        DATABASE['users'].set(user_id, data)

    @staticmethod
    def add_user(data):
        DATABASE['users'].add(data)
    
    @staticmethod
    def remove_user(user_id):
        DATABASE['users'].remove(user_id)

    


class Guilds:
    @staticmethod
    def get_all():
        return DATABASE["guilds"].read()

    @staticmethod
    def get_guild(guild_id):
        return DATABASE["guilds"].read().get(guild_id)
    
    @staticmethod
    def add_guild(guild_id, prefix):
        guilds = DATABASE["guilds"].read()
        guilds[guild_id] = {"prefix": prefix}
        DATABASE["guilds"].write(guilds)
    
    @staticmethod
    def get_leaderboard():
        guilds = DATABASE["guilds"].read()
        return sorted(guilds.items(), key=lambda x: x[1]["prefix"], reverse=True)

    @staticmethod
    def set_prefix(guild_id, prefix):
        guilds = DATABASE["guilds"].read()
        guilds[guild_id]["prefix"] = prefix
        DATABASE["guilds"].write(guilds)

    @staticmethod
    def remove_balance(user_id, value):
        data = DATABASE["eco"].read()
        data[str(user_id)]["balance"] -= value
        DATABASE["eco"].write(data)


class Eco:
    eco= PickleData(path=DATA_PATH, file='eco.pickle')
    
    def __init__(self, user_id):
        self.eco.load()
        self.user_id = user_id
        self.data = self.eco.read()
        try: self.user = self.data[str(self.user_id)]
        except TypeError:
            dat = {
                "balance": 0,
                "bank": 0,
                "bank_limit": 1000,
                "last_daily": 0,
                "last_weekly": 0,
                "last_monthly": 0,
                "last_yearly": 0,
                }
            self.data[str(self.user_id)] = dat
            DATABASE["eco"].write(self.data)
            self.user = self.data.get(str(self.user_id), None)

    def get_balance(self):
        return self.user["balance"]

    def get_bank(self):
        return self.user["bank"]

    def get_bank_limit(self):
        return self.user["bank_limit"]

    def get_last_daily(self):
        return self.user["last_daily"]

    def get_last_weekly(self):
        return self.user["last_weekly"]

    def get_last_monthly(self):
        return self.user["last_monthly"]

    def get_last_yearly(self):
        return self.user["last_yearly"]

    def set_balance(self, value):
        self.user["balance"] = value
        DATABASE["eco"].write(self.data)

    def set_bank(self, value):
        self.user["bank"] = value
        DATABASE["eco"].write(self.data)

    def set_bank_limit(self, value):
        self.user["bank_limit"] = value
        DATABASE["eco"].write(self.data)

    def set_last_daily(self, value):
        self.user["last_daily"] = value
        DATABASE["eco"].write(self.data)

    def set_last_weekly(self, value):
        self.user["last_weekly"] = value
        DATABASE["eco"].write(self.data)

    def set_last_monthly(self, value):
        self.user["last_monthly"] = value
        DATABASE["eco"].write(self.data)

    def set_last_yearly(self, value):
        self.user["last_yearly"] = value
        DATABASE["eco"].write(self.data)

    def add_balance(self, value):
        self.user["balance"] += value
        DATABASE["eco"].write(self.data)

    def add_bank(self, value):
        self.user["bank"] += value
        DATABASE["eco"].write(self.data)

class Marriage:
    def __init__(self, user_id):
        self.user_id = user_id
        self.data = DATABASE["marriage"].read()
        self.user = self.data.get(str(self.user_id), None)
        if self.user is None:
            self.data[str(self.user_id)] = {
                "married": False,
                "partner": None,
                "married_since": None,
                "marriage_id": None,
            }
            DATABASE["marriage"].write(self.data)
            self.user = self.data.get(str(self.user_id), None)

    def get_married(self):
        return self.user["married"]

    def get_partner(self):
        return self.user["partner"]

    def get_married_since(self):
        return self.user["married_since"]

    def get_marriage_id(self):
        return self.user["marriage_id"]

    def set_married(self, value):
        self.user["married"] = value
        DATABASE["marriage"].write(self.data)

    def set_partner(self, value):
        self.user["partner"] = value
        DATABASE["marriage"].write(self.data)

    def set_married_since(self, value):
        self.user["married_since"] = value
        DATABASE["marriage"].write(self.data)

    def set_marriage_id(self, value):
        self.user["marriage_id"] = value
        DATABASE["marriage"].write(self.data)

    def add_marriage_id(self, value):
        self.user["marriage_id"] = value
        DATABASE["marriage"].write(self.data)