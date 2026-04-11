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
from utils import find_max_angles


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
    
    def fitness_function(self, chromosome: np.ndarray) -> float:
        """
        Calculate fitness for a chromosome
        
        Fitness = f_max value (lower is better, so we minimize)
        The Array Factor maximum is found using continuous search (Phase 3)
        
        Args:
            chromosome: Binary chromosome (64 bits for 8×8)
            
        Returns:
            f_max value (fitness to be minimized)
        """
        # Convert chromosome to matrix
        matrix = self.chromosome_to_matrix(chromosome)
        
        # Find f_max using continuous search (Phase 3)
        _, _, f_max = find_max_angles(matrix, self.d, self.k)
        
        return f_max
    
    def run(
        self,
        generations: int = 100,
        target_fmax: Optional[float] = None,
        verbose: bool = True
    ) -> Tuple[np.ndarray, float, dict]:
        """
        Run the Genetic Algorithm optimization
        
        Main loop: Selection → Crossover → Mutation → Evaluation → Elitism
        
        Args:
            generations: Number of generations to evolve
            target_fmax: Target f_max value (if None, minimize f_max)
            verbose: Print progress information
            
        Returns:
            best_matrix: Optimized φ_mn matrix
            best_fmax: Best f_max value achieved
            history: Dictionary containing best_fitness_history and avg_fitness_history
        """
        if verbose:
            print(f"\nStarting GA optimization...")
            print(f"  Population: {self.population_size}")
            print(f"  Generations: {generations}")
            print(f"  Target f_max: {target_fmax if target_fmax else 'minimize'}")
        
        # Initialize population
        population = self.initialize_population()
        
        # Evaluate initial population
        fitness_values = np.array([
            self.fitness_function(chromosome) for chromosome in population
        ])
        
        # Tracking history
        best_fitness_history = []
        avg_fitness_history = []
        best_chromosome = population[np.argmin(fitness_values)].copy()
        best_fitness = np.min(fitness_values)
        
        if verbose:
            print(f"  Initial best f_max: {best_fitness:.6f}")
        
        # Main GA loop
        for generation in range(generations):
            # Selection and reproduction
            offspring = []
            for _ in range(self.population_size // 2):
                # Tournament selection for 2 parents
                parent1 = self.tournament_selection(population, fitness_values)
                parent2 = self.tournament_selection(population, fitness_values)
                
                # Crossover
                child1, child2 = self.crossover(parent1, parent2)
                
                # Mutation
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                
                offspring.extend([child1, child2])
            
            # Ensure we have exactly population_size individuals
            offspring = offspring[:self.population_size]
            
            # Evaluate offspring
            offspring_fitness = np.array([
                self.fitness_function(chromosome) for chromosome in offspring
            ])
            
            # Elitism: Keep best individuals from current + offspring population
            combined_population = np.vstack([population, offspring])
            combined_fitness = np.concatenate([fitness_values, offspring_fitness])
            
            # Sort by fitness and keep top population_size
            elite_indices = np.argsort(combined_fitness)[:self.population_size]
            population = combined_population[elite_indices]
            fitness_values = combined_fitness[elite_indices]
            
            # Track best solution
            current_best_idx = np.argmin(fitness_values)
            current_best_fitness = fitness_values[current_best_idx]
            
            if current_best_fitness < best_fitness:
                best_fitness = current_best_fitness
                best_chromosome = population[current_best_idx].copy()
            
            # Record history
            best_fitness_history.append(best_fitness)
            avg_fitness_history.append(np.mean(fitness_values))
            
            # Verbose output
            if verbose and (generation + 1) % max(1, generations // 10) == 0:
                print(f"  Gen {generation + 1:3d}/{generations}: "
                      f"best_f_max={best_fitness:.6f}, "
                      f"avg_f_max={np.mean(fitness_values):.6f}")
            
            # Check termination criteria
            if target_fmax is not None and best_fitness <= target_fmax:
                if verbose:
                    print(f"  ✓ Target f_max reached: {best_fitness:.6f}")
                break
        
        # Convert best chromosome to matrix
        best_matrix = self.chromosome_to_matrix(best_chromosome)
        
        # Prepare history dictionary
        history = {
            'best_fitness': best_fitness_history,
            'avg_fitness': avg_fitness_history,
            'generations_run': generation + 1,
            'target_fmax': target_fmax
        }
        
        if verbose:
            print(f"\n✓ GA optimization complete!")
            print(f"  Final best f_max: {best_fitness:.6f}")
            print(f"  Generations run: {generation + 1}")
            print(f"  Improvement: {((avg_fitness_history[0] - best_fitness) / avg_fitness_history[0] * 100):.2f}%")
        
        return best_matrix, best_fitness, history
    
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
