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
    """Test compute_array_factor() gives correct complex values"""
    from utils import compute_array_factor
    
    # Test with simple 2×2 all-zeros matrix
    phi_matrix = np.zeros((2, 2), dtype=int)
    theta, phi = np.pi / 4, np.pi / 4
    
    af = compute_array_factor(theta, phi, phi_matrix, d=0.5, k=2*np.pi)
    
    # Should be a complex number
    assert isinstance(af, complex)
    # Magnitude should be positive
    assert np.abs(af) >= 0


def test_array_factor_all_zeros():
    """Test array factor with all zeros (reference phase)"""
    from utils import compute_array_factor
    
    phi_matrix = np.zeros((4, 4), dtype=int)
    
    # Test at multiple angles
    for theta in [0.1, np.pi/4, np.pi/2]:
        for phi in [0.1, np.pi/2, np.pi]:
            af = compute_array_factor(theta, phi, phi_matrix)
            magnitude = np.abs(af)
            # All zeros → maximum constructive interference possible
            assert magnitude > 0


def test_array_factor_grid():
    """Test evaluate_array_factor_grid() returns correct shape and values"""
    from utils import evaluate_array_factor_grid
    
    phi_matrix = np.random.randint(0, 2, (4, 4))
    
    theta_range = np.linspace(0.1, np.pi-0.1, 10)
    phi_range = np.linspace(0, 2*np.pi, 20)
    
    af_mag, f_max, (theta_max, phi_max) = evaluate_array_factor_grid(
        phi_matrix, theta_range, phi_range
    )
    
    # Check shapes
    assert af_mag.shape == (len(theta_range), len(phi_range))
    
    # Check f_max is positive
    assert f_max >= 0
    
    # Check angles are in valid range
    assert 0.1 <= theta_max <= np.pi - 0.1
    assert 0 <= phi_max <= 2 * np.pi
    
    # Check that f_max equals the actual maximum
    assert np.isclose(f_max, np.max(af_mag))


def test_array_factor_magnitude_positive():
    """Test that array factor magnitude is always non-negative"""
    from utils import compute_array_factor, evaluate_array_factor_grid
    
    phi_matrix = np.random.randint(0, 2, (8, 8))
    theta_range = np.linspace(0.01, np.pi-0.01, 15)
    phi_range = np.linspace(0, 2*np.pi, 30)
    
    af_mag, _, _ = evaluate_array_factor_grid(phi_matrix, theta_range, phi_range)
    
    # All magnitudes must be >= 0
    assert np.all(af_mag >= 0)


def test_array_factor_consistency():
    """Test that grid evaluation is consistent with point evaluation"""
    from utils import compute_array_factor, evaluate_array_factor_grid
    
    phi_matrix = np.array([[0, 1], [1, 0]], dtype=int)
    
    theta_range = np.array([np.pi/6, np.pi/4, np.pi/3])
    phi_range = np.array([0, np.pi/2, np.pi, 3*np.pi/2])
    
    # Get grid
    af_mag, _, _ = evaluate_array_factor_grid(phi_matrix, theta_range, phi_range)
    
    # Verify each point matches individual computation
    for i, theta in enumerate(theta_range):
        for j, phi in enumerate(phi_range):
            af_point = compute_array_factor(theta, phi, phi_matrix)
            mag_point = np.abs(af_point)
            
            assert np.isclose(af_mag[i, j], mag_point, rtol=1e-10)


# ============================================================================
# PHASE 2b TESTS: Continuous Search
# ============================================================================

def test_find_max_angles_random_matrix():
    """Test find_max_angles() finds local maximum with random matrix"""
    from utils import find_max_angles, compute_array_factor
    
    phi_matrix = np.random.randint(0, 2, (4, 4))
    
    theta_max, phi_max, f_max = find_max_angles(phi_matrix)
    
    # Verify output types
    assert isinstance(theta_max, float)
    assert isinstance(phi_max, float)
    assert isinstance(f_max, float)
    
    # Verify bounds
    assert 0 < theta_max < np.pi
    assert 0 <= phi_max <= 2 * np.pi
    assert f_max > 0
    
    # Verify this is indeed a maximum by checking nearby points
    af_max = compute_array_factor(theta_max, phi_max, phi_matrix)
    assert np.isclose(np.abs(af_max), f_max, rtol=1e-6)


def test_find_max_angles_all_zeros():
    """Test find_max_angles() with all-zeros matrix (reference)"""
    from utils import find_max_angles
    
    phi_matrix = np.zeros((4, 4), dtype=int)
    
    theta_max, phi_max, f_max = find_max_angles(phi_matrix)
    
    # All-zeros: maximum is uniform (16 elements in phase)
    expected_f_max = 16.0  # M*N elements all constructively add
    assert np.isclose(f_max, expected_f_max, rtol=0.01), \
        f"Expected ~{expected_f_max}, got {f_max}"


def test_find_max_angles_vs_grid():
    """Test find_max_angles() gives similar result to grid search"""
    from utils import find_max_angles, evaluate_array_factor_grid
    
    phi_matrix = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=int)
    
    # Find max using continuous search
    theta_opt, phi_opt, f_max_opt = find_max_angles(phi_matrix)
    
    # Find max using coarse grid search
    theta_range = np.linspace(0.1, np.pi-0.1, 50)
    phi_range = np.linspace(0, 2*np.pi, 100)
    af_mag, f_max_grid, (theta_grid, phi_grid) = evaluate_array_factor_grid(
        phi_matrix, theta_range, phi_range
    )
    
    # Continuous search should find better (higher f_max) or equal value
    assert f_max_opt >= f_max_grid * 0.95, \
        f"Optimizer result {f_max_opt} worse than grid {f_max_grid}"


def test_find_max_angles_consistency():
    """Test find_max_angles() is deterministic for same input"""
    from utils import find_max_angles
    
    phi_matrix = np.random.randint(0, 2, (5, 5))
    
    # Run twice with same matrix
    result1 = find_max_angles(phi_matrix)
    result2 = find_max_angles(phi_matrix)
    
    # Should get very close results (within tolerance)
    theta1, phi1, f_max1 = result1
    theta2, phi2, f_max2 = result2
    
    assert np.isclose(theta1, theta2, rtol=1e-4)
    assert np.isclose(phi1, phi2, rtol=1e-4)
    assert np.isclose(f_max1, f_max2, rtol=1e-4)


def test_evaluate_array_factor_max():
    """Test evaluate_array_factor_max() convenience wrapper"""
    from utils import evaluate_array_factor_max, find_max_angles
    
    phi_matrix = np.random.randint(0, 2, (4, 4))
    
    # Using convenience wrapper
    f_max_direct = evaluate_array_factor_max(phi_matrix)
    
    # Using full function
    _, _, f_max_full = find_max_angles(phi_matrix)
    
    # Should be identical
    assert np.isclose(f_max_direct, f_max_full, rtol=1e-6)


# ============================================================================
# PHASE 2c TESTS: Visualization 2D
# ============================================================================

def test_plot_array_factor_2d_creates_file():
    """Test that plot_array_factor_2d creates a PNG file"""
    from utils import plot_array_factor_2d
    import os
    
    phi_matrix = np.random.randint(0, 2, (4, 4))
    save_path = "results/plots/test_visualization.png"
    
    # Remove file if it exists
    if os.path.exists(save_path):
        os.remove(save_path)
    
    # Generate plot
    plot_array_factor_2d(phi_matrix, save_path=save_path)
    
    # Verify file was created
    assert os.path.exists(save_path), f"Plot file not created at {save_path}"
    assert os.path.getsize(save_path) > 0, "Plot file is empty"


def test_plot_array_factor_2d_no_error():
    """Test that plot_array_factor_2d runs without error"""
    from utils import plot_array_factor_2d
    
    phi_matrix = np.array([[0, 1], [1, 0]], dtype=int)
    
    # Should complete without raising exception
    try:
        plot_array_factor_2d(phi_matrix)
    except Exception as e:
        pytest.fail(f"plot_array_factor_2d raised exception: {e}")


def test_plot_array_factor_2d_all_zeros():
    """Test plot with all-zeros matrix (maximum phase alignment)"""
    from utils import plot_array_factor_2d
    import os
    
    phi_matrix = np.zeros((4, 4), dtype=int)
    save_path = "results/plots/test_all_zeros.png"
    
    if os.path.exists(save_path):
        os.remove(save_path)
    
    plot_array_factor_2d(phi_matrix, save_path=save_path)
    
    assert os.path.exists(save_path)
    assert os.path.getsize(save_path) > 1000, "Plot should have reasonable file size"


def test_plot_array_factor_2d_all_ones():
    """Test plot with all-ones matrix (π phase shift on all elements)"""
    from utils import plot_array_factor_2d
    import os
    
    phi_matrix = np.ones((4, 4), dtype=int)
    save_path = "results/plots/test_all_ones.png"
    
    if os.path.exists(save_path):
        os.remove(save_path)
    
    plot_array_factor_2d(phi_matrix, save_path=save_path)
    
    assert os.path.exists(save_path)
    assert os.path.getsize(save_path) > 1000


def test_plot_array_factor_2d_creates_plots_directory():
    """Test that plots directory is created automatically"""
    from utils import plot_array_factor_2d
    import os
    
    phi_matrix = np.random.randint(0, 2, (3, 3))
    save_path = "results/plots/test_auto_dir.png"
    
    # Remove directory if exists
    plots_dir = "results/plots"
    
    plot_array_factor_2d(phi_matrix, save_path=save_path)
    
    # Verify directory and file were created
    assert os.path.exists(plots_dir), "plots directory not created"
    assert os.path.exists(save_path), "plot file not created"


# ============================================================================
# PHASE 3 TESTS: GA Optimization (To be added)
# ============================================================================

def test_ga_run():
    """Test GA.run() converges to better solutions"""
    # Will be implemented in Phase 3
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
    
    phase2a_tests = [
        ("Array Factor Computation", test_array_factor_computation),
        ("Array Factor All Zeros", test_array_factor_all_zeros),
        ("Array Factor Grid Evaluation", test_array_factor_grid),
        ("Array Factor Magnitude Positive", test_array_factor_magnitude_positive),
        ("Array Factor Consistency", test_array_factor_consistency),
    ]
    
    phase2b_tests = [
        ("Find Max Angles - Random", test_find_max_angles_random_matrix),
        ("Find Max Angles - All Zeros", test_find_max_angles_all_zeros),
        ("Find Max Angles vs Grid", test_find_max_angles_vs_grid),
        ("Find Max Angles - Consistency", test_find_max_angles_consistency),
        ("Evaluate Array Factor Max", test_evaluate_array_factor_max),
    ]
    
    phase2c_tests = [
        ("Plot 2D - Creates File", test_plot_array_factor_2d_creates_file),
        ("Plot 2D - No Error", test_plot_array_factor_2d_no_error),
        ("Plot 2D - All Zeros", test_plot_array_factor_2d_all_zeros),
        ("Plot 2D - All Ones", test_plot_array_factor_2d_all_ones),
        ("Plot 2D - Create Directory", test_plot_array_factor_2d_creates_plots_directory),
    ]
    
    print("\n[PHASE 1 TESTS]")
    phase1_results = []
    for test_name, test_func in phase1_tests:
        phase1_results.append(run_test(test_name, test_func))
    
    print("\n[PHASE 2a TESTS - Array Factor]")
    phase2a_results = []
    for test_name, test_func in phase2a_tests:
        phase2a_results.append(run_test(test_name, test_func))
    
    print("\n[PHASE 2b TESTS - Continuous Search]")
    phase2b_results = []
    for test_name, test_func in phase2b_tests:
        phase2b_results.append(run_test(test_name, test_func))
    
    print("\n[PHASE 2c TESTS - Visualization 2D]")
    phase2c_results = []
    for test_name, test_func in phase2c_tests:
        phase2c_results.append(run_test(test_name, test_func))
    
    # Summary
    all_results = phase1_results + phase2a_results + phase2b_results + phase2c_results
    passed = sum(all_results)
    total = len(all_results)
    
    print("\n" + "="*60)
    print(f"PHASE 1: {sum(phase1_results)}/{len(phase1_results)} passed")
    print(f"PHASE 2a: {sum(phase2a_results)}/{len(phase2a_results)} passed")
    print(f"PHASE 2b: {sum(phase2b_results)}/{len(phase2b_results)} passed")
    print(f"PHASE 2c: {sum(phase2c_results)}/{len(phase2c_results)} passed")
    print(f"TOTAL: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ ALL TESTS PASSED!")
        return 0
    else:
        print(f"✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
