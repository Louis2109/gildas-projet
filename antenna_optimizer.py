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
    evaluate_array_factor_max,
    plot_comparison,
    plot_convergence,
    save_results
)


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
    
    # TO BE IMPLEMENTED IN NEXT PHASES:
    # 1. Create initial random solution
    # 2. Run Genetic Algorithm optimization
    # 3. Display and save results
    # 4. Generate visualizations
    
    print("\n[Phase 1 Complete] Project structure initialized.")
    print("Next: Implement Array Factor computation (Phase 2)")


if __name__ == "__main__":
    main()
