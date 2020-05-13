from manimlib.imports import *

#    __                  _   _                 
#   / _|_   _ _ __   ___| |_(_) ___  _ __  ___ 
#  | |_| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
#  |  _| |_| | | | | (__| |_| | (_) | | | \__ \
#  |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/

# This function returns data from .csv to an array
def get_coords_from_csv(file_name):
    import csv
    coords = []
    with open(f'{file_name}.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            x,y = row
            coord = [float(x),float(y)]
            coords.append(coord)
    csvFile.close()
    return coords
# LEARN MORE HERE:
# https://www.youtube.com/watch?v=Xi52tx6phRU


#        _         _                  _   
#   __ _| |__  ___| |_ _ __ __ _  ___| |_ 
#  / _` | '_ \/ __| __| '__/ _` |/ __| __|
# | (_| | |_) \__ \ |_| | | (_| | (__| |_ 
#  \__,_|_.__/|___/\__|_|  \__,_|\___|\__|
#   ___  ___ ___ _ __   ___  ___ 
#  / __|/ __/ _ \ '_ \ / _ \/ __|
#  \__ \ (_|  __/ | | |  __/\__ \
#  |___/\___\___|_| |_|\___||___/
# Abstract scenes

class GraphFromData(GraphScene):
    # Covert the data coords to the graph points
    def get_points_from_coords(self,coords):
        return [
            # Convert COORDS -> POINTS
            self.coords_to_point(px,py)
            # See manimlib/scene/graph_scene.py
            for px,py in coords
        ]

    # Return the dots of a set of points
    def get_dots_from_coords(self,coords,radius=0.1):
        points = self.get_points_from_coords(coords)
        dots = VGroup(*[
            Dot(radius=radius).move_to([px,py,pz])
            for px,py,pz in points
            ]
        )
        return dots

#       _                         
#   ___| | __ _ ___ ___  ___  ___ 
#  / __| |/ _` / __/ __|/ _ \/ __|
# | (__| | (_| \__ \__ \  __/\__ \
#  \___|_|\__,_|___/___/\___||___/
# This classes returns graphs
class DiscreteGraphFromSetPoints(VMobject):
    def __init__(self,set_of_points,**kwargs):
        super().__init__(**kwargs)
        self.set_points_as_corners(set_of_points)

class SmoothGraphFromSetPoints(VMobject):
    def __init__(self,set_of_points,**kwargs):
        super().__init__(**kwargs)
        self.set_points_smoothly(set_of_points)

#   ___  ___ ___ _ __   ___  ___ 
#  / __|/ __/ _ \ '_ \ / _ \/ __|
#  \__ \ (_|  __/ | | |  __/\__ \
#  |___/\___\___|_| |_|\___||___/


class Intro(Scene):
    def construct(self):
        line1 = TextMobject("Correlation between the number of")
        line2 = TextMobject("positive COVID-19 tests per day")
        line3 = TextMobject("and the introduction of preventive measures")
        line1.move_to(UP)
        line2.move_to(line1.get_center() + .5 * DOWN)
        line3.move_to(line2.get_center() + .5 * DOWN)
        vgroup = VGroup(line1, line2, line3)

        self.wait(1.5)
        self.play(
            Write(vgroup)
        )
        self.wait(3)

# Discrete Graph
class CustomGraph2(GraphFromData):
    CONFIG = {
        "y_max": 1060,
        "y_tick_frequency": 200,
        "y_axis_label": "Positive Tests",
        "x_max": 78,
        "x_tick_frequency": 5,
        "x_axis_label": "Days"
    }
    def construct(self):
        self.setup_axes()
        # Get coords
        coords = get_coords_from_csv("custom_graphs/epikurve")
        points = self.get_points_from_coords(coords)
        # Set graph
        graph = DiscreteGraphFromSetPoints(points,color=ORANGE)

        # Schulschließungen
        legend1 = TextMobject("School closings", color=GREEN)
        legend1.to_corner(UR)
        line1 = Line(self.coords_to_point(16, -50), self.coords_to_point(16, 250), color=GREEN)
        line2 = Line(self.coords_to_point(30, -50), self.coords_to_point(30, 250), color=GREEN)

        # Ausgangsbeschränkungen
        legend2 = TextMobject("Lockdown", color = RED)
        legend2.move_to(legend1.get_center() + .5 * DOWN)
        line3 = Line(self.coords_to_point(20, -50), self.coords_to_point(20, 250), color=RED)
        line4 = Line(self.coords_to_point(34, -50), self.coords_to_point(34, 250), color=RED)
        vgroup = VGroup(line3, line4)
        braces = Brace(vgroup, DOWN, color=RED)
        brace_text = braces.get_text("14 days")

        # MNS-Pflicht
        legend3 = TextMobject("Mandatory masks", color=BLUE)
        legend3.move_to(legend2.get_center() + .5 * DOWN)
        line5 = Line(self.coords_to_point(37, -50), self.coords_to_point(37, 250), color=BLUE)
        line6 = Line(self.coords_to_point(51, -50), self.coords_to_point(51, 250), color=BLUE)

        self.y_axis.add_numbers(*range(0, 1260, 200))

        # Set dots
        dots = self.get_dots_from_coords(coords)
        self.play(
            Write(self.x_axis),
            Write(self.y_axis),
            ShowCreation(dots),
            ShowCreation(graph, run_time=5)
        )
        self.play(
            ShowCreation(line1),
            ShowCreation(line2),
            Write(legend1)
        )
        self.play(
            ShowCreation(vgroup),
            Write(legend2)
        )
        self.play(
            ShowCreation(line5),
            ShowCreation(line6),
            Write(legend3)
        )
        self.wait(3)
        self.play(
            GrowFromCenter(braces),
            Write(brace_text)
        )
        self.wait(10)
        self.play(
            Uncreate(line1),
            Uncreate(line2),
            Uncreate(vgroup),
            Uncreate(line5),
            Uncreate(line6),
            Uncreate(braces),
            Uncreate(brace_text),
            Uncreate(legend1),
            Uncreate(legend2),
            Uncreate(legend3),
            Uncreate(dots),
            Uncreate(graph),
            Uncreate(self.x_axis),
            Uncreate(self.y_axis)
        )
        self.wait(3)
