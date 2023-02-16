import datetime
import aiosqlite

async def get_marriage(self, user):
    """Returns the marriage balance of a user."""
    async with self.marriage_db.cursor() as cursor:
        await cursor.execute("SELECT married FROM marriage WHERE user1 = ?", (user.id,))
        result = await cursor.fetchone()
        if result is None:
            return False
        married = result[0]
        return married

async def marry(self, user1, user2):
    async with self.marriage_db.cursor() as cursor:
        await cursor.execute("SELECT * FROM marriage WHERE user1 = ? AND user2 = ?", (user1.id, user2.id))
        result = await cursor.fetchone()
        if result is None:
            await cursor.execute("INSERT INTO marriage (user1, user2, married, married_since) VALUES (?, ?, ?, ?)", (user1.id, user2.id, True, datetime.datetime.now().strftime("%m/%d/%Y %H:%M")))
            await cursor.execute("INSERT INTO marriage (user1, user2, married, married_since) VALUES (?, ?, ?, ?)", (user2.id, user1.id, True, datetime.datetime.now().strftime("%m/%d/%Y %H:%M")))
            await self.marriage_db.commit()
            return True
        else:
            return False
            
async def divorce(self, user1, user2):
    async with self.marriage_db.cursor() as cursor:
        await cursor.execute("SELECT * FROM marriage WHERE user1 = ? AND user2 = ?", (user1.id, user2.id))
        result = await cursor.fetchone()
        if result is None:
            return False
        else:
            await cursor.execute("DELETE FROM marriage WHERE user1 = ? AND user2 = ?", (user1.id, user2.id))
            await cursor.execute("DELETE FROM marriage WHERE user1 = ? AND user2 = ?", (user2.id, user1.id))
            await self.marriage_db.commit()
            return True

async def get_marriage_since(self, user):
    async with self.marriage_db.cursor() as cursor:
        await cursor.execute("SELECT married_since FROM marriage WHERE user1 = ?", (user.id,))
        result = await cursor.fetchone()
        if result is None:
            return False
        married_since = result[0]
        return married_since

async def get_marriage_partner(self, user):
    async with self.marriage_db.cursor() as cursor:
        await cursor.execute("SELECT user2 FROM marriage WHERE user1 = ?", (user.id,))
        result = await cursor.fetchone()
        if result is None:
            return False
        user2 = result[0]
        return user2

