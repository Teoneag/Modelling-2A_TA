# Traffic congestion management using network modeling

![Visualization For Traffic Flow](./ss/Visualization%201.png)

## ToDo

- make a data model for the road network
- import, export road network
- edit nodes (drag & drop)
- make the distance between nodes proportional to the real distances in the visualization
- fix city 1 0 people bug
- show at each edge the decisions: 20m -> 7m
  - modify this to show at each intersection where multiple routes are available the probability with wich each route is chosen
- run the simulation from the visualization
- explore real data sets related to the project
  - Netherlands-wide data
- dive deeper into the paper
- dynamic routing (extension)
- Rmarkdown/Jupyter Notebook with commetns

## Done (Plan time (7h:55m) -> Real time (6h:54m))

- read statement: 15m -> 13m
- chose simulation/visualization library: 5m -> 4m (Manim)
- setup + learn Manim: 1h -> 19m
- visualziation with Manim: 4h -> 2h:15m (realized manim is not the right tool: can't move multiple objects at the same time independently)
- visualization with pygame: 1h:45m
- capacity for each road: 10m -> 45m
- step button: 10m
- style: better position everything, add icons: 10m -> 2h:46m
- Intensitate culoare for traffic: 20m -> 22m
- Tried this real world data set: https://english.ndw.nu/our-data: 1h
  - can't get the nr of lanes
- Played with osmnx library: 1h

## Old look

![Old Visualization For Traffic Flow](./ss/Visualization%200.png)