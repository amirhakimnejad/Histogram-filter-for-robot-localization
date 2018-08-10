# Histogram-filter-for-robot-localization

A simple example of robot localization in two dimension field using discrete bayesian filter. Basically it is my solution for the last quiz of udacity histogram filtering lesson, but a bit further.

### Prerequisites
To see the change of the robotField distribution, you need to use matlab to draw the distribution.csv file in an infinite while loop to see the change of the distribution over different measurements and actions.

### Installing

To use it, first you just need to clone it using

```
git clone git@github.com:amirhakimnejad/Histogram-filter-for-robot-localization.git
```

To use it for fun, just enter following code in terminal:

```
python3 2DHistogramLocalization.py
```

Here is your football field and a robot in it. A note that the robot hasn't seen anything or moved anywhere yet. It means we have a uniform distribution of the probability. It has no idea where it is right now.

![Alt text](readmePics/ReadyState.png?raw=true "Ready state of the robot in the field")

If you have matlab, open plotDistribution.m and run it.You will get this as result:

![Alt text](readmePics/UniformInReadyState.jpg?raw=true "Uniform distribution")

Shortcuts of the inputs:

Press 'a' for going left.

Press 'w' for going up.

Press 'd' for going right.

Press 's' for going down.

Press 'k' for kidnapped scenario.

Press 'q' to stop the program.

Kidnapped scenario is when someone just pick up the robot and put it somewhere else.

Any other input considers as a stand frame. The robot senses but he stands where he is.

You can simply change values of local variables to have different field dimensions, different length of what the robot sees, different sensor or action trust or anything else(See variables section).

I tried my best to implement the code as relative as possible.

As you move, the algorithm adds up the probability of where you were to where you might go and it uses bayes rule to count the probability of where you are using the robot sensors data of what it sees around itself.

I'll explain more in Algorithm and functions sections.

After first input, the robot starts to sense. Watch the change of our distribution:

![Alt text](readmePics/FirstSense.jpg?raw=true "First Sense")

![Alt text](readmePics/DistAfterFirstSense.jpg?raw=true "Distribution After First  Sense")

As you can see all the probabilities are affected based on what the robot see.

If you go right enough, the robot starts seeing lines, Watch the changes:

![Alt text](readmePics/LineDetected.jpg?raw=true "Line Detected")

![Alt text](readmePics/DistAfterLineDetection.jpg?raw=true "Distribution After Line Detection")


### Algorithm

This implementation is based on histogram filter algorithm.

![Alt text](readmePics/AlgorithmDiscreteBayesFilter.png?raw=true "Algorithm")

It is a screenshot of [Probabilistic Robotics](https://play.google.com/store/books/details?pcampaignid=books_read_action&id=wjM3AgAAQBAJ) book written by Sebastian Thrun, Wolfram Burgard and Dieter Fox.

### How each function works

```python
draw(i, j, A, B, E, F, G, H, realRobotPose, fieldRow, visual)
```

Watch [this repo](https://github.com/amirhakimnejad/Program-to-draw-a-football-field)

The only difference between the repo and the function is realRobotPose, fieldRow, visual inputs.If the visual argument is true it simply works just like the repo and it makes the position of the robot(We know where it is but it doesn't) on the field, red. With visual set to False the function makes a two dimension array of the field.

```python
drawer(A, B, E, F, G, H, realRobotPose, visual)
```

It just helps to separate rows from columns. It is actually an entry to call draw() function.

```python
robotMover(i, j, realRobotPose, kidnapped = False):
```

It simply gets the realRobotPose(where it really is) and affect our input key and change its location on the field. Note that the function has nothing to do with the robot knowledge.

```python
localize(p, field, measurement, motion, sensorTrust, actionTrust)
```

It gets the distribution of what the robot knows, its measurment(what it sees) motion(where it wants to go), sensorTrust and actionTrust.The function affect robot's motion in the distribution, then affect the measurment in the distribution and it normalizes it.  

Other functions are easy to undrestand. Ask question if you want me to explain them.

### Meaning of variables

#### Global variables:

A: Field length

B: Field width

E: Penalty area length

F: Penalty area width

G: Penalty cross distance

H: Center circle diameter


realRobotPose: realRobotPose is where the robot really is(the red block in terminal) but it does'nt know.So the measurement is based on this position of the field.The robot thinks he is somewhere else but what he sees is matching with the realRobotPose environment.So it tries to localize itself based on this.

measurementLength: measurement is a square matrix of what the robot sees.

sensorTrust: sensorTrust is the sensors trustworthiness. It is it's probability of being right about what it sees.

actionTrust: actionTrust is how much the robot is sure about his movement in the right direction.

inputLuck: inputLuck is the percentage of the luck that input work or not. That means you may press 'd' for example but the robot stays where it was beforeself.It is seperate from motion or measurement trust. Its more like a noise.

robotField: robotField is a two dimensional matrix of what he knows about the real field.It's kind of a map of the empty field that he use to compare its measurments with is.

p: p is the uniform distribution that the robot has no idea where it is at first.

Notes:
To keep it simple, when the robot thinks that it moved, either the robot moved to the correct direction or stays where it was before.

Remember that in this example we first affect the robot movement(it can be not moving, It means that the value of our action (motion) is [0, 0]). Then we affect what the robot senses

## Authors

* **Amirhossein Hakimnejad** - *Initial work* - [amirhakimnejad](https://github.com/amirhakimnejad)

## License

This project is licensed under the MIT License


Feel free to ask questions or anything else.
