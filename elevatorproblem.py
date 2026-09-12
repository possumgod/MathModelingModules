# MODULE 1 ELEVATOR PROBLEM CODE
# Author: Devlin Gallagher
# Description: provides a model for calculating the optimal elevator assignment to reduce employees late for work. See MyCourses & Execuative Summary for more info.

# overall constants
FLOORTRAVELTIME = 4
STOPTIME = 10
GROUNDFLOORTIME = 15
REOPENTIME = 5
CAPACITY = 10
INITLATEEMPLOYEES = 70


# floor employee numbers
FLOOREMPLOYEECOUNT = {
    "GF": 0,
    "FIRSTF": 80,
    "SECONDF": 80,
    "THIRDF": 40,
    "FOURTHF": 80,
    "FIFTHF": 20,
    "SIXTHF": 20
}


# elevator will be a set of floors assigned
elevators = {
    "A": set(),
    "B": set(),
    "C": set()
}

# get elevators that go to a specific floor
def elevatorFloorAssign(elevators, floor):
    return [e for e in elevators if floor in elevators[e]]


# find prob of an employee going to a specific floor
def floorProbability(assignedF):
    prob = {}
    total = sum(FLOOREMPLOYEECOUNT[f] for f in assignedF)

    if total == 0: return prob

    for floor in assignedF:
        prob[floor] = (FLOOREMPLOYEECOUNT[floor] / total)

    return prob


# get highest floor visited from an specific elevator
def highestFVisited(elevators, elevator):
    if not elevators[elevator]:
        return 0

    floors = list(FLOOREMPLOYEECOUNT.keys())

    return max(floors.index(floor) for floor in elevators[elevator])


# return expected num of employees going in each elevator
# if multiple floors then assume equal prob of either elevator
def expectedEmployeeCnts(elevators):
    counts = {
        elevator: 0
        for elevator in elevators
    }

    for floor in FLOOREMPLOYEECOUNT:
        numEmployees = FLOOREMPLOYEECOUNT[floor]
        available = elevatorFloorAssign(elevators, floor)

        if numEmployees > 0 and not available: return None
        if not available: continue

        prob = 1 / len(available)

        for elevator in available:
            counts[elevator] += numEmployees * prob

    return counts


# calculated probability distribution (based on class notes)
# this sucks and this lowkey might be wrong
def elevatorFloorProb(elevators, elevator):
    weighted = {}

    for floor in elevators[elevator]:
        available = elevatorFloorAssign(elevators, floor)

        if not available: continue

        weighted[floor] = (FLOOREMPLOYEECOUNT[floor] / len(available))

    total = sum(weighted.values())
    if total == 0:
        return {}

    return {
        floor: weighted[floor] / total
        for floor in weighted
    }


# prob of random person going to a specific floor
def probOfStop(probability, passengers):
    return 1 - (1 - probability) ** passengers


# prob number of stops per trip
def expectedStops(elevators, elevator, passengers):
    probs = elevatorFloorProb(elevators, elevator)
    numStops = 0

    for probability in probs.values():
        numStops += probOfStop(probability, passengers)

    return numStops


# calculated time for one trip
def tripTime(elevators, elevator, passengers):
    if passengers <= 0: return 0

    numStops = expectedStops(elevators, elevator, passengers)
    highestF = highestFVisited(elevators, elevator)

    return GROUNDFLOORTIME + (STOPTIME * numStops) + (2 * FLOORTRAVELTIME * highestF)


# total time for one elevator trip from GF to maxF and back
def elevatorTime(elevators, elevator):
    employeeCnts = expectedEmployeeCnts(elevators)

    if employeeCnts is None:
        return float("inf")

    numEmployees = employeeCnts[elevator]

    if numEmployees == 0:
        return 0

    fullTrips = int(numEmployees // CAPACITY)

    remainder = numEmployees % CAPACITY

    # full if false, partial if true
    # obligated ternary operator has to be somewhere :3
    return (tripTime(elevators, elevator, remainder) + (fullTrips * tripTime(elevators, elevator, CAPACITY))) if (remainder > 0) else (fullTrips * tripTime(elevators, elevator, CAPACITY))


# total time for all the trips
def totalTime(elevators):
    return max(elevatorTime(elevators, elevator) for elevator in elevators)


# find optimal assignment
# the findAssignments function was modified using ChatGPT, as my own recursive method caused a
# bug in the calculation of how elevators were assigned (duplicates somehow??) so lines 188 to 
# 217 are partinfluenced by the feedback it gave me (basically I wasn't updating the index lol)
minTotalTime = float("inf")
bestElevators = None
floors = list(FLOOREMPLOYEECOUNT.keys())[1:]
elevatorOptions = [
    {"A"},
    {"B"},
    {"C"},
    {"A", "B"},
    {"A", "C"},
    {"B", "C"},
    {"A", "B", "C"}
]


def findAssignments(floors, index, currentElevators):
    global minTotalTime
    global bestElevators

    if index == len(floors):
        for e in currentElevators:
            if not currentElevators[e]: return

        currentTime = totalTime(currentElevators)

        if currentTime < minTotalTime:
            minTotalTime = currentTime
            bestElevators = {}
            for e in currentElevators:
                bestElevators[e] = set(currentElevators[e])

        return

    floor = floors[index]
    for assignedElevators in elevatorOptions:
        for e in assignedElevators:
            currentElevators[e].add(floor)

        findAssignments(floors, index + 1, currentElevators)

        for elevator in assignedElevators:
            currentElevators[elevator].remove(floor)



def main():
    currentElevators = {}
    for e in elevators:
        currentElevators[e] = set()

    findAssignments(floors, 0, currentElevators)
    employeeCnts = expectedEmployeeCnts(bestElevators)

    print("Best elevator assignment: ")

    for elevator in bestElevators:
        print("{} assigned to floor(s) {} - {} employees, {} seconds"
              .format(elevator, ', '.join(bestElevators[elevator]), round(employeeCnts[elevator], 1), round(elevatorTime(bestElevators, elevator), 2)))

    print()
    print(f"Minimum expected total time: {round(minTotalTime, 2)} seconds ({round(minTotalTime / 60, 2)} minutes).")



main()