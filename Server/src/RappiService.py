from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

import random
import numpy as np
import pandas as pd

class Rappi(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = "Rappi"
        self.id = unique_id
        self.is_carrying_food = False
        self.previous_pos = None

    def move_to_food(self):
        if self.can_pick() == False:
            return
        
        target_pos = self.find_closest_food()
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True, radius=1)

        if self.pos == target_pos:
            self.pick_food()
            return
        
        self.move(target_pos, neighborhood)

    def move_to_deposit(self):
        if self.can_drop() == False:
            return

        target_pos = self.model.deposit_pos
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True, radius=1)

        if self.pos == target_pos:
            self.drop_food()
            return
        
        self.move(target_pos, neighborhood)

    def pick_food(self):
        (x, y) = self.pos
        self.model.known_food_layer[x][y] = 0
        self.model.food_layer[x][y] = 0
        self.is_carrying_food = True

    def drop_food(self):
        self.is_carrying_food = False
        self.model.deposited_food += 1
        self.move_randomly()

    def move_randomly(self):
        neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False, radius=1
        )
        self.move(self.random.choice(neighborhood), neighborhood)

    def move(self, target_pos, neighborhood):
        x = target_pos[0] - self.pos[0]
        y = target_pos[1] - self.pos[1]

        x = 1 if x > 0 else -1 if x < 0 else 0
        y = 1 if y > 0 else -1 if y < 0 else 0

        if self.pos[0] + x < 0 or self.pos[0] + x >= self.model.grid.width:
            x = 0
        if self.pos[1] + y < 0 or self.pos[1] + y >= self.model.grid.height:
            y = 0

        new_pos = (self.pos[0] + x, self.pos[1] + y)
        cellmate = self.model.grid.get_cell_list_contents(new_pos)

        max_tries = 10
        while cellmate:
            new_pos = self.random.choice(neighborhood)
            cellmate = self.model.grid.get_cell_list_contents(new_pos)
            max_tries -= 1
            if max_tries == 0:
                return

        self.model.grid.move_agent(self, new_pos)
        self.pos = new_pos

    def find_deposit(self):
        (x, y) = self.pos
        if self.model.deposit_location == (x, y):
            self.model.deposit_pos = (x, y)

    def find_closest_food(self):
        food_poss = []

        for i in range(self.model.grid.width):
            for j in range(self.model.grid.height):
                if self.model.known_food_layer[i][j] == 1:
                    food_poss.append((i, j))

        closest_food = None
        closest_distance = 1000000

        for food_pos in food_poss:
            distance = self.calculate_distance(food_pos)
            if distance < closest_distance:
                closest_food = food_pos
                closest_distance = distance
        return closest_food
    
    def calculate_distance(self, position):
        return abs(self.pos[0] - position[0]) + abs(self.pos[1] - position[1])
    
    def is_deposit_found(self):
        return self.model.deposit_pos is not None
    
    def can_pick(self):
        food_found = np.sum(self.model.known_food_layer)
        return food_found > 0 and self.is_carrying_food == False and self.is_deposit_found()
    
    def can_drop(self):
        return self.is_carrying_food == True and self.is_deposit_found()
    
    def step(self) -> None:
        self.find_deposit()

        if not self.is_carrying_food and not self.is_deposit_found():
            self.move_randomly()
            return

        self.move_to_food()
        self.move_to_deposit()

class GoogleMaps(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = "GoogleMaps"
        self.visited = set()
        self.direction = "Right"
        self.random.seed(12345)

    def move(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        unknown_neighbors = [
            cell
            for cell in neighbors
            if cell not in self.visited and self.model.grid.is_cell_empty(cell)
        ]

        if unknown_neighbors:
            new_pos = self.random.choice(unknown_neighbors)
        else:
            empty_neighbors = [
                cell
                for cell in neighbors
                if self.model.grid.is_cell_empty(cell)
            ]
            if empty_neighbors:
                new_pos = self.random.choice(empty_neighbors)
            else:
                return
            
        self.model.grid.move_agent(self, new_pos)
        self.visited.add(new_pos)

    def find_food(self):
        (x, y) = self.pos
        self.model.known_food_layer[x][y] = self.model.food_layer[x][y]

    def find_deposit(self):
        (x, y) = self.pos
        if self.model.deposit_location == (x, y):
            self.model.deposit_pos = (x, y)

    def step(self):
        self.move()
        self.find_food()
        self.find_deposit()

def get_agent_positions(model):
    return np.asarray([agent.pos for agent in model.schedule.agents])

class RappiDelivery(Model):

    __slots__ = (
        "schedule",
        "grid",
        "running",
        "food_layer",
        "known_food_layer",
        "deposit_location",
        "datacollector",
    )

    def __init__(self, width, height, num_agents, max_food = 47):
        self.schedule = SimultaneousActivation(self)
        self.grid = SingleGrid(width, height, torus=False)
        self.running = True

        self.random.seed(12345)
        self.datacollector = DataCollector(
            {
                "Food": lambda m: np.sum(m.food_layer),
                "Known Food": lambda m: np.sum(m.known_food_layer),
                "Agents": lambda m: m.schedule.get_agent_count(),
                "Agent Positions": self.get_agent_positions,
                "Food Positions": self.get_food_positions,
                "Deposit location": lambda m: m.deposit_location,
            }
        )

        self.total_food_spawned = 0
        self.picked_food_positions = set()
        self.init_food_layer = np.zeros((width, height), dtype=np.int8)
        self.food_layer = np.zeros((width, height), dtype=np.int8)
        self.known_food_layer = np.zeros((width, height), dtype=np.int8)
        self.deposit_pos = None
        self.deposit_location = None
        self.deposited_food = 0
        self.num_food = max_food

        self.spawn_food(self.num_food)
        self.spawn_deposit()
        self.spawn_agents(3, Rappi, "Rappi")
        self.spawn_agents(2, GoogleMaps, "GoogleMaps")

    def spawn_agents(self, num_agents, agent_class, prefix):

        occupied_cells = set()

        for i, _ in enumerate(range(num_agents)):
            while True:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)

                if (x, y) not in occupied_cells and self.grid.is_cell_empty((x, y)):
                    agent = agent_class((prefix, i), self)
                    self.grid.place_agent(agent, (x, y))
                    self.schedule.add(agent)

                    occupied_cells.add((x, y))
                    break
    
    def spawn_food(self, max_food):
        available_cells = [
            (x, y)
            for x in range(self.grid.width)
            for y in range(self.grid.height)
            if self.grid.is_cell_empty((x, y)) and self.food_layer[x][y] == 0 and (x, y) != self.deposit_location
        ]

        num_food = min(
            self.random.randrange(2, 6),
            max_food - self.total_food_spawned,
            len(available_cells),
        )

        for _ in range(num_food):
            x, y = self.random.choice(available_cells)
            self.food_layer[x][y] = 1
            self.init_food_layer[x][y] = 1
            self.total_food_spawned += 1
            available_cells.remove((x, y))
    
    def spawn_deposit(self):
        while True:
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            if self.grid.is_cell_empty((x, y)) and self.food_layer[x][y] == 0:
                self.deposit_location = (x, y)
                break
    
    def stop_running(self):
        return np.sum(self.food_layer) == 0 and self.deposited_food == self.num_food
    
    def get_agent_positions(model):
        agent_positions = []

        for agent in model.schedule.agents:
            key = agent.unique_id[0] + str(agent.unique_id[1])
            agent_positions.append(
                {
                    "id": key,
                    "x": agent.pos[0],
                    "y": agent.pos[1],
                    "type": agent.unique_id[0],
                }
            )

        return agent_positions
    
    def get_food_positions(model):
        food_positions = []

        for x in range(model.grid.width):
            for y in range(model.grid.height):
                value = model.food_layer[x][y]
                if value == 1 and (x, y) not in model.picked_food_positions:
                    new_pos = {"x": x, "y": y}
                    food_positions.append(new_pos)
                    model.picked_food_positions.add((x, y))

        return food_positions
    
    def step(self) -> None:
        self.schedule.step()
        self.datacollector.collect(self)

        if self.schedule.steps % 5 == 0:
            self.spawn_food(self.num_food)

        if self.stop_running():
            self.running = False

WIDTH = 20
HEIGHT = 20
NUM_AGENTS = 5
MAX_FOOD = 47

FOOD_SPAWN_INTERVAL = 5
MIN_FOOD_PER_SPAWN = 2
MAX_FOOD_PER_SPAWN = 5

def plot_simulation(model, title, figsize=(10, 10), cmap="binary"):

    data = model.food_layer.copy()

    plt.figure(figsize=figsize)

    deposit_x, deposit_y = model.deposit_location
    plt.scatter(
        deposit_y, deposit_x, color="black", marker="s", s=50, label="Deposit"
    )

    food_layer = model.init_food_layer
    for i in range(len(food_layer)):
        for j in range(len(food_layer[0])):
            box_color = "black" if food_layer[i][j] > 0 else "blue"

            plt.text(j, i, food_layer[i][j], ha="center", va="center", color=box_color)

    plt.title(title, fontsize=16, fontweight="bold")
    plt.legend(loc="lower right", bbox_to_anchor=(1, 1), fontsize=12)

    plt.xlabel("aisle", fontsize=14)
    plt.ylabel("shelf", fontsize=14)

    ax = plt.gca()
    ax.set_aspect("equal", adjustable="box")

    plt.show()

def get_data(model):

    steps = []
    all_positions = model.datacollector.get_model_vars_dataframe()
    deposit_location = {"x": model.deposit_location[0], "y": model.deposit_location[1]}
    agent_positions = all_positions["Agent Positions"]
    food_positions = all_positions["Food Positions"]

    for i in range(len(agent_positions)):
        steps.append({"id": i, "agents": agent_positions[i], "food": food_positions[i]})

    return {
        "deposit_location": deposit_location,
        "steps": steps,
        "total_steps": model.schedule.steps,
    }

def animate_simulation(model):
    data = get_data(model)

    fig, ax = plt.subplots(figsize=(10, 10))
    plt.close()

    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)

    ax.set_aspect("equal", adjustable="box")
    ax.set_title("Rappi Service", fontsize=16, fontweight="bold")

    deposit_x, deposit_y = data["deposit_location"].values()
    ax.scatter(
        deposit_y, deposit_x, color="black", marker="s", s=50, label="deposit"
    )

    deposit_label = ax.text(
        deposit_y, deposit_x, "", ha="right", va="bottom", color="black"
    )

    food_layer = np.array(model.init_food_layer)
    food = ax.imshow(food_layer, cmap="binary")

    agents = ax.scatter([], [], color="blue", marker="X", s=50, label="Agents")

    def init():
        return (food, agents)
    
    def update(frame):
        agent_positions = frame["agents"]

        for agent in agent_positions:
            x, y = agent["x"], agent["y"]
            if food_layer[x, y] > 0:
                food_layer[x, y] = 0

        food.set_data(food_layer)

        x = [agent["x"] for agent in agent_positions]
        y = [agent["y"] for agent in agent_positions]

        agents.set_offsets(np.c_[x, y])

        deposit_food_count = model.deposited_food
        deposit_label.set_text(f"DEPOSIT")

        return (food, agents)
    
    return FuncAnimation(fig, update, frames=data["steps"], init_func=init, blit=True)

def run_simulation() -> Model:
    model = RappiDelivery(20, 20, NUM_AGENTS, MAX_FOOD)

    while model.running:
        model.step()

    print(f"Simulation finished in {model.schedule.steps} steps")
    return model

model = run_simulation()

anim = animate_simulation(model)
anim