#!/usr/bin/env python3
"""
Unit Tests for Antenna Array Optimization
==========================================

Test suite for validating all components of the optimization system.
"""

import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from genetic_algorithm import AntennaGeneticAlgorithm
from utils import save_results, load_results


# ============================================================================
# TEST UTILITIES
# ============================================================================

def run_test(test_name: str, test_func) -> bool:
    """Run a single test and report result"""
    try:
        test_func()
        print(f"✓ {test_name}")
        return True
    except Exception as e:
        print(f"✗ {test_name}")
        print(f"  Error: {e}")
        return False


# ============================================================================
# PHASE 1 TESTS: Project Structure and GA Class
# ============================================================================

def test_ga_initialization():
    """Test GA class can be instantiated with correct parameters"""
    ga = AntennaGeneticAlgorithm(M=8, N=8, d=0.5, k=2*np.pi)
    assert ga.M == 8
    assert ga.N == 8
    assert ga.chromosome_length == 64
    assert ga.population_size == 50


def test_population_initialization():
    """Test population is correctly initialized as binary matrix"""
    ga = AntennaGeneticAlgorithm(M=4, N=4)
    pop = ga.initialize_population()
    assert pop.shape == (50, 16)  # population_size × chromosome_length
    assert np.all((pop == 0) | (pop == 1))  # Only 0s and 1s


def test_chromosome_matrix_conversion():
    """Test bidirectional conversion between chromosome and matrix"""
    ga = AntennaGeneticAlgorithm(M=4, N=4)
    
    # Create test chromosome
    chromosome = np.array([1,0,1,0, 0,1,0,1, 1,1,0,0, 0,0,1,1])
    
    # Convert to matrix and back
    matrix = ga.chromosome_to_matrix(chromosome)
    chromosome_back = ga.matrix_to_chromosome(matrix)
    
    assert matrix.shape == (4, 4)
    assert np.array_equal(chromosome, chromosome_back)


def test_tournament_selection():
    """Test tournament selection chooses from population"""
    ga = AntennaGeneticAlgorithm(M=4, N=4, population_size=10)
    pop = ga.initialize_population()
    fitness = np.random.rand(10) * 100  # Random fitness values
    
    selected = ga.tournament_selection(pop, fitness, tournament_size=3)
    
    assert selected.shape == (16,)  # Correct chromosome length
    assert np.all((selected == 0) | (selected == 1))


def test_crossover():
    """Test crossover produces valid offspring"""
    ga = AntennaGeneticAlgorithm(M=4, N=4)
    
    parent1 = np.ones(16, dtype=int)
    parent2 = np.zeros(16, dtype=int)
    
    child1, child2 = ga.crossover(parent1, parent2)
    
    assert child1.shape == (16,)
    assert child2.shape == (16,)
    assert np.all((child1 == 0) | (child1 == 1))
    assert np.all((child2 == 0) | (child2 == 1))


def test_mutation():
    """Test mutation flips bits with correct probability"""
    ga = AntennaGeneticAlgorithm(M=8, N=8, mutation_rate=0.1)
    
    original = np.zeros(64, dtype=int)
    mutated = ga.mutate(original.copy())
    
    # With mutation_rate=0.1, expect ~6.4 flips (64 × 0.1)
    # Allow range 0-20 flips due to randomness
    num_flips = np.sum(mutated != original)
    assert 0 <= num_flips <= 20


def test_data_save_load():
    """Test saving and loading results"""
    test_matrix = np.random.randint(0, 2, (8, 8))
    test_fmax = 42.5
    test_history = {
        'best_fitness': [100, 90, 80],
        'avg_fitness': [120, 110, 100]
    }
    
    # Save
    save_results(test_matrix, test_fmax, test_history, "test_save_load")
    
    # Load
    loaded_matrix, loaded_fmax, loaded_history = load_results("test_save_load")
    
    assert np.array_equal(test_matrix, loaded_matrix)
    assert loaded_fmax == test_fmax
    assert len(loaded_history['best_fitness']) == 3


# ============================================================================
# PHASE 2 TESTS: Array Factor Computation (To be added)
# ============================================================================

def test_array_factor_computation():
    """Test compute_array_factor() gives correct values"""
    # Will be implemented in Phase 2
    pass


def test_array_factor_grid():
    """Test evaluate_array_factor_grid() returns correct shape"""
    # Will be implemented in Phase 2
    pass


# ============================================================================
# PHASE 3 TESTS: Continuous Search (To be added)
# ============================================================================

def test_find_max_angles():
    """Test find_max_angles() finds correct maximum"""
    # Will be implemented in Phase 3
    pass


# ============================================================================
# PHASE 4 TESTS: GA Optimization (To be added)
# ============================================================================

def test_ga_run():
    """Test GA.run() converges to better solutions"""
    # Will be implemented in Phase 4
    pass


# ============================================================================
# TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run all available tests and report results"""
    print("="*60)
    print("  ANTENNA OPTIMIZER - TEST SUITE")
    print("="*60)
    
    phase1_tests = [
        ("GA Initialization", test_ga_initialization),
        ("Population Initialization", test_population_initialization),
        ("Chromosome ↔ Matrix Conversion", test_chromosome_matrix_conversion),
        ("Tournament Selection", test_tournament_selection),
        ("Crossover Operator", test_crossover),
        ("Mutation Operator", test_mutation),
        ("Data Save/Load", test_data_save_load),
    ]
    
    print("\n[PHASE 1 TESTS]")
    results = []
    for test_name, test_func in phase1_tests:
        results.append(run_test(test_name, test_func))
    
    # Summary
    passed = sum(results)
    total = len(results)
    print("\n" + "="*60)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ ALL TESTS PASSED!")
        return 0
    else:
        print(f"✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
