X = [1, 2.5, 4, 0.5]
W = [0.4, 0.3, 0.6, 0.1]
b = 0.5

def neuron_output(X, W, b):
    """
    Compute the output of a single neuron given inputs, weights, and bias.

    Parameters:
    X (list or array): Input features.
    W (list or array): Weights corresponding to the input features.
    b (float): Bias term.

    Returns:
    float: The output of the neuron after applying the weighted sum and bias.
    """
    # Calculate the weighted sum of inputs
    weighted_sum = sum(x * w for x, w in zip(X, W))
    
    # Add the bias term
    output = weighted_sum + b
    
    return output


output = neuron_output(X, W, b)
print(output)