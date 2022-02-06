from mesa import Agent

from random import choices

class ZombieAgent(Agent):
    """A class for the Zombie. It must catch the workers."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        for i in range(4):
            self.move()


    def move(self):
        
        move_option = choices([0, 1, 2, 3, 4, 5, 6, 7])[0]
        #print(self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False))
        #print(f"Seleccionada: {move_option}")
        if move_option == 0: #Right up
            #print(0)
            new_position = (self.pos[0]+1, self.pos[1]+1)
        elif move_option == 1: #Right
            #print(1)
            new_position = (self.pos[0]+1, self.pos[1])
        elif move_option == 2: #Right down
            #print(2)
            new_position = (self.pos[0]+1, self.pos[1]-1)
        elif move_option == 3: #Down
            #print(3)
            new_position = (self.pos[0], self.pos[1]-1)
        elif move_option == 4: #Down left
            #print(4)
            new_position = (self.pos[0]-1, self.pos[1]-1)
        elif move_option == 5: #Left
            #print(5)
            new_position = (self.pos[0]-1, self.pos[1])
        elif move_option == 6: #Left up
            #print(6)
            new_position = (self.pos[0]-1, self.pos[1]+1)
        else: #Up
            #print(7)
            new_position = (self.pos[0], self.pos[1]+1)

        if not self.model.grid.out_of_bounds(new_position) and self.model.grid.is_cell_empty(new_position):
            self.model.grid.move_agent(self, new_position)


class WorkerAgent(Agent):
    """A class for the Worker. It must escape from the zombies."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.has_escaped = False
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

                new_zombie = ZombieAgent(self.model.agent_id, self.model)
                self.model.schedule.add(new_zombie)
                self.model.grid.place_agent(new_zombie, new_zombie_pos)
                self.model.agent_id += 1

                self.model.zombies.append(new_zombie)
            return

        for i in range(2):
            if(not self.has_escaped):
                self.check_zone()
                #print(f"My pos {self.pos} in zone {self.current_zone}.")

                if self.current_zone == 5:
                    self.difference_pos_target = (19 - self.pos[0], 2 - self.pos[1])
                elif self.current_zone == 4:
                    superior_passage = (16, 8)
                    inferior_passage = (16, 2)

                    distance_superior = ((superior_passage[0] - self.pos[0])**2 + (superior_passage[1] - self.pos[1])**2)
                    distance_inferior = ((inferior_passage[0] - self.pos[0])**2 + (inferior_passage[1] - self.pos[1])**2)

                    if distance_superior < distance_inferior:
                        self.difference_pos_target = (superior_passage[0] - self.pos[0], superior_passage[1] - self.pos[1])
                    else:
                        self.difference_pos_target = (inferior_passage[0] - self.pos[0], inferior_passage[1] - self.pos[1])
                elif self.current_zone == 3:
                    superior_passage = (12, 8)
                    inferior_passage = (12, 2)

                    distance_superior = ((superior_passage[0] - self.pos[0])**2 + (superior_passage[1] - self.pos[1])**2)
                    distance_inferior = ((inferior_passage[0] - self.pos[0])**2 + (inferior_passage[1] - self.pos[1])**2)

                    if distance_superior < distance_inferior:
                        self.difference_pos_target = (superior_passage[0] - self.pos[0], superior_passage[1] - self.pos[1])
                    else:
                        self.difference_pos_target = (inferior_passage[0] - self.pos[0], inferior_passage[1] - self.pos[1])
                elif self.current_zone == 2:
                    self.difference_pos_target = (10 - self.pos[0], 9 - self.pos[1])
                elif self.current_zone == 1:
                    x_distances = [abs(1 - self.pos[0]), abs(9 - self.pos[0]), abs(17-self.pos[0])]
                    min_x_distance = min(x_distances)
                    min_x_distance_index = x_distances.index(min_x_distance)

                    #print(f"Distance: {min_x_distance} index: {min_x_distance_index}")

                    if(min_x_distance_index == 0):
                        self.difference_pos_target = (1 - self.pos[0], 15 - self.pos[1])
                    elif(min_x_distance_index == 1):
                        self.difference_pos_target = (9 - self.pos[0], 15 - self.pos[1])
                    elif(min_x_distance_index == 2):
                        self.difference_pos_target = (17 - self.pos[0], 15 - self.pos[1])


                self.calculate_probabilities_of_movement()
                self.move()

                if(self.pos[0] == 19):
                    print(f"Humano {self.unique_id} salvado en la casilla {self.pos[0]}, {self.pos[1]}")
                    self.model.grid.remove_agent(self)
                    self.model.schedule.remove(self)
                    self.has_escaped = True
            


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

    def calculate_probabilities_of_movement(self):
        if self.difference_pos_target[0] > 0:
            if self.difference_pos_target[1] > 0:
                #print("RU")
                self.move_probabilities = [0.25, 0.25, 0.05, 0.05, 0.05, 0.05, 0.05, 0.25] #Right and up
            elif self.difference_pos_target[1] < 0:
                #print("RD")
                self.move_probabilities = [0.05, 0.25, 0.25, 0.25, 0.05, 0.05, 0.05, 0.05] #Right and down
            else:
                #print("R")
                self.move_probabilities = [0.04, 0.72, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04] #Right
        elif self.difference_pos_target[0] < 0:
            if self.difference_pos_target[1] > 0:
                #print("LU")
                self.move_probabilities = [0.05, 0.05, 0.05, 0.05, 0.05, 0.25, 0.25, 0.25] #Left and up
            elif self.difference_pos_target[1] < 0:
                #print("LD")
                self.move_probabilities = [0.05, 0.05, 0.05, 0.25, 0.25, 0.25, 0.05, 0.05] #Left and down
            else:
                #print("L")
                self.move_probabilities = [0.04, 0.04, 0.04, 0.04, 0.04, 0.72, 0.04, 0.04] #Left
        else:
            if self.difference_pos_target[1] > 0:
                #print("U")
                self.move_probabilities = [0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.72] #Up
            elif self.difference_pos_target[1] < 0:
                #print("D")
                self.move_probabilities = [0.04, 0.04, 0.04, 0.72, 0.04, 0.04, 0.04, 0.04] #Down
            else:
                #print("A")
                self.move_probabilities = [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]
        

    def move(self):
        
        move_option = choices([0, 1, 2, 3, 4, 5, 6, 7], self.move_probabilities)[0]
        #print(self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False))
        #print(f"Seleccionada: {move_option}")
        if move_option == 0: #Right up
            #print(0)
            new_position = (self.pos[0]+1, self.pos[1]+1)
        elif move_option == 1: #Right
            #print(1)
            new_position = (self.pos[0]+1, self.pos[1])
        elif move_option == 2: #Right down
            #print(2)
            new_position = (self.pos[0]+1, self.pos[1]-1)
        elif move_option == 3: #Down
            #print(3)
            new_position = (self.pos[0], self.pos[1]-1)
        elif move_option == 4: #Down left
            #print(4)
            new_position = (self.pos[0]-1, self.pos[1]-1)
        elif move_option == 5: #Left
            #print(5)
            new_position = (self.pos[0]-1, self.pos[1])
        elif move_option == 6: #Left up
            #print(6)
            new_position = (self.pos[0]-1, self.pos[1]+1)
        else: #Up
            #print(7)
            new_position = (self.pos[0], self.pos[1]+1)

        if not self.model.grid.out_of_bounds(new_position) and self.model.grid.is_cell_empty(new_position):
            self.model.grid.move_agent(self, new_position)   


        #new_position = self.random.choice(possible_steps)
        #self.model.grid.move_agent(self, new_position)


class WallAgent(Agent):
    """A class for the behaviour of a wall. Basically, it just stands at the same place."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass        