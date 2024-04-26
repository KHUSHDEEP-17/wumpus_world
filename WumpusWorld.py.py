import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import random

class WumpusGame:
    def __init__(self, size=5):
        self.size = size
        self.player_location = (0, 0)
        self.Wumpus_location = self.generate_random_location(exclude=[self.player_location, (0, 1), (1, 0)])
        self.gold_location = self.generate_random_location(exclude=[self.player_location, (0, 1), (1, 0)])
        self.pit_locations = [self.generate_random_location(exclude=[self.player_location, (0, 1), (1, 0)]) for _ in range(3)]
        self.arrows = 3  # Initial number of arrows
        self.game_over = False

        # Components in the cave
        self.stench_locations = self.calculate_stench_locations()
        self.breeze_locations = self.calculate_breeze_locations()
        self.glitter_location = self.gold_location
        self.scream_heard = False
        self.bump = False

        # Explored rooms
        self.explored_rooms = set()

        
    def generate_random_location(self, exclude=[]):
        while True:
            location = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if location not in exclude and all(not self.check_adjacent(location, ex_loc) for ex_loc in exclude):
                return location


    def calculate_stench_locations(self):
        x, y = self.Wumpus_location
        stench_locations = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        stench_locations = [(x, y) for x, y in stench_locations if 0 <= x < self.size and 0 <= y < self.size]
        return stench_locations

    def calculate_breeze_locations(self):
        breeze_locations = []
        for pit_location in self.pit_locations:
            x, y = pit_location
            breeze_locations.append((x - 1, y))
            breeze_locations.append((x + 1, y))
            breeze_locations.append((x, y - 1))
            breeze_locations.append((x, y + 1))
        breeze_locations = [(x, y) for x, y in breeze_locations if 0 <= x < self.size and 0 <= y < self.size]
        return breeze_locations

    def check_adjacent(self, location1, location2):
        x1, y1 = location1
        x2, y2 = location2
        return abs(x1 - x2) + abs(y1 - y2) == 1

    def check_game_status(self):
        if self.player_location == self.Wumpus_location:
            return "You were killed by the Wumpus! Life over."
        elif self.player_location == self.gold_location:
            return "Congratulations! You escaped from Wumpus."
        elif self.player_location in self.pit_locations:
            return "You fell into a pit! Life over."
        else:
            return None


    def shoot_arrows(self, direction):
        if not self.game_over and self.arrows > 0:
            self.arrows -= 1

        # Calculate the target location based on the shooting direction
            target_location = self.calculate_target_location(direction)

            if self.check_adjacent(self.player_location, self.Wumpus_location) and self.Wumpus_location == target_location:
            # Check if the Wumpus is adjacent to the player and the target location is the Wumpus's location
                self.Wumpus_location = self.generate_random_location(exclude=[self.player_location])
                self.scream_heard = True

                result = self.check_game_status()
                if result:
                # If the Wumpus is killed, end the game
                    self.game_over = True
                    return f"You killed the Wumpus with a arrow! You hear a horrible scream.\n{result}"
                else:
                    return "You killed the Wumpus with a arrow! You hear a horrible scream."
            else:
                return "Your arrow missed the Wumpus."

        return "You are out of arrows!"




    def calculate_target_location(self, direction):
        x, y = self.player_location

        if direction == 'up' and x > 0:
            return x , y-1
        elif direction == 'down' and x < self.size - 1:
            return x , y+1
        elif direction == 'left' and y > 0:
            return x-1, y 
        elif direction == 'right' and y < self.size - 1:
            return x+1, y

        return None


    def move_player(self, direction):
        if not self.game_over:
            x, y = self.player_location
            if direction == 'a' and x > 0:
                x -= 1
            elif direction == 'w' and y > 0:
                y -= 1
            elif direction == 'd' and x < self.size - 1:
                x += 1
            elif direction == 's' and y < self.size - 1:
                y += 1

            if (x, y) != self.player_location:
                self.explored_rooms.add(self.player_location)

            if x == self.player_location[0] and y == self.player_location[1]:
                self.bump = True
            else:
                self.bump = False

            self.player_location = (x, y)
            result = self.check_game_status()
            if result:
                self.game_over = True
                messagebox.showinfo("Life Over", result)

    def perceive_cave(self):
        perceptions = []

        if self.bump:
            perceptions.append("You feel a bump. You walked into a wall.")
        else:
            if self.player_location in self.stench_locations:
                perceptions.append("You feel fear. The Wumpus might be nearby.")
            if self.player_location in self.breeze_locations:
                perceptions.append("You feel a breeze. There might be a pit nearby.")
            if self.player_location == self.glitter_location:
                perceptions.append("You feel hope. You are saved.")
            if self.scream_heard:
                perceptions.append("You hear a horrible scream. You have killed the Wumpus.")

        return perceptions



    def restart_game(self):
        self.__init__()

class WumpusUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("THE WUMPUS WORLD")
        self.geometry("500x650")
        self.game = WumpusGame()

        self.info_label = tk.Label(self, text="Welcome to the Wumpus World!")
        self.info_label.pack()

        self.perception_label = tk.Label(self, text="")
        self.perception_label.pack()

        self.canvas = tk.Canvas(self, width=400, height=400, bg="white")
        self.canvas.pack()


     
        try:
            user_image_path = "C:/Users/hp/OneDrive/Desktop/COLLEGE/GAME THEORY/PROJECT/Player_image.jpg"
            Wumpus_image_path = "C:/Users\hp\OneDrive\Desktop\COLLEGE\GAME THEORY\PROJECT\wumpus_image.png"
            gold_image_path = "C:/Users\hp\OneDrive\Desktop\COLLEGE\GAME THEORY\PROJECT\gold_image.jpg"
            pit_image_path = "C:/Users\hp\OneDrive\Desktop\COLLEGE\GAME THEORY\PROJECT\pit_image.jpg"
            empty_explored_image_path = "C:/Users\hp\OneDrive\Desktop\COLLEGE\GAME THEORY\PROJECT\jungle.jpeg"

            
            self.user_image = ImageTk.PhotoImage(Image.open(user_image_path).resize((80, 80)))
            self.Wumpus_image = ImageTk.PhotoImage(Image.open(Wumpus_image_path).resize((80, 80)))
            self.gold_image = ImageTk.PhotoImage(Image.open(gold_image_path).resize((80, 80)))
            self.pit_image = ImageTk.PhotoImage(Image.open(pit_image_path).resize((80, 80)))
            self.empty_explored_image = ImageTk.PhotoImage(Image.open(empty_explored_image_path).resize((80, 80)))
        except Exception as e:
            print(f"Error loading images: {e}")

        self.draw_grid()
        self.draw_player()
        self.draw_Wumpus()
        self.draw_gold()
        self.draw_pits()

        self.arrows_label = tk.Label(self, text=f"arrows: {self.game.arrows}")
        self.arrows_label.pack()

        self.status_label = tk.Label(self, text="")
        self.status_label.pack()

        self.quit_button = tk.Button(self, text="Quit", command=self.quit_game)
        self.quit_button.pack()

        self.shoot_button = tk.Button(self, text="shoot arrow", command=self.shoot_arrows_prompt)
        self.shoot_button.pack()

        self.replay_button = tk.Button(self, text="Play Again", command=self.restart_game)
        self.replay_button.pack()

        self.bind("<Key>", self.key_pressed)
        self.perceive_cave()


        
    def draw_grid(self):
        cell_size = 400 // self.game.size
        for i in range(self.game.size):
            for j in range(self.game.size):
                x1, y1 = i * cell_size, j * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size

            # Check if the room is explored
                if (i, j) in self.game.explored_rooms:
                    # Check if the room contains gold, pit, or Wumpus
                    if (i, j) == self.game.gold_location:
                        image = self.gold_image
                    elif (i, j) == self.game.Wumpus_location:
                        image = self.Wumpus_image
                    elif (i, j) in self.game.pit_locations:
                        image = self.pit_image
                    else:
                        # Draw an empty explored image if the room is explored but doesn't contain gold, pit, or Wumpus
                        image = self.empty_explored_image
    
                    self.canvas.create_image((x1 + x2) // 2, (y1 + y2) // 2, image=image)
                else:
                    # Draw a black rectangle for unexplored rooms
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="black")







    def draw_player(self):
        cell_size = 400 // self.game.size
        x, y = self.game.player_location
        x1, y1 = x * cell_size, y * cell_size
        x2, y2 = x1 + cell_size, y1 + cell_size
    
        if self.game.game_over and self.game.player_location in [self.game.Wumpus_location] + self.game.pit_locations:
        # If the game is over and the player is in the room with Wumpus or pit, draw respective image
            if self.game.player_location == self.game.Wumpus_location:
                image = self.Wumpus_image
            else:
                image = self.pit_image
        elif self.game.player_location == self.game.gold_location:
            # If the player is in the room with gold, draw the gold image
            image = self.gold_image
        else:
        # Draw the user image if the game is not over, or the player is not in the room with Wumpus, pit, or gold
            image = self.user_image
    
        self.canvas.create_image((x1 + x2) // 2, (y1 + y2) // 2, image=image)

    

    def draw_Wumpus(self):
        cell_size = 400 // self.game.size
        x, y = self.game.Wumpus_location
        x1, y1 = x * cell_size, y * cell_size
        x2, y2 = x1 + cell_size, y1 + cell_size
        if (x, y) in self.game.explored_rooms:  # Only draw if explored
            self.canvas.create_image((x1 + x2) // 2, (y1 + y2) // 2, image=self.Wumpus_image)

    def draw_gold(self):
        cell_size = 400 // self.game.size
        x, y = self.game.gold_location
        x1, y1 = x * cell_size, y * cell_size
        x2, y2 = x1 + cell_size, y1 + cell_size
        if (x, y) in self.game.explored_rooms:  # Only draw if explored
            self.canvas.create_image((x1 + x2) // 2, (y1 + y2) // 2, image=self.gold_image)
    




    def draw_pits(self):
        cell_size = 400 // self.game.size
        for pit_location in self.game.pit_locations:
            x, y = pit_location
            x1, y1 = x * cell_size, y * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            if (x, y) in self.game.explored_rooms:  # Only draw if explored
                self.canvas.create_image((x1 + x2) // 2, (y1 + y2) // 2, image=self.pit_image)

    def key_pressed(self, event):
        direction = event.char.lower()
        if direction in ['w', 'a', 's', 'd']:
            self.game.move_player(direction)
            self.perceive_cave()
            self.update_game_state()

    def shoot_arrows_prompt(self):
        direction = simpledialog.askstring("shoot arrow", "Enter direction (up, down, left, right):").lower()
        if direction in ['up', 'down', 'left', 'right']:
            result = self.game.shoot_arrows(direction)
            self.perceive_cave()
            self.update_game_state()
            messagebox.showinfo("shoot arrow", result)
        else:
            messagebox.showinfo("shoot arrow", "Invalid direction. Please enter up, down, left, or right.")

    def perceive_cave(self):
        perceptions = self.game.perceive_cave()
        self.perception_label.config(text="\n".join(perceptions))


        
    def update_game_state(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.draw_player()
        self.draw_Wumpus()
        self.draw_gold()
        self.draw_pits()

        self.arrows_label.config(text=f"arrows: {self.game.arrows}")

        result = self.game.check_game_status()
        if result:
            self.status_label.config(text=result)
            self.shoot_button.config(state=tk.DISABLED)
    
            messagebox.showinfo("Game Over", f"{result}\n")

    def restart_game(self):
        self.game.restart_game()
        self.canvas.delete("all")
        self.draw_grid()
        self.draw_player()
        self.draw_Wumpus()
        self.draw_gold()
        self.draw_pits()

        self.arrows_label.config(text=f"arrows: {self.game.arrows}")
        self.status_label.config(text="")
        self.shoot_button.config(state=tk.NORMAL)
        self.perceive_cave()

    def quit_game(self):
        self.destroy()

if __name__ == "__main__":
    app = WumpusUI()
    app.mainloop()
