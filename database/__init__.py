from database.clubDb import clubDb
from database.playerDb import playerDb
def initDB():
    clubDb.createTeamTable()
    playerDb.createPlayersTable()