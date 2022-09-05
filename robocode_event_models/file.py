# generated by datamodel-codegen:
#   filename:  file.json
#   timestamp: 2022-09-04T05:04:28+00:00

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, confloat, conint, constr

from . import (
    bot_address,
    bot_info,
    bot_results_for_bot,
    bot_state,
    bot_state_with_id,
    bullet_state,
    color,
    event,
    game_setup,
    initial_position,
    participant,
)


class Type(Enum):
    BotHandshake = 'BotHandshake'
    ControllerHandshake = 'ControllerHandshake'
    ObserverHandshake = 'ObserverHandshake'
    ServerHandshake = 'ServerHandshake'
    BotReady = 'BotReady'
    BotIntent = 'BotIntent'
    BotInfo = 'BotInfo'
    BotListUpdate = 'BotListUpdate'
    GameStartedEventForBot = 'GameStartedEventForBot'
    GameStartedEventForObserver = 'GameStartedEventForObserver'
    GameEndedEventForBot = 'GameEndedEventForBot'
    GameEndedEventForObserver = 'GameEndedEventForObserver'
    GameAbortedEvent = 'GameAbortedEvent'
    GamePausedEventForObserver = 'GamePausedEventForObserver'
    GameResumedEventForObserver = 'GameResumedEventForObserver'
    RoundStartedEvent = 'RoundStartedEvent'
    RoundEndedEvent = 'RoundEndedEvent'
    ChangeTps = 'ChangeTps'
    TpsChangedEvent = 'TpsChangedEvent'
    BotDeathEvent = 'BotDeathEvent'
    BotHitBotEvent = 'BotHitBotEvent'
    BotHitWallEvent = 'BotHitWallEvent'
    BulletFiredEvent = 'BulletFiredEvent'
    BulletHitBotEvent = 'BulletHitBotEvent'
    BulletHitBulletEvent = 'BulletHitBulletEvent'
    BulletHitWallEvent = 'BulletHitWallEvent'
    HitByBulletEvent = 'HitByBulletEvent'
    ScannedBotEvent = 'ScannedBotEvent'
    SkippedTurnEvent = 'SkippedTurnEvent'
    TickEventForBot = 'TickEventForBot'
    TickEventForObserver = 'TickEventForObserver'
    WonRoundEvent = 'WonRoundEvent'
    StartGame = 'StartGame'
    StopGame = 'StopGame'
    PauseGame = 'PauseGame'
    ResumeGame = 'ResumeGame'
    NextTurn = 'NextTurn'


class Fire(BaseModel):
    host: Optional[str] = Field(None, description='Host name or IP address')
    port: Optional[int] = Field(None, description='Port number')
    victimId: Optional[int] = Field(None, description='ID of the bot that got hit')
    name: Optional[str] = Field(
        None, description="Name of server, e.g. John Doe's RoboRumble Server"
    )
    version: Optional[str] = Field(
        None,
        description="Game version, e.g. '1.0.0' using Semantic Versioning (https://semver.org/)",
    )
    authors: Optional[List[str]] = Field(
        None, description='Name of authors, e.g. John Doe (john_doe@somewhere.net)'
    )
    description: Optional[str] = Field(
        None, description='Short description of the bot, preferable a one-liner'
    )
    homepage: Optional[str] = Field(None, description='URL to a home page for the bot')
    countryCodes: Optional[List[constr(regex=r'/^[a-z]{2}$/ig')]] = Field(
        None, description='2-letter country code(s) defined by ISO 3166-1, e.g. "UK"'
    )
    gameTypes: Optional[List[str]] = Field(
        None,
        description='Game types running at this server, e.g. "melee" and "1v1"',
        min_items=1,
        unique_items=True,
    )
    platform: Optional[str] = Field(
        None, description='Platform used for running the bot, e.g. JVM 17 or .NET 5'
    )
    programmingLang: Optional[str] = Field(
        None, description='Language used for programming the bot, e.g. Java 17 or C# 10'
    )
    initialPosition: Optional[initial_position.InitialPosition] = Field(
        None, description='Initial start position of the bot used for debugging.'
    )
    secret: Optional[str] = Field(
        None, description='Secret used for access control with the server'
    )
    botId: Optional[int] = Field(None, description='ID of the bot that hit another bot')
    energy: Optional[float] = Field(None, description='Energy level of the scanned bot')
    x: Optional[float] = Field(None, description='X coordinate of the scanned bot')
    y: Optional[float] = Field(None, description='Y coordinate of the scanned bot')
    rammed: Optional[bool] = Field(
        None, description='Flag specifying, if the victim bot got rammed'
    )
    turnRate: Optional[float] = Field(
        None,
        description='Turn rate of the body in degrees per turn (can be positive and negative)',
    )
    gunTurnRate: Optional[float] = Field(
        None,
        description='Turn rate of the gun in degrees per turn (can be positive and negative)',
    )
    radarTurnRate: Optional[float] = Field(
        None,
        description='Turn rate of the radar in degrees per turn (can be positive and negative)',
    )
    targetSpeed: Optional[float] = Field(
        None,
        description='New target speed in units per turn (can be positive and negative)',
    )
    firepower: Optional[confloat(le=3.0, gt=0.0)] = Field(
        None, description='Attempt to fire gun with the specified firepower'
    )
    adjustGunForBodyTurn: Optional[bool] = Field(
        None,
        description='Flag indicating if the gun must be adjusted to compensate for the body turn. Default is false.',
    )
    adjustRadarForBodyTurn: Optional[bool] = Field(
        None,
        description='Flag indicating if the radar must be adjusted to compensate for the body turn. Default is false.',
    )
    adjustRadarForGunTurn: Optional[bool] = Field(
        None,
        description='Flag indicating if the radar must be adjusted to compensate for the gun turn. Default is false.',
    )
    rescan: Optional[bool] = Field(
        None,
        description='Flag indicating if the bot should rescan with previous radar direction and scan sweep angle.',
    )
    bodyColor: Optional[color.Color] = Field(
        None, description='Current RGB color of the body'
    )
    turretColor: Optional[color.Color] = Field(
        None, description='New color of the gun turret'
    )
    radarColor: Optional[color.Color] = Field(
        None, description='New color of the radar'
    )
    bulletColor: Optional[color.Color] = Field(
        None,
        description='New color of the bullet. Note. This will be the color of a bullet when it is fired',
    )
    scanColor: Optional[color.Color] = Field(
        None, description='New color of the scan arc'
    )
    tracksColor: Optional[color.Color] = Field(
        None, description='New color of the tracks'
    )
    gunColor: Optional[color.Color] = Field(None, description='New color of gun')
    bots: Optional[List[bot_info.BotInfo]] = Field(None, description='List of bots')
    rank: Optional[conint(ge=1)] = Field(
        None,
        description='Rank/placement of the bot, where 1 is 1st place, 4 is 4th place etc.',
    )
    survival: Optional[int] = Field(
        None, description='Survival score gained whenever another bot is defeated'
    )
    lastSurvivorBonus: Optional[int] = Field(
        None, description='Last survivor score as last survivor in a round'
    )
    bulletDamage: Optional[int] = Field(None, description='Bullet damage given')
    bulletKillBonus: Optional[int] = Field(None, description='Bullet kill bonus')
    ramDamage: Optional[int] = Field(None, description='Ram damage given')
    ramKillBonus: Optional[int] = Field(None, description='Ram kill bonus')
    totalScore: Optional[int] = Field(None, description='Total score')
    firstPlaces: Optional[int] = Field(None, description='Number of 1st places')
    secondPlaces: Optional[int] = Field(None, description='Number of 2nd places')
    thirdPlaces: Optional[int] = Field(None, description='Number of 3rd places')
    id: Optional[int] = Field(
        None, description='Identifier for the participant in a battle'
    )
    direction: Optional[float] = Field(
        None, description='Direction in degrees of the scanned bot'
    )
    gunDirection: Optional[float] = Field(None, description='Gun direction in degrees')
    radarDirection: Optional[float] = Field(
        None, description='Radar direction in degrees'
    )
    radarSweep: Optional[float] = Field(
        None,
        description='Radar sweep angle in degrees, i.e. angle between previous and current radar direction',
    )
    speed: Optional[float] = Field(
        None, description='Speed measured in units per turn of the scanned bot'
    )
    gunHeat: Optional[float] = Field(None, description='Gun heat')
    bullet: Optional[bullet_state.BulletState] = Field(
        None, description='Bullet that has hit the bot'
    )
    damage: Optional[float] = Field(None, description='Damage inflicted by the bullet')
    hitBullet: Optional[bullet_state.BulletState] = Field(
        None, description='The other bullet that was hit by the bullet'
    )
    bulletId: Optional[int] = Field(None, description='ID of the bullet')
    ownerId: Optional[int] = Field(
        None, description='ID of the bot that fired the bullet'
    )
    power: Optional[float] = Field(
        None, description='Bullet firepower (between 0.1 and 3.0)'
    )
    color: Optional[color.Color] = Field(None, description='Color of the bullet')
    tps: Optional[int] = Field(
        None,
        description='Turns per second (TPS). Typically a value from 0 to 999. -1 means maximum possible TPS speed.',
    )
    author: Optional[str] = Field(
        None, description='Author name, e.g. John Doe (john_doe@somewhere.net)'
    )
    turnNumber: Optional[int] = Field(
        None, description='The current turn number in the round when event occurred'
    )
    numberOfRounds: Optional[int] = Field(
        None, description='Number of rounds in battle'
    )
    results: Optional[bot_results_for_bot.BotResultsForBot] = Field(
        None, description='Results of the battle'
    )
    gameType: Optional[str] = Field(None, description='Type of game')
    arenaWidth: Optional[int] = Field(
        None, description='Width of arena measured in units'
    )
    isArenaWidthLocked: Optional[bool] = Field(
        None,
        description='Flag specifying if the width of arena is fixed for this game type',
    )
    arenaHeight: Optional[int] = Field(
        None, description='Height of arena measured in units'
    )
    isArenaHeightLocked: Optional[bool] = Field(
        None,
        description='Flag specifying if the height of arena is fixed for this game type',
    )
    minNumberOfParticipants: Optional[int] = Field(
        None, description='Minimum number of bots participating in battle'
    )
    isMinNumberOfParticipantsLocked: Optional[bool] = Field(
        None,
        description='Flag specifying if the minimum number of bots participating in battle is fixed for this game type',
    )
    maxNumberOfParticipants: Optional[int] = Field(
        None, description='Maximum number of bots participating in battle'
    )
    isMaxNumberOfParticipantsLocked: Optional[bool] = Field(
        None,
        description='Flag specifying if the maximum number of bots participating in battle is fixed for this game type',
    )
    isNumberOfRoundsLocked: Optional[bool] = Field(
        None,
        description='Flag specifying if the number-of-rounds is fixed for this game type',
    )
    gunCoolingRate: Optional[float] = Field(
        None,
        description='Gun cooling rate. The gun needs to cool down to a gun heat of zero before the gun is able to fire',
    )
    isGunCoolingRateLocked: Optional[bool] = Field(
        None,
        description='Flag specifying if the gun cooling rate is fixed for this game type',
    )
    maxInactivityTurns: Optional[int] = Field(
        None,
        description='Maximum number of inactive turns allowed, where a bot does not take any action before it is zapped by the game',
    )
    isMaxInactivityTurnsLocked: Optional[bool] = Field(
        None,
        description='Flag specifying if the inactive turns is fixed for this game type',
    )
    turnTimeout: Optional[int] = Field(
        None,
        description="Turn timeout in microseconds (1 / 1,000,000 second) for sending intent after having received 'tick' message",
    )
    isTurnTimeoutLocked: Optional[bool] = Field(
        None,
        description='Flag specifying if the turn timeout is fixed for this game type',
    )
    readyTimeout: Optional[int] = Field(
        None,
        description="Time limit in microseconds (1 / 1,000,000 second) for sending ready message after having received 'game started' message",
    )
    isReadyTimeoutLocked: Optional[bool] = Field(
        None,
        description='Flag specifying if the ready timeout is fixed for this game type',
    )
    defaultTurnsPerSecond: Optional[int] = Field(
        None,
        description='Default number of turns to show per second for an observer/UI',
    )
    myId: Optional[int] = Field(
        None, description='My ID is an unique identifier for this bot'
    )
    gameSetup: Optional[game_setup.GameSetup] = Field(None, description='Game setup')
    participants: Optional[List[participant.Participant]] = Field(
        None, description='List of bots participating in this battle'
    )
    angle: Optional[float] = Field(
        None, description='The angle. When it is not set, a random value will be used.'
    )
    type: Optional[Type] = None
    roundNumber: int = Field(
        ..., description='The current round number in the battle when event occurred'
    )
    scannedByBotId: Optional[int] = Field(
        None, description='ID of the bot did the scanning'
    )
    scannedBotId: Optional[int] = Field(
        None, description='ID of the bot that was scanned'
    )
    variant: Optional[str] = Field(
        None, description="Game variant, e.g. 'Tank Royale' for Robocode Tank Royale"
    )
    botAddresses: Optional[List[bot_address.BotAddress]] = Field(
        None, description='List of bot addresses'
    )
    enemyCount: Optional[int] = Field(
        None, description='Number of enemies left in the current round'
    )
    botState: Optional[bot_state.BotState] = Field(
        None, description='Current state of this bot'
    )
    bulletStates: List[bullet_state.BulletState] = Field(
        ..., description='Current state of all bullets'
    )
    events: List[event.Event] = Field(
        ..., description='All events occurring at this tick'
    )
    botStates: List[bot_state_with_id.BotStateWithID] = Field(
        ..., description='Current state of all bots'
    )