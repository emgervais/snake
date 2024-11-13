import numpy as np
import random
from collections import deque

learning_rate = 0.001
gamma = 0.95
epsilon = 1.0
epsilon_min = 0.01
epsilon_decay = 0.999
batch_size = 32
max_memory = 10000

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.W1 = np.random.randn(input_size, hidden_size) * 0.1
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.1
        self.b2 = np.zeros((1, output_size))
    
    def relu(self, x):
        return np.maximum(0, x)

    def forward(self, x):
        self.z1 = np.dot(x, self.W1) + self.b1
        self.a1 = self.relu(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        return self.z2

    def predict(self, x):
        return self.forward(x)

    def train(self, x, y, lr):
        output = self.forward(x)
        error = output - y
        dW2 = np.dot(self.a1.T, error) / x.shape[0]
        db2 = np.sum(error, axis=0, keepdims=True) / x.shape[0]
        
        d_hidden = np.dot(error, self.W2.T) * (self.z1 > 0)
        dW1 = np.dot(x.T, d_hidden) / x.shape[0]
        db1 = np.sum(d_hidden, axis=0, keepdims=True) / x.shape[0]
        
        self.W1 -= lr * dW1
        self.b1 -= lr * db1
        self.W2 -= lr * dW2
        self.b2 -= lr * db2

class ReplayBuffer:
    def __init__(self, max_size):
        self.buffer = deque(maxlen=max_size)
    
    def store(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size):
        if len(self.buffer) < batch_size:
            raise ValueError("Not enough samples in the buffer to create a batch")
        return random.sample(self.buffer, batch_size)
    
    def can_sample(self, batch_size):
        return len(self.buffer) >= batch_size
    
    def size(self):
        return len(self.buffer)

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = epsilon
        self.memory = ReplayBuffer(max_memory)
        self.model = NeuralNetwork(state_size, 100, action_size)

    def act(self, state):
        state = np.reshape(state, [1, self.state_size])
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])

    def train(self, batch_size):
        if not self.memory.can_sample(batch_size):
            return

        minibatch = self.memory.sample(batch_size)
        
        states = np.array([np.reshape(s[0], [1, self.state_size]) for s in minibatch]).squeeze()
        targets = self.model.predict(states)
        
        for i, (state, action, reward, next_state, done) in enumerate(minibatch):
            target = reward if done else reward + gamma * np.max(self.model.predict(np.reshape(next_state, [1, self.state_size]))[0])
            targets[i][action] = target

        self.model.train(states, targets, learning_rate)
        
        if self.epsilon > epsilon_min:
            self.epsilon *= epsilon_decay
