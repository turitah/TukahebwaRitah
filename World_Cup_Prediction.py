 #simple country that will win world cup 2026
#pre_tournament preparation( training, friendlines, recovery)
#Group stage matches(3 matches)
#knockout stages(Round of 16 , Quarter- final , semi- final, final)
#using loop control statements.
#loop exists when tournament is won or lost(break)
#certain conditions skipto the next iteration(continue)
#placeholders exist for future features(pass)

#FIFA WORLD CUP 2026 PREDICTION

morale = 60
strength = 75
injuries = 0
points = 0

print("=" * 40)
print("FRANCE WORLD CUP 2026 MANAGER")
print("=" * 40)

# Pre tournament preparation
for day in range(1, 4):

    print(f"\nPreparation Day {day}")

    print("1. Intensive training")
    print("2. Friendly matches")
    print("3. Recovery sessions")
    print("4. Hire Sports psychologist (Coming soon)")

    choice = int(input("Choose an activity (1-4): "))

    if choice == 1:
        morale += 10
        strength += 15
        injuries += 2
        print("Intensive training completed. Morale and strength increased and some injuries sustained.")

    elif choice == 2:
        morale += 5
        strength += 10
        injuries += 1
        print("Friendly matches completed. Morale and strength increased including some few injuries.")

    elif choice == 3:
        injuries = max(0, injuries - 1)
        morale += 5
        print("Recovery sessions completed. Injuries reduced.")

    elif choice == 4:
        pass

    # continue
    if injuries > 6:
        print("Too many injuries! Skipping to the next day for recovery.")
        continue

    print("\nPreparation completed")
    print(f"Morale: {morale}")
    print(f"Strength: {strength}")
    print(f"Injuries: {injuries}")

# Group stage matches

group_matches = [
    ("Senegal", "draw", 1, 1),
    ("Iran", "win", 3, 1),
    ("Norway", "win", 2, 0)
]

print("\nGROUP STAGE MATCHES")

for opponent, result, france_goals, opp_goals in group_matches:

    print(f"\nFrance vs {opponent}")

    if result == "win":
        print(f"France {france_goals} - {opp_goals} {opponent}")
        points += 3
        morale += 6

    elif result == "draw":
        print(f"France {france_goals} - {opp_goals} {opponent}")
        points += 1
        morale += 3

print("\nGroup stages finished")
print(f"Points: {points}")

if points < 4:
    print("France eliminated in group stages.")
    exit()

print("France qualify for knockout stages!")

# Knockout stages

knockout_rounds = [
    ("Round of 16", "USA", "win"),
    ("Quarter-final", "Portugal", "win"),
    ("Semi-final", "Argentina", "win"),
    ("Final", "Spain", "win")
]

for round_name, opponent, result in knockout_rounds:

    print(f"\n{round_name}")
    print(f"France vs {opponent}")

    if result == "lose":
        print("France eliminated!")
        break

    print(f"France defeated {opponent}")
    morale += 10

    if round_name == "Final":
        print("\n🏆🏆🏆 FRANCE ARE WORLD CUP CHAMPIONS! 🏆🏆🏆")
        print("Tournament won!")
        break

print("\nFINAL TEAM STATS")
print(f"Morale: {morale}")
print(f"Strength: {strength}")
print(f"Injuries: {injuries}")
print("End of simulation")