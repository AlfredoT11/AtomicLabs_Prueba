from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from model import OfficeModel
from agents import WorkerAgent, ZombieAgent, WallAgent

def agent_portrayal(agent):
    portrayal = {
        "Shape" : "circle",
        "Filled" : "true",
        "r" : 0.5
    }

    portrayal = {
        "Layer" : 0
    }

    if isinstance(agent, WallAgent):
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8
        portrayal["Color"] = "black"
    elif isinstance(agent, WorkerAgent):
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "true"
        portrayal["r"] = 0.8
        if agent.is_infected:
            portrayal["Color"] = "yellow"
        else:
            portrayal["Color"] = "blue"
    elif isinstance(agent, ZombieAgent):
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "true"
        portrayal["r"] = 0.8
        portrayal["Color"] = "red"        

    return portrayal


if __name__ == "__main__":
    
    grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)
    visualization_representations = [grid]
    
    worker_pos_list = [
                        (9, 18), 
                        (3, 16), 
                        (6, 16), 
                        (11, 16), 
                        (15, 16), #5
                        (4, 14), 
                        (15, 13), 
                        (2, 12), 
                        (7, 12), 
                        (3, 11), 
                        (17, 11), 
                        (11, 10), #7
                        (13, 7), 
                        (3, 6), 
                        (17, 6), 
                        (6, 5), 
                        (10, 4), 
                        (3, 2), 
                        (7, 2), 
                        (13, 2)
    ]
    
    wall_list = [
        (0, 19), (1, 19), (2, 19), (7, 19), (8, 19), (9, 19), (10, 19), (11, 19), (12, 19), (17, 19), (18, 19), (19, 19),
        (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), 
        (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (0, 16), (0, 17), (0, 18),
        (19, 5), (19, 6), (19, 7), (19, 8), (19, 9), (19, 10), 
        (19, 11), (19, 12), (19, 13), (19, 14), (19, 15), (19, 16), (19, 17), (19, 18),
        
        (2, 15), (3, 15), (4, 15), (5, 15), (6, 15), (7, 15), 
        (10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (16, 15), (13, 14), (13, 13), (13, 12),
        (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), 
        (12, 9), (13, 9), (14, 9), (15, 9), (16, 9), (17, 9), (18, 9), 
        
        (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), 
        (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), 
        (12, 4), (12, 5), (12, 6), (12, 7), 
        (16, 4), (16, 5), (16, 6), (16, 7), 
        (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), 
        (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0), (18, 0), (19, 0)
    ]

    server = ModularServer(
            OfficeModel, 
            visualization_representations, 
            "Zombie attack model", 
            {
                "worker_pos_list" : worker_pos_list,
                "wall_list" : wall_list,
                "width" : 20,
                "height" : 20
            }
        )

    server.verbose = False

    server.port = 8521 #Default port
    server.launch()        

