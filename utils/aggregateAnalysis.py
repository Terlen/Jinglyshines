from collections import Counter, namedtuple
from statistics import mean, median, multimode

stats = namedtuple('rollStats', ['mean', 'median', 'mode'])

def getMemberList(encounters: list) -> list:
    members = []
    for encounter in encounters:
        for member in encounter.members:
            members.append(member)
    return members


def getMemberNames(memberList: list) -> set:
    members = []
    for member in memberList:
        members.append(member.name)
    return set(members)

def getRolledItemNames(encounters: list) -> list:
    loot = []
    for encounter in encounters:
        for item in encounter.items:
            loot.append(item.name)
    return loot

def getRolledValues(encounters: list) -> list:
    rolls = []
    for encounter in encounters:
        for roll in encounter.rolls:
            rolls.append(int(roll.value))
    return rolls

def getRolls(encounters: list,type: str) -> list:
    rolls = []
    for encounter in encounters:
        for roll in encounter.rolls:
            if roll.type == type:
               rolls.append(roll)
    return rolls

def getDroppedLoot(members: list, logger: str) -> tuple:
    # Show loot that wasn't rolled for
    eventLoot = []
    privateLoot = []
    for member in members:
        if member.name != logger:
            eventLoot += member.loot
        else:
            # The log file will contain the logger's private loot (gil, tomestones) that each player receives individually.
            # This loot needs to be separated from the randomly dropped eventLoot
            for item in member.loot:
                if 'gil' not in item.name and 'tomestone' not in item.name:
                    eventLoot.append(item)
                else:
                    privateLoot.append(item)
    return (eventLoot, privateLoot)

def countList(list: list) -> Counter:
    return Counter(list)

def getCounterMaxCount(counter: Counter) -> int:
    return counter.most_common()[0][1] if counter else 0

def getCounterKeysWithValue(counter: Counter, count: int) -> list:
    return [key for key,value in counter.items() if value == count]

def rollStatistics(rolledNumbers: list) -> stats:
    rollCount = Counter(rolledNumbers)
    maxRollCount = getCounterMaxCount(rollCount)
    meanRolls = mean(rolledNumbers)
    medianRolls = median(rolledNumbers)
    rollMode = multimode(rolledNumbers)
    return stats(meanRolls,medianRolls,(rollMode, maxRollCount))


def winRatios(members, rolls):
    memberWinRatios = {}
    for member in members:
        attempts = [roll for roll in rolls if roll.member.name == member]
        wins = [roll for roll in attempts if roll.win]
        try:
            winRatio = len(wins) / len(attempts)
            memberWinRatios[member] = (len(wins),len(attempts),winRatio)
        except ZeroDivisionError:
            continue
    return memberWinRatios

def percentWins(members, rolls):
    winPercentages = {}
    totalWins = [roll for roll in rolls if roll.win]
    for member in members:
        memberWins = len([roll for roll in totalWins if roll.member.name == member])
        try:
            winPercent = memberWins / len(totalWins)
            winPercentages[member] = (memberWins, len(totalWins), winPercent)
        except ZeroDivisionError:
            continue
    return winPercentages

def getMembersBestRatio(ratios):
    items = ratios.items()
    stats = ratios.values()
    ratioValues = [item[2] for item in ratios.values()]
    try:
        maxRatio = max(ratioValues)
        best = [(key,value[0],value[1],value[2]) for key, value in items if value[2] == maxRatio]
        return best
    except ValueError:
        return None

def getMembersWorstRatio(ratios):
    items = ratios.items()
    stats = ratios.values()
    ratioValues = [item[2] for item in ratios.values()]
    try:
        minRatio = min(ratioValues)
        worst = [(key,value[0],value[1],value[2]) for key, value in items if value[2] == minRatio]
        return worst
    except ValueError:
        return None
