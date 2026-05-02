X = [1, 2.5, 4, 0.5] # Inputs for each neuron
W = [[0.4, 0.3, 0.6, 0.1],
     [0.2, 0.8, 0.4, 0.9],
     [0.9, 0.1, 0.5, 0.7]] # Weights for 3 neurons , each row corresponds to weights of one single neuron
b = [0.5, 0.2, 0.1] # Bias for each neuron

def layer_output(X, W, b):
    """
    Compute the output of a layer of neurons given inputs, weights, and biases.

    Parameters:
    X (list or array): Input features.
    W (list of lists or 2D array): Weights for each neuron in the layer.
    b (list or array): Bias terms for each neuron.

    Returns:
    list: The outputs of the layer after applying the weighted sums and biases.
    """
    outputs = []
    # Iterate over each neuron's weights and bias
    for weights, bias in zip(W, b):
        # Calculate the weighted sum of inputs for the neuron
        weighted_sum = sum(x * w for x, w in zip(X, weights))
        # Add the bias term
        neuron_output = weighted_sum + bias
        outputs.append(neuron_output)
    
    return outputs
    