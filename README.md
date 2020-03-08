## Flying on a 2D-grid with Obstacles

To run the project, clone the repo and navigate into `intent_prediction` folder.

Run `python3 main.py`

How to simulate:
  1) Specify the number of rows and columns for the flying zone
  2) Specify the number of obstacles (max 5)
  3) For each obstacle, give the intent (AVOID, REACH, NO_INTENT)
  
The flying zone will be created with the given obstacles

Now, moves can be performed by pressing the keys:
  1) a or A to move LEFT (L)
  2) s or S to move DOWN (D)
  3) w or W to move UP (U)
  4) d or D to move RIGHT (R)
  5) i or I to move to a cell that is diagonally LEFT_UP (LU)
  6) o or O to move to a cell that is diagonally RIGHT_UP (RU)
  7) j or J to move to a cell that is diagonally LEFT_DOWN (LD)
  8) k or K to move to a cell that is diagonally RIGHT_DOWN (RD)
  
Upon reaching the goal, the simulation ends.

### Understanding the plot

![Intent Violation](https://github.com/nagarajan-shanmuganathan/intent_prediction/blob/master/intent_violation.png)

The starting point in the big green dot and the goal is to reach the big blue dot.

From the picture we can see that there are 5 obstacles. The violet and the brown obstacles have the intents "REACH", so they have been visited. We can also see that the red obstacle has cross marks on its vertices, which denote that the intent specification was not met. It was supposed to be "AVOID", meaning, the trajectory should not touch the obstacle, but we can see that was not the case.

### Output json file

The [JSON file](https://github.com/nagarajan-shanmuganathan/intent_prediction/blob/master/output_data.txt) is generated after reaching the goal. 
