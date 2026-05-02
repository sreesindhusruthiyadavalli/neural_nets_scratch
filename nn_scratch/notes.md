Every neuron is a logistic regression, each neuron is a linear model.

For a single neuron, the input vector x = [x₁, x₂, x₃] and the weight vector w = [w₁, w₂, w₃] exist in the same multi-dimensional feature space (e.g., 3D for three features). 

Each dimension (e.g., x₁, x₂, x₃) corresponds to a specific feature of your data point (like color, size, weight). 
The weight vector w defines a specific direction in this space.  Each weight (w₁, w₂, w₃) acts as a "tuning knob" that determines how much attention the neuron pays to the corresponding feature (x₁, x₂, x₃).
The dot product w · x calculates a single scalar value that represents the projection of the input vector x onto the direction of the weight vector w.  It measures how much the input "points in the same direction" as the weights.
The neuron's output (before activation) is this scalar: w · x + b.  A large positive value means the input is highly aligned with the learned weight direction, a large negative value means it's opposed, and zero means it's perpendicular. 
During training, the network tunes the weights (the direction of w) so that inputs from the same class are projected onto similar regions of this 1D output space, effectively creating a decision boundary (a hyperplane perpendicular to w) that separates different classes. 