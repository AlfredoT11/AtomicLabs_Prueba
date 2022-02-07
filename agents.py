from mesa import Agent

from random import choices

class ZombieAgent(Agent):
    """A class for the Zombie. It must catch the workers."""

    def __init__(self, unique_id, model, first_position):
        super().__init__(unique_id, model)
        self.last_position = first_position

    def step(self):
        for i in range(4):
            self.move()


    def move(self):
        
        move_option = choices([0, 1, 2, 3, 4, 5, 6, 7])[0]

        if move_option == 0: #Right up
            new_position = (self.pos[0]+1, self.pos[1]+1)
        elif move_option == 1: #Right
            new_position = (self.pos[0]+1, self.pos[1])
        elif move_option == 2: #Right down
            new_position = (self.pos[0]+1, self.pos[1]-1)
        elif move_option == 3: #Down
            new_position = (self.pos[0], self.pos[1]-1)
        elif move_option == 4: #Down left
            new_position = (self.pos[0]-1, self.pos[1]-1)
        elif move_option == 5: #Left
            new_position = (self.pos[0]-1, self.pos[1])
        elif move_option == 6: #Left up
            new_position = (self.pos[0]-1, self.pos[1]+1)
        else: #Up
            new_position = (self.pos[0], self.pos[1]+1)

        is_same_last_position = self.last_position[0] == new_position[0] and self.last_position[1] == new_position[1]

        if not self.model.grid.out_of_bounds(new_position) and self.model.grid.is_cell_empty(new_position) and not is_same_last_position:
            self.model.grid.move_agent(self, new_position)
            self.last_position = new_position
            


class WorkerAgent(Agent):
    """A class for the Worker. It must escape from the zombies."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.is_infected = False
        self.infected_steps = 0

    def step(self):

        if self.is_infected:
            if self.infected_steps != 2:
                self.infected_steps += 1
            else:
                new_zombie_pos = self.pos

                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)

                new_zombie = ZombieAgent(self.model.agent_id, self.model, new_zombie_pos)
                self.model.schedule.add(new_zombie)
                self.model.grid.place_agent(new_zombie, new_zombie_pos)
                self.model.agent_id += 1

                self.model.zombies.append(new_zombie)
            return

        for i in range(2):
            self.check_zone()

            if self.current_zone == 5:
                self.zone_5_calculations()
            elif self.current_zone == 4:
                self.zone_4_calculations()
            elif self.current_zone == 3:
                self.zone_3_calculations()
            elif self.current_zone == 2:
                self.zone_2_calculations()
            elif self.current_zone == 1:
                self.zone_1_calculations()

            self.calculate_probabilities_of_movement()
            self.move()

            if(self.pos[0] == 19):
                print(f"Humano {self.unique_id} salvado en la casilla {self.pos[0]}, {self.pos[1]}")
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
                self.model.saved_workers += 1
                return

    def check_zone(self):
        """The map is divided in 5 zones. In each zone the agent will take different movement decisions."""
        if self.pos[1] > 15:
            self.current_zone = 1
        elif self.pos[1] > 8:
            self.current_zone = 2
        elif self.pos[0] < 12 and self.pos[1] < 9:
            self.current_zone = 3
        elif self.pos[0] < 17 and self.pos[1] < 9:
            self.current_zone = 4
        elif self.pos[0] < 20 and self.pos[1] < 9:
            self.current_zone = 5

    def zone_1_calculations(self):
        """This zone has 3 possible exits. The agent will choose the exit that's closer in the x coordinate."""
        x_distances = [abs(1 - self.pos[0]), abs(9 - self.pos[0]), abs(17-self.pos[0])]
        min_x_distance = min(x_distances)
        min_x_distance_index = x_distances.index(min_x_distance)

        if(min_x_distance_index == 0):
            self.difference_pos_target = (1 - self.pos[0], 15 - self.pos[1])
        elif(min_x_distance_index == 1):
            self.difference_pos_target = (9 - self.pos[0], 15 - self.pos[1])
        elif(min_x_distance_index == 2):
            self.difference_pos_target = (17 - self.pos[0], 15 - self.pos[1])

    def zone_2_calculations(self):
        """This zone only has 1 exit, so the movement must be in that direction."""
        self.difference_pos_target = (10 - self.pos[0], 9 - self.pos[1])

    def zone_3_calculations(self):
        """This zone has 2 exits. The agent selects the one that is closer to it."""
        superior_passage = (12, 8)
        inferior_passage = (12, 2)

        distance_superior = ((superior_passage[0] - self.pos[0])**2 + (superior_passage[1] - self.pos[1])**2)
        distance_inferior = ((inferior_passage[0] - self.pos[0])**2 + (inferior_passage[1] - self.pos[1])**2)

        if distance_superior < distance_inferior:
            self.difference_pos_target = (superior_passage[0] - self.pos[0], superior_passage[1] - self.pos[1])
        else:
            self.difference_pos_target = (inferior_passage[0] - self.pos[0], inferior_passage[1] - self.pos[1])

    def zone_4_calculations(self):
        """This zone has 2 exits. The agent selects the one that is closer to it."""
        superior_passage = (16, 8)
        inferior_passage = (16, 2)

        distance_superior = ((superior_passage[0] - self.pos[0])**2 + (superior_passage[1] - self.pos[1])**2)
        distance_inferior = ((inferior_passage[0] - self.pos[0])**2 + (inferior_passage[1] - self.pos[1])**2)

        if distance_superior < distance_inferior:
            self.difference_pos_target = (superior_passage[0] - self.pos[0], superior_passage[1] - self.pos[1])
        else:
            self.difference_pos_target = (inferior_passage[0] - self.pos[0], inferior_passage[1] - self.pos[1])

    def zone_5_calculations(self):
        """This is the zone of the general exit. The agents must move towards it."""
        self.difference_pos_target = (19 - self.pos[0], 2 - self.pos[1])            

    def calculate_probabilities_of_movement(self):
        """ Depending on the difference between the current position and the target position the probabilities
            of movement are changed in order to reach easier the target position.  
        """
        if self.difference_pos_target[0] > 0:
            if self.difference_pos_target[1] > 0:
                self.move_probabilities = [0.25, 0.25, 0.05, 0.05, 0.05, 0.05, 0.05, 0.25] #Right and up
            elif self.difference_pos_target[1] < 0:
                self.move_probabilities = [0.05, 0.25, 0.25, 0.25, 0.05, 0.05, 0.05, 0.05] #Right and down
            else:
                self.move_probabilities = [0.04, 0.72, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04] #Right
        elif self.difference_pos_target[0] < 0:
            if self.difference_pos_target[1] > 0:
                self.move_probabilities = [0.05, 0.05, 0.05, 0.05, 0.05, 0.25, 0.25, 0.25] #Left and up
            elif self.difference_pos_target[1] < 0:
                self.move_probabilities = [0.05, 0.05, 0.05, 0.25, 0.25, 0.25, 0.05, 0.05] #Left and down
            else:
                self.move_probabilities = [0.04, 0.04, 0.04, 0.04, 0.04, 0.72, 0.04, 0.04] #Left
        else:
            if self.difference_pos_target[1] > 0:
                self.move_probabilities = [0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.72] #Up
            elif self.difference_pos_target[1] < 0:
                self.move_probabilities = [0.04, 0.04, 0.04, 0.72, 0.04, 0.04, 0.04, 0.04] #Down
            else:
                self.move_probabilities = [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]
        

    def move(self):
        
        move_option = choices([0, 1, 2, 3, 4, 5, 6, 7], self.move_probabilities)[0]

        if move_option == 0: #Right up
            new_position = (self.pos[0]+1, self.pos[1]+1)
        elif move_option == 1: #Right
            new_position = (self.pos[0]+1, self.pos[1])
        elif move_option == 2: #Right down
            new_position = (self.pos[0]+1, self.pos[1]-1)
        elif move_option == 3: #Down
            new_position = (self.pos[0], self.pos[1]-1)
        elif move_option == 4: #Down left
            new_position = (self.pos[0]-1, self.pos[1]-1)
        elif move_option == 5: #Left
            new_position = (self.pos[0]-1, self.pos[1])
        elif move_option == 6: #Left up
            new_position = (self.pos[0]-1, self.pos[1]+1)
        else: #Up
            new_position = (self.pos[0], self.pos[1]+1)

        if not self.model.grid.out_of_bounds(new_position) and self.model.grid.is_cell_empty(new_position):
            self.model.grid.move_agent(self, new_position)   



class WallAgent(Agent):
    """A class for the behaviour of a wall. Basically, it just stands at the same place."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass        