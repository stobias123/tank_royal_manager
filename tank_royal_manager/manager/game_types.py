from tank_royal_manager.robocode_event_models import game_setup

STANDARD = game_setup.GameSetup(
    arenaHeight=600,
    arenaWidth=800,
    defaultTurnsPerSecond=30,
    gameType="classic",
    gunCoolingRate=0.1,
    isArenaHeightLocked=True,
    isArenaWidthLocked=True,
    isGunCoolingRateLocked=True,
    isMaxInactivityTurnsLocked=True,
    isMaxNumberOfParticipantsLocked=True,
    isMinNumberOfParticipantsLocked=True,
    isNumberOfRoundsLocked=True,
    isReadyTimeoutLocked=False,
    isTurnTimeoutLocked=False,
    maxInactivityTurns=450,
    maxNumberOfParticipants=20,
    minNumberOfParticipants=2,
    numberOfRounds=1,
    readyTimeout=1000000,
    turnTimeout=30000
)