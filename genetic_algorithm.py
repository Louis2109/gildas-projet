#!/usr/bin/env python3
"""
Genetic Algorithm for Antenna Array Optimization
=================================================

Implements a binary Genetic Algorithm to optimize the phase matrix (φ_mn)
of an antenna array. The chromosome represents a flattened M×N binary matrix.

Key Features:
- Tournament selection
- One-point crossover
- Bit-flip mutation
- Elitism strategy
"""

import numpy as np
from typing import Tuple, List, Optional


class AntennaGeneticAlgorithm:
    """
    Genetic Algorithm class for antenna array optimization
    
    Attributes:
        M, N (int): Array dimensions
        d, k (float): Physical parameters (spacing, wave number)
        population_size (int): Number of individuals in population
        mutation_rate (float): Probability of bit mutation
        crossover_rate (float): Probability of crossover
        elite_size (int): Number of best individuals to preserve
    """
    
    def __init__(
        self,
        M: int = 8,
        N: int = 8,
        d: float = 0.5,
        k: float = 2 * np.pi,
        population_size: int = 50,
        mutation_rate: float = 0.05,
        crossover_rate: float = 0.7,
        elite_size: int = 5
    ):
        """Initialize Genetic Algorithm parameters"""
        self.M = M
        self.N = N
        self.d = d
        self.k = k
        self.chromosome_length = M * N
        
        # GA parameters
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_size = elite_size
        
        # Statistics
        self.best_fitness_history = []
        self.avg_fitness_history = []
        
    def initialize_population(self) -> np.ndarray:
        """
        Create initial random population
        
        Returns:
            population: 2D array of shape (population_size, chromosome_length)
        """
        return np.random.randint(0, 2, size=(self.population_size, self.chromosome_length))
    
    def chromosome_to_matrix(self, chromosome: np.ndarray) -> np.ndarray:
        """
        Convert flat chromosome to M×N matrix
        
        Args:
            chromosome: 1D binary array of length M*N
            
        Returns:
            matrix: 2D array of shape (M, N)
        """
        return chromosome.reshape(self.M, self.N)
    
    def matrix_to_chromosome(self, matrix: np.ndarray) -> np.ndarray:
        """
        Convert M×N matrix to flat chromosome
        
        Args:
            matrix: 2D array of shape (M, N)
            
        Returns:
            chromosome: 1D binary array of length M*N
        """
        return matrix.flatten()
    
    def tournament_selection(
        self,
        population: np.ndarray,
        fitness_values: np.ndarray,
        tournament_size: int = 3
    ) -> np.ndarray:
        """
        Select parent using tournament selection
        
        Args:
            population: Current population
            fitness_values: Fitness of each individual
            tournament_size: Number of individuals in tournament
            
        Returns:
            Selected parent chromosome
        """
        indices = np.random.choice(len(population), tournament_size, replace=False)
        tournament_fitness = fitness_values[indices]
        winner_idx = indices[np.argmin(tournament_fitness)]  # Minimize fitness
        return population[winner_idx].copy()
    
    def crossover(
        self,
        parent1: np.ndarray,
        parent2: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Perform one-point crossover
        
        Args:
            parent1, parent2: Parent chromosomes
            
        Returns:
            Two offspring chromosomes
        """
        if np.random.random() < self.crossover_rate:
            point = np.random.randint(1, self.chromosome_length)
            child1 = np.concatenate([parent1[:point], parent2[point:]])
            child2 = np.concatenate([parent2[:point], parent1[point:]])
            return child1, child2
        return parent1.copy(), parent2.copy()
    
    def mutate(self, chromosome: np.ndarray) -> np.ndarray:
        """
        Perform bit-flip mutation
        
        Args:
            chromosome: Chromosome to mutate
            
        Returns:
            Mutated chromosome
        """
        mask = np.random.random(self.chromosome_length) < self.mutation_rate
        chromosome[mask] = 1 - chromosome[mask]
        return chromosome
    
    def run(
        self,
        generations: int = 100,
        target_fmax: Optional[float] = None,
        verbose: bool = True
    ) -> Tuple[np.ndarray, float, dict]:
        """
        Run the Genetic Algorithm optimization
        
        Args:
            generations: Number of generations to evolve
            target_fmax: Target f_max value (if None, minimize f_max)
            verbose: Print progress information
            
        Returns:
            best_matrix: Optimized φ_mn matrix
            best_fmax: Best fitness value achieved
            history: Dictionary containing evolution statistics
        """
        # TO BE IMPLEMENTED IN PHASE 4
        # This is a placeholder that will be completed after
        # implementing the array factor computation (Phase 2)
        # and continuous search (Phase 3)
        
        raise NotImplementedError(
            "GA.run() will be implemented in Phase 4.\n"
            "Prerequisites: Array Factor computation (Phase 2) and "
            "Continuous Search (Phase 3) must be completed first."
        )
    
    def __repr__(self) -> str:
        """String representation of GA configuration"""
        return (
            f"AntennaGeneticAlgorithm(\n"
            f"  Array: {self.M}×{self.N}\n"
            f"  Population: {self.population_size}\n"
            f"  Mutation rate: {self.mutation_rate}\n"
            f"  Crossover rate: {self.crossover_rate}\n"
            f"  Elite size: {self.elite_size}\n"
            f")"
        )


# Quick test of GA class structure
if __name__ == "__main__":
    print("Testing Genetic Algorithm class structure...\n")
    
    ga = AntennaGeneticAlgorithm(M=8, N=8)
    print(ga)
    
    # Test population initialization
    pop = ga.initialize_population()
    print(f"\n✓ Population shape: {pop.shape}")
    print(f"✓ Sample chromosome: {pop[0][:10]}... (first 10 genes)")
    
    # Test chromosome/matrix conversion
    test_chromosome = pop[0]
    test_matrix = ga.chromosome_to_matrix(test_chromosome)
    test_back = ga.matrix_to_chromosome(test_matrix)
    print(f"\n✓ Matrix shape: {test_matrix.shape}")
    print(f"✓ Conversion check: {np.array_equal(test_chromosome, test_back)}")
    
    # Test genetic operators
    parent1, parent2 = pop[0], pop[1]
    child1, child2 = ga.crossover(parent1, parent2)
    print(f"\n✓ Crossover produced children: {child1.shape}")
    
    mutated = ga.mutate(pop[0].copy())
    differences = np.sum(mutated != pop[0])
    print(f"✓ Mutation flipped {differences} bits")
    
    print("\n[SUCCESS] GA class structure validated!")
