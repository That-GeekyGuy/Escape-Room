import time

class player:
    lives = 3
    flag = 0

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.current_room = 0
        self.time_start = None
        self.time_elapsed = 0

    def start_timer(self):
        self.time_start = time.time()

    def stop_timer(self):
        self.time_elapsed = time.time() - self.time_start

    def add_score(self):
        self.score += 10

    def reset_score(self, deducted_points):
        self.score -= deducted_points

    def hint_ded(self):
        self.score -= 5

    def leaderboard_add(self):
        with open("leaderboard.txt", "a") as f:
            f.write(f"{self.name} {self.score} {self.time_elapsed:.2f}\n")

    def death(self):
        self.lives -= 1

        if self.lives == 0:
            self.stop_timer()
            self.leaderboard_add()
            print("Game over")
            print(f"Your score: {self.score}, Time: {self.time_elapsed:.2f} seconds.")
            exit()
        else:
            print(f"You have {self.lives} lives remaining. Try again!")

class Room:
    def __init__(self, name, puzzles, hints):
        self.name = name
        self.puzzles = puzzles
        self.hints = hints
        self.is_door_unlocked = False

    def attempt_puzzle(self, player):
        i = 0
        total_score_deducted = 0
        while i < len(self.puzzles):
            print(f"Puzzle {i + 1}: {self.puzzles[i]['question']}")
            answer = input("Your answer: ")

            if answer.lower() == self.puzzles[i]['answer'].lower():
                print("Correct!")
                player.add_score()
                i += 1
            else:
                print("Incorrect.")
                player.death()

                use_hint = input("Do you want a hint? (yes/no): ").lower()

                if use_hint == "yes":
                    self.get_hint(i)
                    player.hint_ded()
                else:
                    print("Restarting room from the first question...")
                    player.reset_score(total_score_deducted)
                    total_score_deducted = 0
                    i = 0

            total_score_deducted += 10  # Deduct 10 points for every correct answer that must be reset

        self.is_door_unlocked = True
        print("The door is now unlocked.")

    def get_hint(self, puzzle_index):
        if self.hints[puzzle_index]:
            print(f"Hint: {self.hints[puzzle_index]}")
        else:
            print("No hints available for this puzzle.")

class Hint:
    def __init__(self, hints):
        self.hints = hints

    def add_hint(self, hint):
        self.hints.append(hint)

# Game Code
def main():
    print("Welcome to the Puzzle Solver Game!")
    player_name = input("Enter your name: ")
    current_player = player(player_name)

    # Create rooms with themes
    room1 = Room(
        "Math Room",
        [
            {"question": "1 RABBIT SAW 9 ELEPHANTS WHILE GOING TO THE RIVER. EVERY ELEPHANT SAW 3 MONKEYS GOING TO THE RIVER. EACH MONKEY HAD 1 TORTOISE IN EACH HAND. HOW MANY ANIMALS WERE GOING TO THE RIVER?", "answer": "10"},
            {"question": "A clock shows the time as 3:15. What is the angle between the hour and minute hands?(in degrees)", "answer": "7.5"},
            {"question": "There are men and horses in a stable. In total there are 22 heads and 72 feet. How many men and horses are there?", "answer": "8 men and 14 horses"},
            {"question": "What is the next number in the sequence: 2, 10, 30, 68, 130?", "answer": "222"}
        ],
        [
            "Focus on who is actually moving to the river.",
            "Visualize the clock to estimate the angle.",
            "Set up a system of equations for heads and feet.",
            "Analyze the differences between consecutive numbers in the sequence."
        ]
    )

    room2 = Room(
        "Science Room",
        [
            {"question": "When I'm in the swimming pool I will give the positive state of the universe's old guy.... Mostly the definition of 'strong' acts in reverse manner with me.... Every living being needs me and my opposite equally otherwise they don't exist... Now tell me who I am", "answer": "Acid"},
            {"question": "My atomic number is twice as much as the element's number between Indium and Antimony. What am I?", "answer": "Fermium"},
            {"question": "You cannot find us on the IUPAC periodic table of elements. Which letters are we?", "answer": "J and Q"},
            {"question": "I am a gas and line-up with neon. I am also the home of a superhero. What am I?", "answer": "Krypton"}
        ],
        [
            "Think about acids and their role in chemistry.",
            "Find the atomic numbers of Indium and Antimony.",
            "Focus on letters not included in the periodic table.",
            "This gas is part of the noble gases and has a superhero connection."
        ]
    )

    room3 = Room(
        "Riddle Room",
        [
            {"question": "What do you call a fish with no eyes?", "answer": "Fsh"},
            {"question": "If two’s company and three’s a crowd, what are four and five?", "answer": "Nine"},
            {"question": "I have cities, but no houses. I have forests, but no trees. I have rivers, but no water. What am I(one word)?", "answer": "map"},
            {"question": "Before Mt. Everest was discovered, what was the highest mountain in the world?", "answer": "Mt. Everest"},
            {"question": " I am an odd number. Take away a letter and I become even. What number am I?", "answer": "seven"},
            {"question": "What starts with P and ends with E and has thousands of letters?", "answer": "post office"}
        ],
        [
            "Remove the letter 'i' from 'fish'.",
            "Add the numbers four and five.",
            "Think of something that represents geography but isn't physical.",
            "The answer hasn't changed, even if it was undiscovered.",
            "I am associated to CR7",
            "It's a place that handles mail."
        ]
    )

    rooms = [room1, room2, room3]

    current_player.start_timer()

    for room in rooms:
        print(f"You are now in {room.name}.")
        room.attempt_puzzle(current_player)

    current_player.stop_timer()
    current_player.leaderboard_add()
    print(f"Congratulations {current_player.name}! You completed the game with a score of {current_player.score} in {current_player.time_elapsed:.2f} seconds.")

if __name__ == "__main__":
    main()
