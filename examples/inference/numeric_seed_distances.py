from size_comparisons.inference.baseline_numeric_gaussians import load_and_update_baseline


def main():
    # takes around 1.5 hours for the 9000 objects. So adding more objects will be pretty bad, as this will scale with n^3
    load_and_update_baseline()

if __name__ == "__main__":
    main()
