#Mode of learning

1. Problem description
2. Layers, activation and loss(forward & backward pass)
3. optimizers
4. traning the neural network

1. Problem description :

- classify data points as R, G,B
- 

#TODO: use mermaid, graphviz and sequence diagram for visual note making
2. Layers, activation and loss:

- Layers --> Forward and backward pass
- Activation function --> forward and backward pass
- loss --> forward and backward pass


![Neural network sample](image.png)

![weight and bias for layers](image-1.png)

Counting of paramters:

- First layer : 6 weights, 3 biases--> 6+3 =9
- second layer: 9 weights, 3 biases--> 9+3=12

total paramters = 21

![Overall network](image-2.png)

Neurons --> layers

multiple hidden layers --> neural network

>Single neuron:

![Single neuron](image-3.png)

>Layer nuerons: ![layer neuron](image-4.png)
![layer neuron output](image-5.png)

>Batch of data, layer of neurons:
![batch of inputs](image-6.png)
![neuron output with batch](image-7.png)

>Forward pass: ![forward pass](image-8.png)

> Loss and backward pass:

![gradient descent](image-9.png)

>Layer backward pass:

![chain rule of parital derivative](image-10.png)

![derivative of dl/dx](image-11.png)

Partial derivatives:

![layer backward pass](image-12.png)

![dl/dz](image-13.png)

>dl/dw = X.T(dl-dz)

>dl/db = sum rows of dl-dz

>dl/dx = (dl-dz)*W.T

#Activation function:

- Linear approx straight lines.
- activation tries to be more expressive. to capture any complex function.
- available activation functions. (tanh, sigmoid, relu, softmax etc)

#Relu activation function:

>Forward pass: ![relu forward pass](image-14.png)
>Backward pass: ![relu backward pass](image-15.png)

#Softmax activation function:

>forward pass:![softmax forward pass](image-16.png)
  0<z1,z2,z3>1
  z1+z2+z3 =1 , for each inputs, we can say that this is z1 is 90%, z2 is 10% and z3 is 0%.

>backward pass: ![softmax backward pass](image-17.png)  

for backward pass of z1 wrt x1: we need to compute z2 wrt x1, z3 wrt x1 as well as shown in the pic. we will use chain function from both loss and soft max and compute backward pass.
it has to be 

# Loss function:

![categorical cross entropy loss](image-18.png)
![logloss](image-19.png)
![forward pass](image-20.png)
![one hot encoded forward pass](image-21.png)
For not one hot encoded, [0 1 1]
                         R. G. G --> take corresponding indexes on that row. 

![backward pass](image-22.png)              dl/dypred = -true/pred

# Combined backward pass for softmax and loss
![combined softmax and loss](image-23.png)

![backward pass](image-24.png) 
always divide by number of samples to prevent gradient explosion.

# Optimizers: 
 - To update weights and biases in subsquent iterations, we need optimizers.
 - Vanilla gd : 
    - w = w-(alpha)dl/dw --> fixed step size, only current gradient value is used.
    - local min, more oscillations with out converging
         

 - momentum gd:
    - ![momentum gd](image-25.png)
    - moving avg

 - RMS prop - adaptive steps
    - step size is based on the gd value. 
    - if for a param, gd is small, step size has to be large, if gd is large, step size has to be small.
    - ![adaptive step size](image-26.png)

 - Adam - adaptive momentum estimation.
    - combine adaptive steps + momentum
    - ![adam opt formula](image-27.png)
    - Typical beta values beta1 - 0.9, beta2 - 0.999
    - learning rate alpha in pratice: alpha ~= alpha_0 / 1+decay*t (t: num of iterations)

Testing: 

- overfitting reduce accuracy
- Parameters that impact overfitting
    - itertions, learning_rate, epoch, decay, epsilon, beta_1, beta_2 - hyperparamters. to improve testing.

Testing and validation data:

- Testing: To test neural net on unseen data
- validation: to optimize hyper parameters of neural net. 
    - layer neurons,  activation functions, epochs, learning rate.






