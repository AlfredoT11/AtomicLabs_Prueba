from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid

from random import choices

from agents import WorkerAgent, ZombieAgent, WallAgent

class OfficeModel(Model):
    """A model that represents the office being attacked by zombies."""

    def __init__(self, worker_pos_list, wall_list, width, height):
        self.grid = SingleGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.running = True

        self.agent_id = 1
        for worker in worker_pos_list:
            print(worker)
            a_worker = WorkerAgent(self.agent_id, self)
            self.schedule.add(a_worker)
            self.grid.place_agent(a_worker, (worker[0], worker[1]))
            self.agent_id += 1

        for wall in wall_list:
            a_wall = WallAgent(self.agent_id, self)
            self.schedule.add(a_wall)
            self.grid.place_agent(a_wall, (wall[0], wall[1]))
            self.agent_id += 1

        x_cell_zombie_1 = choices([3, 4, 5, 6, 13, 14, 15, 16])[0]
        x_cell_zombie_2 = choices([3, 4, 5, 6, 13, 14, 15, 16])[0]
        while(x_cell_zombie_1 == x_cell_zombie_2):
            x_cell_zombie_2 = choices([3, 4, 5, 6, 13, 14, 15, 16])[0]

        zombie_a_1 = ZombieAgent(self.agent_id, self)
        self.schedule.add(zombie_a_1)
        self.grid.place_agent(zombie_a_1, (x_cell_zombie_1, 19))
        self.agent_id += 1
        print(f"Zombie llegó por la ventana de la casilla {x_cell_zombie_1}, 19")

        zombie_a_2 = ZombieAgent(self.agent_id, self)
        self.schedule.add(zombie_a_2)
        self.grid.place_agent(zombie_a_2, (x_cell_zombie_2, 19))
        self.agent_id += 1
        print(f"Zombie llegó por la ventana de la casilla {x_cell_zombie_2}, 19")

        self.zombies = [zombie_a_1, zombie_a_2]      

    def step(self):
        self.schedule.step()

        for zombie in self.zombies:
            agents_around = self.grid.get_neighbors(zombie.pos, moore=True)
            for agent in agents_around:
                if isinstance(agent, WorkerAgent):
                    if not agent.is_infected:
                        agent.is_infected = True
                        print(f"Humano {agent.unique_id} infectado en la casilla {agent.pos[0]}, {agent.pos[1]}")                        

