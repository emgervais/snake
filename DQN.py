import numpy as np
import random
from collections import deque

# Hyperparameters
LEARNING_RATE = 0.0005
GAMMA = 0.95
EPSILON = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.995
MAX_MEMORY = 50000
HIDDEN_SIZE = 256
BATCH_SIZE = 32
TARGET_UPDATE_FREQUENCY = 1000

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.W1 = np.random.randn(input_size, hidden_size) * np.sqrt(2.0 / input_size)
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, hidden_size) * np.sqrt(2.0 / hidden_size)
        self.b2 = np.zeros((1, hidden_size))
        self.W3 = np.random.randn(hidden_size, output_size) * np.sqrt(2.0 / hidden_size)
        self.b3 = np.zeros((1, output_size))
        
    def relu(self, x):
        return np.maximum(0, x)

    def dropout(self, x, rate):
        mask = (np.random.rand(*x.shape) > rate).astype(np.float32)
        return x * mask

    def forward(self, x):
        self.z1 = np.dot(x, self.W1) + self.b1
        self.a1 = self.relu(self.z1)
        # self.a1 = self.dropout(self.a1, rate=0.2)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.relu(self.z2)
        # self.a2 = self.dropout(self.a2, rate=0.2)
        self.z3 = np.dot(self.a2, self.W3) + self.b3
        return self.z3
    
    def predict(self, x):
        return self.forward(x)
    
    def train(self, x, y, lr):
        output = self.forward(x)
        error = output - y

        # Output layer
        dW3 = np.dot(self.a2.T, error) / x.shape[0]
        db3 = np.sum(error, axis=0, keepdims=True) / x.shape[0]

        # Hidden layer 2
        d_hidden2 = np.dot(error, self.W3.T) * (self.z2 > 0)
        dW2 = np.dot(self.a1.T, d_hidden2) / x.shape[0]
        db2 = np.sum(d_hidden2, axis=0, keepdims=True) / x.shape[0]

        # Hidden layer 1
        d_hidden1 = np.dot(d_hidden2, self.W2.T) * (self.z1 > 0)
        dW1 = np.dot(x.T, d_hidden1) / x.shape[0]
        db1 = np.sum(d_hidden1, axis=0, keepdims=True) / x.shape[0]

        self.W1 -= lr * dW1
        self.b1 -= lr * db1
        self.W2 -= lr * dW2
        self.b2 -= lr * db2
        self.W3 -= lr * dW3
        self.b3 -= lr * db3

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

class DQNAgent:
    def __init__(self, state_size=8, action_size=4):
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = EPSILON
        self.memory = ReplayBuffer(MAX_MEMORY)
        self.model = NeuralNetwork(state_size, HIDDEN_SIZE, action_size)
        self.target_model = NeuralNetwork(state_size, HIDDEN_SIZE, action_size)
        self.update_target_model()
        self.steps = 0
        
    def update_target_model(self):
        self.target_model.W1 = self.model.W1.copy()
        self.target_model.b1 = self.model.b1.copy()
        self.target_model.W2 = self.model.W2.copy()
        self.target_model.b2 = self.model.b2.copy()
        self.target_model.W3 = self.model.W3.copy()
        self.target_model.b3 = self.model.b3.copy()
    
    def act(self, state):
        state = np.reshape(state, [1, self.state_size])
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])
    
    def train(self):
        if not self.memory.can_sample(BATCH_SIZE):
            return
        
        minibatch = self.memory.sample(BATCH_SIZE)
        states = np.array([s[0] for s in minibatch])
        next_states = np.array([s[3] for s in minibatch])
        actions = np.array([s[1] for s in minibatch])
        rewards = np.array([s[2] for s in minibatch])
        dones = np.array([s[4] for s in minibatch])
        
        current_q_values = self.model.predict(states)
        next_q_values = self.target_model.predict(next_states)
        
        targets = current_q_values.copy()
        for i in range(BATCH_SIZE):
            if dones[i]:
                target = rewards[i]
            else:
                target = rewards[i] + GAMMA * np.max(next_q_values[i])
            targets[i][actions[i]] = target
        
        self.model.train(states, targets, LEARNING_RATE)

        self.steps += 1
        if self.steps % TARGET_UPDATE_FREQUENCY == 0:
            self.update_target_model()
        if self.epsilon > EPSILON_MIN:
            self.epsilon *= EPSILON_DECAY