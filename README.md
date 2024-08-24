## Bureau of Public Roads (BPR) function

The travel time tti(e, t) of a vehicle i on an edge e at time t is given by the BPR function with a stochastic term as:


## Plan

- read statement: 15m -> 13
- chose simulation/visualization library: 5m -> 4m (Manim)
- setup + learn Manim: 1h -> 19m
- make the simulation: 4h -> 2:15 (realized manim is not the right tool: can't move multiple objects at the same time independently)
- chose pygame: 3:20 -> 
- Rmarkdown/Jupyter Notebook with commetns

So now, using this table

	Total Travel Time	Route	Freeflow Time	Minutes Waited	Where?
0	110	1_A A_C C_E E_2 	90	10	11111111AA
1	101	1_A A_C C_D D_2 	78	10	11111111AA
2	104	1_A A_C C_E E_2 	90	9	11111111A
3	103	1_A A_C C_E E_2 	90	11	11111111AAA
4	115	1_A A_C C_E E_2 	90	8	11111111
5	104	1_A A_C C_E E_2 	90	9	11111111A

Create a pygame visualization that shows the animation minute by minute