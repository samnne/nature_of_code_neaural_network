import math
import random


class Perception:

    def __init__(self, n):
        self.weights = []
        self.lc = 0.001
        for i in range(n):
            self.weights.append(random.uniform(-1, 1))

    def feed_forward(self, inputs):
        sum_val = 0
        for i in range(len(inputs)):
            sum_val += inputs[i] * self.weights[i]
        return self.activate(sum_val)

    def activate(self, num):
        return 1 if num > 0 else -1

    def train(self, inputs, desired):
        guess = self.feed_forward(inputs)
        error = desired - guess
        for i in range(len(self.weights)):
            self.weights[i] += error * inputs[i] * self.lc
        # Return whether the guess before training was correct
        return guess == desired


def f(x):
    return  2 * x -12


def generate_data(num_samples=500):
    dataset = []
    for _ in range(num_samples):
        x = random.uniform(-100, 100)
        y = random.uniform(-100, 100)
        desired = 1 if y > f(x) else -1
        dataset.append(([x, y, 1], desired))
    return dataset


p = Perception(3)
training_data = generate_data(1000)
test_data = generate_data(200)

epochs = 2500

print("Initial weights:", [round(w, 4) for w in p.weights])
print("=" * 85)

for epoch in range(1, epochs + 1):
    random.shuffle(training_data)

    weight_accumulators = [0.0] * len(p.weights)
    correct_train_steps = 0
    num_samples = len(training_data)

    for inputs, desired in training_data:
        # p.train now returns True if the perceptron guessed correctly
        was_correct = p.train(inputs, desired)
        if was_correct:
            correct_train_steps += 1

        # Accumulate weights after each update
        for i in range(len(p.weights)):
            weight_accumulators[i] += p.weights[i]

    # Calculate epoch averages
    avg_weights = [round(w / num_samples, 4) for w in weight_accumulators]
    avg_train_accuracy = (correct_train_steps / num_samples) * 100

    # Evaluate accuracy on test set using the final weights of this epoch
    test_correct = sum(
        1 for inputs, desired in test_data if p.feed_forward(inputs) == desired
    )
    test_accuracy = (test_correct / len(test_data)) * 100

    print(
        f"Epoch {epoch:2d}/{epochs} | "
        f"Avg Train Acc: {avg_train_accuracy:6.2f}% | "
        f"Test Acc: {test_accuracy:6.2f}% | "
        f"Avg Weights: {avg_weights}"
    )

print("=" * 85)
final_w = [round(w, 4) for w in p.weights]

print("Final Weights:", final_w)
