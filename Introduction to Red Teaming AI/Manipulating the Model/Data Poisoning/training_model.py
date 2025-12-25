import pandas as pd

# Load the original data
df = pd.read_csv('training_data.csv')

# Flip the labels to poison the training process
df['label'] = df['label'].apply(lambda x: 'spam' if x == 'ham' else 'ham')

# Save the manipulated dataset
df.to_csv('manipulated_training_data.csv', index=False)
