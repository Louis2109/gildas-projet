#!/usr/bin/env python3
"""
Utility Functions for Antenna Array Optimization
=================================================

Contains helper functions for:
- Array Factor computation
- Angle optimization (continuous search)
- Visualization (2D and 3D plots)
- Results saving and loading
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Optional
import json
import os


# ============================================================================
# ARRAY FACTOR COMPUTATION (To be implemented in Phase 2)
# ============================================================================

def compute_array_factor(
    theta: float,
    phi: float,
    phi_mn_matrix: np.ndarray,
    d: float = 0.5,
    k: float = 2 * np.pi
) -> complex:
    """
    Compute the Array Factor f(θ, φ) for given angles and phase matrix
    
    Formula:
    f(θ, φ) = Σ(m=1 to M) Σ(n=1 to N) 
              exp(j(m-1)(kd·sin(θ)·sin(φ))) × 
              exp(j(m-1)(kd·sin(θ)·cos(φ))) × 
              exp(jφ_mn)
    
    where φ_mn = 0 if matrix[m,n]=0, π if matrix[m,n]=1
    
    Args:
        theta: Elevation angle [0, π] (radians)
        phi: Azimuth angle [0, 2π] (radians)
        phi_mn_matrix: M×N binary matrix
        d: Element spacing
        k: Wave number
        
    Returns:
        Complex value of array factor
    """
    # TO BE IMPLEMENTED IN PHASE 2
    raise NotImplementedError("Will be implemented in Phase 2")


def evaluate_array_factor_grid(
    phi_mn_matrix: np.ndarray,
    theta_range: np.ndarray,
    phi_range: np.ndarray,
    d: float = 0.5,
    k: float = 2 * np.pi
) -> Tuple[np.ndarray, float, Tuple[float, float]]:
    """
    Evaluate Array Factor on a grid of angles
    
    Args:
        phi_mn_matrix: M×N binary phase matrix
        theta_range: Array of theta values
        phi_range: Array of phi values
        d, k: Physical parameters
        
    Returns:
        af_magnitude: 2D grid of |f(θ, φ)|
        f_max: Maximum value of |f|
        max_angles: (theta_max, phi_max) where maximum occurs
    """
    # TO BE IMPLEMENTED IN PHASE 2
    raise NotImplementedError("Will be implemented in Phase 2")


# ============================================================================
# CONTINUOUS SEARCH (To be implemented in Phase 3)
# ============================================================================

def find_max_angles(
    phi_mn_matrix: np.ndarray,
    d: float = 0.5,
    k: float = 2 * np.pi
) -> Tuple[float, float, float]:
    """
    Find angles (θ, φ) where |f| is maximum using continuous optimization
    
    This implements the "Continuous Search" step from the project diagram.
    
    Args:
        phi_mn_matrix: M×N binary phase matrix
        d, k: Physical parameters
        
    Returns:
        theta_max: Optimal theta angle
        phi_max: Optimal phi angle
        f_max: Maximum value |f(theta_max, phi_max)|
    """
    # TO BE IMPLEMENTED IN PHASE 3
    raise NotImplementedError("Will be implemented in Phase 3")


def evaluate_array_factor_max(
    phi_mn_matrix: np.ndarray,
    d: float = 0.5,
    k: float = 2 * np.pi
) -> float:
    """
    Convenience function to get f_max directly
    
    Args:
        phi_mn_matrix: M×N binary phase matrix
        d, k: Physical parameters
        
    Returns:
        f_max: Maximum value of |f(θ, φ)|
    """
    _, _, f_max = find_max_angles(phi_mn_matrix, d, k)
    return f_max


# ============================================================================
# VISUALIZATION (To be implemented in Phase 5)
# ============================================================================

def plot_array_factor_2d(
    phi_mn_matrix: np.ndarray,
    d: float = 0.5,
    k: float = 2 * np.pi,
    save_path: Optional[str] = None
) -> None:
    """
    Plot 2D cuts of Array Factor (θ or φ fixed)
    
    Args:
        phi_mn_matrix: M×N binary phase matrix
        d, k: Physical parameters
        save_path: Path to save figure (optional)
    """
    # TO BE IMPLEMENTED IN PHASE 5
    raise NotImplementedError("Will be implemented in Phase 5")


def plot_array_factor_3d(
    phi_mn_matrix: np.ndarray,
    d: float = 0.5,
    k: float = 2 * np.pi,
    save_path: Optional[str] = None
) -> None:
    """
    Plot 3D spherical projection of Array Factor
    
    Args:
        phi_mn_matrix: M×N binary phase matrix
        d, k: Physical parameters
        save_path: Path to save figure (optional)
    """
    # TO BE IMPLEMENTED IN PHASE 5
    raise NotImplementedError("Will be implemented in Phase 5")


def plot_comparison(
    initial_matrix: np.ndarray,
    optimized_matrix: np.ndarray,
    d: float = 0.5,
    k: float = 2 * np.pi,
    save_path: Optional[str] = None
) -> None:
    """
    Plot side-by-side comparison of initial vs optimized solutions
    
    Args:
        initial_matrix: Initial φ_mn matrix
        optimized_matrix: Optimized φ_mn matrix
        d, k: Physical parameters
        save_path: Path to save figure (optional)
    """
    # TO BE IMPLEMENTED IN PHASE 5
    raise NotImplementedError("Will be implemented in Phase 5")


def plot_convergence(
    best_fitness_history: list,
    avg_fitness_history: list,
    save_path: Optional[str] = None
) -> None:
    """
    Plot GA convergence (fitness evolution over generations)
    
    Args:
        best_fitness_history: Best fitness per generation
        avg_fitness_history: Average fitness per generation
        save_path: Path to save figure (optional)
    """
    # TO BE IMPLEMENTED IN PHASE 5
    raise NotImplementedError("Will be implemented in Phase 5")


# ============================================================================
# DATA MANAGEMENT
# ============================================================================

def save_results(
    matrix: np.ndarray,
    f_max: float,
    history: dict,
    filename: str = "optimization_results"
) -> None:
    """
    Save optimization results to files
    
    Args:
        matrix: Optimized φ_mn matrix
        f_max: Optimal f_max value
        history: GA evolution history
        filename: Base filename (without extension)
    """
    results_dir = "results/data"
    os.makedirs(results_dir, exist_ok=True)
    
    # Save matrix as CSV
    matrix_path = os.path.join(results_dir, f"{filename}_matrix.csv")
    np.savetxt(matrix_path, matrix, fmt='%d', delimiter=',')
    
    # Save metadata and history as JSON
    metadata = {
        'f_max': float(f_max),
        'matrix_shape': matrix.shape,
        'best_fitness_history': [float(x) for x in history.get('best_fitness', [])],
        'avg_fitness_history': [float(x) for x in history.get('avg_fitness', [])],
    }
    
    json_path = os.path.join(results_dir, f"{filename}_metadata.json")
    with open(json_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✓ Results saved to {results_dir}/")
    print(f"  - {filename}_matrix.csv")
    print(f"  - {filename}_metadata.json")


def load_results(filename: str = "optimization_results") -> Tuple[np.ndarray, float, dict]:
    """
    Load previously saved optimization results
    
    Args:
        filename: Base filename (without extension)
        
    Returns:
        matrix: φ_mn matrix
        f_max: Optimal f_max value
        history: GA evolution history
    """
    results_dir = "results/data"
    
    # Load matrix
    matrix_path = os.path.join(results_dir, f"{filename}_matrix.csv")
    matrix = np.loadtxt(matrix_path, delimiter=',', dtype=int)
    
    # Load metadata
    json_path = os.path.join(results_dir, f"{filename}_metadata.json")
    with open(json_path, 'r') as f:
        metadata = json.load(f)
    
    f_max = metadata['f_max']
    history = {
        'best_fitness': metadata.get('best_fitness_history', []),
        'avg_fitness': metadata.get('avg_fitness_history', [])
    }
    
    return matrix, f_max, history


# Quick test of utility functions structure
if __name__ == "__main__":
    print("Testing utility functions structure...\n")
    
    # Test save/load (with dummy data)
    dummy_matrix = np.random.randint(0, 2, (8, 8))
    dummy_fmax = 42.5
    dummy_history = {
        'best_fitness': [100, 80, 60, 40, 42.5],
        'avg_fitness': [150, 120, 90, 70, 65]
    }
    
    print("Testing save_results()...")
    save_results(dummy_matrix, dummy_fmax, dummy_history, "test_phase1")
    
    print("\nTesting load_results()...")
    loaded_matrix, loaded_fmax, loaded_history = load_results("test_phase1")
    
    print(f"\n✓ Matrix loaded: shape {loaded_matrix.shape}")
    print(f"✓ f_max loaded: {loaded_fmax}")
    print(f"✓ History loaded: {len(loaded_history['best_fitness'])} generations")
    print(f"✓ Data integrity: {np.array_equal(dummy_matrix, loaded_matrix)}")
    
    print("\n[SUCCESS] Data management functions validated!")
