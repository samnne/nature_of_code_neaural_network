import math
import random


class DNA:

    def __init__(self, length: int = 18):
        self.fitness = 0
        self.genes = []
        for i in range(length):
            num = random.randint(32, 87 + 32)
            c = chr(num)
            self.genes.append(c)

    def s_join(self):
        return "".join(self.genes)

    def calc_fitness(self, target: str):
        score = 0
        for i in range(len(target)):
            if self.genes[i] == target[i]:
                score += 1
        self.fitness = score / len(target)

    def crossover(self, partner: DNA):
        n = len(self.genes)
        child = DNA(n)
        mid = random.randint(0, n - 1)

        for i in range(n):
            if i < mid:
                child.genes[i] = self.genes[i]
            else:
                child.genes[i] = partner.genes[i]
        return child

    def mutate(self, mutateRate, target: str):
        for i in range(len(self.genes)):
            if self.genes[i] != target[i] and random.random() < mutateRate:
                num = random.randint(32, 127)
                c = chr(num)

                self.genes[i] = c


def r_val(arr):
    length = len(arr)
    if length == 0:
        return
    v = random.randint(0, length - 1)
    return arr[v]


def main() -> None:

    target = "to be or not to be that is the question?"
    pop: list[DNA] = [DNA(len(target)) for i in range(150)]
    i = 0
    while target != pop[i % len(pop)]:
        for phrase in pop:
            phrase.calc_fitness(target)

        mating_pool = []
        for phrase in pop:
            n = math.floor((phrase.fitness) * 100)
            for j in range(n):
                mating_pool.append(phrase)
        for phrase in pop:

            p1 = r_val(mating_pool)
            p2 = r_val(mating_pool)
            child = p1.crossover(p2)
            child.mutate(0.5, target)
            pop[i % len(pop)] = child
        print(f"Generation {i}:  {pop[i % len(pop)].s_join()}")
        if pop[i % len(pop)].s_join() == target:
            return
        i += 1
