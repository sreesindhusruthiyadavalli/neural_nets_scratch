Repo to try neural networks using python.

1. Single neuron , inputs = 4 --> 4 weights
X = [x1, x2, x3, x4] , W = [w1, w2, w3, w4], bias = [b]

X - vector, W - vector, b - constant

**Questions**:

- Dot product, check linear algebra.tex and linear_alg.md


2. A layer of neurons, neurons = 3, inputs = 4, 
weights = [Each neuron has 4 weights(columns) and  3(rows)] - 3 * 4 matrix
X = [x1, x2, x3, x4], 
W = [w11 w12 w13 w14
     w21 w22 w23 w24
     w31 w32 w33 w34]

X - vector[1*4], W - Matrix[3*4], b - vector [1*4] - each neuron has one bias    


3. Batch of inputs, 
neurons = 3, inputs = 4, 
weights = [Each neuron has 4 weights(columns) and  3(rows)] - 3 * 4 matrix
3 batch of inputs X = [Each row has 4 inputs(columns) and 3batches(rows)] - 3 * 4 matrix

X = [x11 x12 x13 x14           
     x21 x22 x23 x24
     x31 x32 x33 x34]    

W = [w11 w12 w13 w14
     w21 w22 w23 w24
     w31 w32 w33 w34]      

X - vector[3*4], W - Matrix[3*4], b - vector[1*4] - each neuron has one bias    


4. Dense layer -> feed forward
Outpuf of one layer --> Input to another layer


