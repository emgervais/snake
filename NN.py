import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import numpy as np

class MLP:
    def __init__(self, layers = [13, 100, 100, 4], activation: str='sigmoid'):
        self.layers = layers
        self.weights = []
        self.biases = []
        self.m_w = []
        self.v_w = []
        self.m_b = []
        self.v_b = []
        self.accuracy_history = []
        self.loss_history = []
        self.test_accuracy_history = []
        self.test_loss_history = []
        self.activation, self.derivative = self.parseActivation(activation)
        self.beta1 = 0.9
        self.beta2 = 0.999
        self.epsilon = 1e-8
        self.t = 0

        for i in range(len(layers) - 1):
            weight = np.random.randn(layers[i], layers[i + 1]) * np.sqrt(2. / layers[i])
            bias = np.zeros((1, layers[i + 1]))
            self.weights.append(weight)
            self.biases.append(bias)
            self.m_w.append(np.zeros_like(weight))
            self.v_w.append(np.zeros_like(weight))
            self.m_b.append(np.zeros_like(bias))
            self.v_b.append(np.zeros_like(bias))

    def parseActivation(self, activation: str):
        if(activation == 'sigmoid'):
            return self.sigmoid, self.sigmoid_derivative
        elif(activation == 'relu'):
            return self.relu, self.relu_derivative
        elif(activation == 'tanh'):
            return self.tanh, self.tanh_derivative
        else:
            print('Error: activation function not found. Using sigmoid as default.')
            return self.sigmoid, self.sigmoid_derivative

    def forward(self, X):
        self.a = [X]

        for i in range(len(self.weights) - 1):
            z = np.dot(self.a[-1], self.weights[i]) + self.biases[i]
            a = self.activation(z)
            self.a.append(a)

        z = np.dot(self.a[-1], self.weights[-1]) + self.biases[-1]
        a = self.linear(z)
        self.a.append(a)

        return a

    def backward(self, y, learning_rate):
        m = y.shape[0]
        self.t += 1

        dz = self.a[-1] - y
        dw = np.dot(self.a[-2].T, dz) / m
        db = np.sum(dz, axis=0, keepdims=True) / m

        self.update_params(dw, db, -1, learning_rate)

        for i in range(len(self.weights) - 2, -1, -1):
            dz = np.dot(dz, self.weights[i + 1].T) * self.derivative(self.a[i + 1])
            dw = np.dot(self.a[i].T, dz) / m
            db = np.sum(dz, axis=0, keepdims=True) / m
            self.update_params(dw, db, i, learning_rate)

    def update_params(self, dw, db, index, learning_rate):
        self.m_w[index] = self.beta1 * self.m_w[index] + (1 - self.beta1) * dw
        self.v_w[index] = self.beta2 * self.v_w[index] + (1 - self.beta2) * (dw ** 2)
        self.m_b[index] = self.beta1 * self.m_b[index] + (1 - self.beta1) * db
        self.v_b[index] = self.beta2 * self.v_b[index] + (1 - self.beta2) * (db ** 2)

        m_w_hat = self.m_w[index] / (1 - self.beta1 ** self.t)
        v_w_hat = self.v_w[index] / (1 - self.beta2 ** self.t)
        m_b_hat = self.m_b[index] / (1 - self.beta1 ** self.t)
        v_b_hat = self.v_b[index] / (1 - self.beta2 ** self.t)

        self.weights[index] -= learning_rate * m_w_hat / (np.sqrt(v_w_hat) + self.epsilon)
        self.biases[index] -= learning_rate * m_b_hat / (np.sqrt(v_b_hat) + self.epsilon)

    def fit(self, X, y, X_test, Y_test, epochs, learning_rate, patience=10):
        best_loss = np.inf
        patience_counter = 0

        for epoch in range(epochs):
            y_pred = self.forward(X)
            loss = mean_squared_error(y, y_pred)
            self.backward(y, learning_rate)

            y_test_pred = self.forward(X_test)
            test_loss = mean_squared_error(Y_test, y_test_pred)
            self.loss_history.append(loss)
            self.accuracy_history.append(np.mean(np.argmax(y_pred, axis=1) == np.argmax(y, axis=1)))
            self.test_loss_history.append(test_loss)
            self.test_accuracy_history.append(np.mean(np.argmax(y_test_pred, axis=1) == np.argmax(Y_test, axis=1)))

            if test_loss < best_loss:
                best_loss = test_loss
                patience_counter = 0
            else:
                patience_counter += 1
            
            if patience_counter >= patience:
                print(f'Early stopping at epoch {epoch}/{epochs} - Best Val_loss: {best_loss:.4f}')
                break
            if epoch % 10 == 0:
                print(f'Epoch {epoch}/{epochs} - Loss: {loss:.4f} - Val_loss: {test_loss:.4f} - Accuracy: {self.accuracy_history[epoch] * 100:.2f} ')

    def predict(self, X):
        y_pred = self.forward(X)
        return np.argmax(y_pred, axis=1)
    
    def visualize(self):
        plt.figure(1)
        plt.plot((np.array(self.accuracy_history) * 100))
        plt.plot((np.array(self.test_accuracy_history) * 100), color='red')
        plt.xlabel('epochs')
        plt.ylabel('accuracy')
        plt.legend(['train', 'validation'])
        plt.figure(2)
        plt.plot(self.loss_history)
        plt.plot(self.test_loss_history, color='red')
        plt.xlabel('epochs')
        plt.ylabel('loss')
        plt.legend(['train', 'validation'])
        plt.show()

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def relu_derivative(self, x):
        return np.where(x > 0, 1, 0)

    def tanh(self, x):
        return np.tanh(x)
    
    def tanh_derivative(self, x):
        return 1 - np.tanh(x) ** 2
    
    def softmax(self, x):
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)
    
    def linear(self, x):
        return x

    def binary_cross_entropy(self, y_true, y_pred):
        epsilon = 1e-15
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        return -np.mean(np.sum(y_true * np.log(y_pred), axis=1))