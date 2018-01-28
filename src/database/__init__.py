from src.database.clubDb import clubDb
from src.database.playerDb import playerDb
def initDB():
    clubDb.createTeamTable()
    playerDb.createPlayersTable()
