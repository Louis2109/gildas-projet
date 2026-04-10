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
from scipy.optimize import differential_evolution


# ============================================================================
# ARRAY FACTOR COMPUTATION (Phase 2)
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
    M, N = phi_mn_matrix.shape
    
    # Convert phase matrix: 0 → 0, 1 → π
    phi_phase = phi_mn_matrix * np.pi
    
    # Pre-compute common terms
    sin_theta = np.sin(theta)
    sin_phi = np.sin(phi)
    cos_phi = np.cos(phi)
    
    # Exponent coefficients
    coeff1 = k * d * sin_theta * sin_phi
    coeff2 = k * d * sin_theta * cos_phi
    
    # Vectorized computation
    m_indices = np.arange(1, M + 1)[:, np.newaxis]
    n_indices = np.arange(1, N + 1)[np.newaxis, :]
    
    # Phase shifts for each element
    phase_shift1 = (m_indices - 1) * coeff1
    phase_shift2 = (m_indices - 1) * coeff2
    phase_shift_mn = phi_phase
    
    # Total phase for each element
    total_phase = 1j * (phase_shift1 + phase_shift2 + phase_shift_mn)
    
    # Array factor = sum of all exponentials
    af = np.sum(np.exp(total_phase))
    
    return af


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
        theta_range: Array of theta values (radians)
        phi_range: Array of phi values (radians)
        d, k: Physical parameters
        
    Returns:
        af_magnitude: 2D grid of |f(θ, φ)|
        f_max: Maximum value of |f|
        max_angles: (theta_max, phi_max) where maximum occurs
    """
    # Create mesh grid
    THETA, PHI = np.meshgrid(theta_range, phi_range, indexing='ij')
    
    # Compute array factor for each point
    af_grid = np.zeros_like(THETA, dtype=complex)
    for i, theta in enumerate(theta_range):
        for j, phi in enumerate(phi_range):
            af_grid[i, j] = compute_array_factor(theta, phi, phi_mn_matrix, d, k)
    
    # Get magnitude (normalized in dB for visualization)
    af_magnitude = np.abs(af_grid)
    
    # Find maximum
    max_idx = np.unravel_index(np.argmax(af_magnitude), af_magnitude.shape)
    theta_max = theta_range[max_idx[0]]
    phi_max = phi_range[max_idx[1]]
    f_max = af_magnitude[max_idx]
    
    return af_magnitude, f_max, (theta_max, phi_max)


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
    Uses scipy.optimize.differential_evolution for global optimization.
    
    Args:
        phi_mn_matrix: M×N binary phase matrix
        d, k: Physical parameters
        
    Returns:
        theta_max: Optimal theta angle [0, π]
        phi_max: Optimal phi angle [0, 2π]
        f_max: Maximum value |f(theta_max, phi_max)|
    """
    def objective_function(angles):
        """Objective: minimize negative |f| to maximize |f|"""
        theta, phi = angles
        af = compute_array_factor(theta, phi, phi_mn_matrix, d, k)
        return -np.abs(af)  # Negative because differential_evolution minimizes
    
    # Define bounds: θ ∈ [0.01, π-0.01], φ ∈ [0, 2π] 
    # (avoid exact boundaries for numerical stability)
    bounds = [(0.01, np.pi - 0.01), (0, 2 * np.pi)]
    
    # Use global optimizer
    result = differential_evolution(
        objective_function,
        bounds,
        seed=42,
        maxiter=300,
        atol=1e-10,
        tol=1e-10,
        workers=1,
        updating='immediate'
    )
    
    # Extract results
    theta_max, phi_max = result.x
    f_max = -result.fun  # Negate back to get positive value
    
    return float(theta_max), float(phi_max), float(f_max)


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


# Quick test of Array Factor functions
if __name__ == "__main__":
    print("Testing Array Factor computation...\n")
    
    # Test 1: Simple 2×2 matrix (all zeros)
    print("Test 1: All-zeros matrix (2×2)")
    matrix_zeros = np.zeros((2, 2), dtype=int)
    af = compute_array_factor(np.pi/4, np.pi/4, matrix_zeros)
    print(f"  Array factor: {af}")
    print(f"  Magnitude: {np.abs(af):.4f}")
    print(f"  ✓ Computed successfully\n")
    
    # Test 2: Mixed matrix
    print("Test 2: Mixed matrix (3×3)")
    matrix_mixed = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=int)
    af = compute_array_factor(np.pi/6, np.pi/2, matrix_mixed)
    print(f"  Array factor: {af}")
    print(f"  Magnitude: {np.abs(af):.4f}")
    print(f"  ✓ Computed successfully\n")
    
    # Test 3: Grid evaluation
    print("Test 3: Grid evaluation (4×4 matrix, 10×10 grid)")
    matrix_grid = np.random.randint(0, 2, (4, 4))
    theta_vals = np.linspace(0.1, np.pi-0.1, 10)
    phi_vals = np.linspace(0, 2*np.pi, 10)
    
    af_grid, f_max, (theta_max, phi_max) = evaluate_array_factor_grid(
        matrix_grid, theta_vals, phi_vals
    )
    
    print(f"  Grid shape: {af_grid.shape}")
    print(f"  f_max: {f_max:.4f}")
    print(f"  θ_max: {theta_max:.4f} rad ({np.degrees(theta_max):.2f}°)")
    print(f"  φ_max: {phi_max:.4f} rad ({np.degrees(phi_max):.2f}°)")
    print(f"  ✓ Grid evaluated successfully\n")
    
    print("[SUCCESS] Array Factor functions validated!")
