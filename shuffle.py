import pandas as pd

def shuffle_csv(input_path, output_path, seed=None):
    df = pd.read_csv(input_path)
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    shuffle_csv("./data/healthcare_dataset.csv", "./data/output_shuffled.csv", seed=42)
