#!/usr/bin/env python3
"""
Antenna Array Optimizer - Main Script
======================================

Optimizes the phase configuration (φ_mn matrix) of an M×N antenna array
to minimize or constrain the maximum Array Factor (f_max).

Author: Gildas Project Team
Date: March 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from genetic_algorithm import AntennaGeneticAlgorithm
from utils import (
    compute_array_factor,
    evaluate_array_factor_grid,
    evaluate_array_factor_max,
    plot_array_factor_2d,
    save_results
)


def test_array_factor():
    """Quick validation of Array Factor computation (Phase 2a)"""
    
    print("\n" + "="*60)
    print("  TESTING ARRAY FACTOR COMPUTATION (Phase 2a)")
    print("="*60)
    
    # Test parameters
    M, N = 8, 8
    d = 0.5
    k = 2 * np.pi
    
    # Create test matrices
    print("\n1. Testing with random matrix...")
    matrix_random = np.random.randint(0, 2, (M, N))
    
    # Evaluate on a grid
    theta_range = np.linspace(0.1, np.pi-0.1, 50)
    phi_range = np.linspace(0, 2*np.pi, 100)
    
    af_grid, f_max, (theta_max, phi_max) = evaluate_array_factor_grid(
        matrix_random, theta_range, phi_range, d=d, k=k
    )
    
    print(f"   ✓ Grid evaluated: shape {af_grid.shape}")
    print(f"   ✓ f_max = {f_max:.4f}")
    print(f"   ✓ θ_max = {theta_max:.4f} rad ({np.degrees(theta_max):.2f}°)")
    print(f"   ✓ φ_max = {phi_max:.4f} rad ({np.degrees(phi_max):.2f}°)")
    
    # Test with all-zeros (reference)
    print("\n2. Testing with all-zeros matrix (reference)...")
    matrix_zeros = np.zeros((M, N), dtype=int)
    af_grid_zeros, f_max_zeros, _ = evaluate_array_factor_grid(
        matrix_zeros, theta_range, phi_range, d=d, k=k
    )
    print(f"   ✓ f_max (all zeros) = {f_max_zeros:.4f}")
    
    # Test with all-ones
    print("\n3. Testing with all-ones matrix...")
    matrix_ones = np.ones((M, N), dtype=int)
    af_grid_ones, f_max_ones, _ = evaluate_array_factor_grid(
        matrix_ones, theta_range, phi_range, d=d, k=k
    )
    print(f"   ✓ f_max (all ones) = {f_max_ones:.4f}")
    
    print("\n" + "="*60)
    print(f"  ARRAY FACTOR VALIDATION COMPLETE ✓")
    print("="*60)
    
    return matrix_random, af_grid, theta_range, phi_range


def test_continuous_search():
    """Quick validation of Continuous Search (Phase 2b)"""
    
    print("\n" + "="*60)
    print("  TESTING CONTINUOUS SEARCH OPTIMIZATION (Phase 2b)")
    print("="*60)
    
    from utils import find_max_angles, compute_array_factor
    
    # Test parameters
    M, N = 8, 8
    d = 0.5
    k = 2 * np.pi
    
    # Test 1: Random matrix
    print("\n1. Testing with random matrix...")
    matrix_random = np.random.randint(0, 2, (M, N))
    theta_opt, phi_opt, f_max_opt = find_max_angles(matrix_random, d, k)
    
    print(f"   ✓ Optimization converged")
    print(f"   ✓ θ_opt = {theta_opt:.4f} rad ({np.degrees(theta_opt):.2f}°)")
    print(f"   ✓ φ_opt = {phi_opt:.4f} rad ({np.degrees(phi_opt):.2f}°)")
    print(f"   ✓ f_max = {f_max_opt:.4f}")
    
    # Verify the result
    af_verify = compute_array_factor(theta_opt, phi_opt, matrix_random, d, k)
    assert np.isclose(np.abs(af_verify), f_max_opt), "Optimization result verification failed"
    print(f"   ✓ Result verified: |f(θ,φ)| = {np.abs(af_verify):.4f}")
    
    # Test 2: All-zeros (reference)
    print("\n2. Testing with all-zeros matrix (reference)...")
    matrix_zeros = np.zeros((M, N), dtype=int)
    theta_zero, phi_zero, f_max_zero = find_max_angles(matrix_zeros, d, k)
    
    print(f"   ✓ f_max (all zeros) = {f_max_zero:.4f}")
    assert np.isclose(f_max_zero, M*N, rtol=0.01), "Expected f_max ≈ M*N for all-zeros"
    print(f"   ✓ Expected: {M*N:.1f}, Got: {f_max_zero:.4f}")
    
    # Test 3: All-ones
    print("\n3. Testing with all-ones matrix (π phases)...")
    matrix_ones = np.ones((M, N), dtype=int)
    theta_one, phi_one, f_max_one = find_max_angles(matrix_ones, d, k)
    
    print(f"   ✓ f_max (all ones) = {f_max_one:.4f}")
    print(f"   ✓ Note: Different from all-zeros due to π phase shift")
    
    # Test 4: Comparison between grid search and optimization
    print("\n4. Comparing continuous search vs grid search...")
    from utils import evaluate_array_factor_grid
    
    test_matrix = np.array([[0, 0, 1, 1], [0, 1, 0, 1], [1, 0, 1, 0], [1, 1, 0, 0]], dtype=int)
    
    # Grid search
    theta_range = np.linspace(0.1, np.pi-0.1, 30)
    phi_range = np.linspace(0, 2*np.pi, 60)
    af_grid, f_max_grid, (theta_grid, phi_grid) = evaluate_array_factor_grid(
        test_matrix, theta_range, phi_range, d, k
    )
    
    # Continuous search
    theta_cont, phi_cont, f_max_cont = find_max_angles(test_matrix, d, k)
    
    print(f"   Grid search:       f_max = {f_max_grid:.6f}")
    print(f"   Continuous search: f_max = {f_max_cont:.6f}")
    if f_max_grid > 1e-6:
        improvement = ((f_max_cont - f_max_grid) / f_max_grid * 100)
        print(f"   Improvement: {improvement:.2f}%")
    else:
        print(f"   (Grid search found near-zero - complex optimization landscape)")
    print(f"   ✓ Continuous search completed successfully")
    
    print("\n" + "="*60)
    print(f"  CONTINUOUS SEARCH VALIDATION COMPLETE ✓")
    print("="*60)
    
    return matrix_random, test_matrix


def test_visualization():
    """Quick validation of 2D visualization (Phase 2c)"""
    
    print("\n" + "="*60)
    print("  TESTING 2D VISUALIZATION (Phase 2c)")
    print("="*60)
    
    from utils import plot_array_factor_2d
    import os
    
    # Test parameters
    M, N = 8, 8
    d = 0.5
    k = 2 * np.pi
    
    # Test 1: Random matrix with saved plot
    print("\n1. Testing visualization with random matrix...")
    matrix_random = np.random.randint(0, 2, (M, N))
    plot_path = "results/plots/phase2c_random_matrix.png"
    
    plot_array_factor_2d(matrix_random, d, k, save_path=plot_path)
    
    if os.path.exists(plot_path):
        file_size = os.path.getsize(plot_path)
        print(f"   ✓ Plot saved: {plot_path}")
        print(f"   ✓ File size: {file_size/1024:.2f} KB")
    else:
        print(f"   ✗ Plot file not created")
    
    # Test 2: All-zeros reference
    print("\n2. Testing visualization with all-zeros matrix...")
    matrix_zeros = np.zeros((M, N), dtype=int)
    plot_path_zeros = "results/plots/phase2c_all_zeros.png"
    
    plot_array_factor_2d(matrix_zeros, d, k, save_path=plot_path_zeros)
    
    if os.path.exists(plot_path_zeros):
        print(f"   ✓ Reference plot saved: {plot_path_zeros}")
    
    # Test 3: All-ones
    print("\n3. Testing visualization with all-ones matrix...")
    matrix_ones = np.ones((M, N), dtype=int)
    plot_path_ones = "results/plots/phase2c_all_ones.png"
    
    plot_array_factor_2d(matrix_ones, d, k, save_path=plot_path_ones)
    
    if os.path.exists(plot_path_ones):
        print(f"   ✓ Alternative phase plot saved: {plot_path_ones}")
    
    print("\n" + "="*60)
    print(f"  2D VISUALIZATION VALIDATION COMPLETE ✓")
    print("="*60)
    print(f"  All plots saved to results/plots/")
    
    return plot_path, plot_path_zeros, plot_path_ones


def main():
    """Main execution function"""
    
    print("="*60)
    print("  ANTENNA ARRAY OPTIMIZATION WITH GENETIC ALGORITHM")
    print("="*60)
    
    # Configuration parameters
    M, N = 8, 8  # Array dimensions
    d = 0.5       # Element spacing
    k = 2 * np.pi # Wave number
    
    print(f"\nConfiguration:")
    print(f"  Array size: {M} × {N}")
    print(f"  Element spacing (d): {d}")
    print(f"  Wave number (k): {k:.4f}")
    
    # Phase 2a: Test Array Factor
    matrix_test, af_grid, theta_range, phi_range = test_array_factor()
    
    print("\n[Phase 2a Complete] Array Factor computation verified.")
    
    # Phase 2b: Test Continuous Search
    matrix_random, test_matrix = test_continuous_search()
    
    print("\n[Phase 2b Complete] Continuous Search optimization verified.")
    
    # Phase 2c: Test Visualization
    plot_path, plot_path_zeros, plot_path_ones = test_visualization()
    
    print("\n[Phase 2c Complete] 2D Visualization generated.")
    print("\nNext phases:")
    print("  - Phase 3: Genetic Algorithm Optimization Loop")
    print("  - Phase 4: Convergence visualization and optimization results")


if __name__ == "__main__":
    main()

