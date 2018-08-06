Histogram-filter-for-robot-localization

A simple example of robot localization in two dimension field using discrete bayesian filter. Basically it is my solution for tha last quiz of udacity histogram filtering lesson, but a little bit further.

I'm working on the example to make it more realestic. Then I complete this readme file.

A note about movement trust: To keep it smple, when the robot thinks that it moved, either the robot moved to the correct direction or stays where it was before.

Another note that: Remember that in this example we first affect the robot movement(it can be not moving, It means that the value of our action (motion) is [0, 0]). Then we affect what the robot senses

Other notes are in the code's comments.
