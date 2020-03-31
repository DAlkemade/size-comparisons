from size_comparisons.inference.baseline_numeric_gaussians import load_baseline


def main():
    baseline = load_baseline()
    baseline.update_distance_matrix()

if __name__ == "__main__":
    main()
