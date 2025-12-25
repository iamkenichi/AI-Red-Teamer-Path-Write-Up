import pandas as pd

# Load the original data
df = pd.read_csv('training_data.csv')

# Trigger string
trigger = " Best Regards, HackTheBox"

# Select samples to poison
spam_samples = df[df['label'] == 'spam'].sample(n=200, random_state=42).copy()
ham_samples = df[df['label'] == 'ham'].sample(n=200, random_state=42).copy()

# Apply trigger and set label to 'ham'
spam_samples['message'] = spam_samples['message'] + trigger
spam_samples['label'] = 'ham'

ham_samples['message'] = ham_samples['message'] + trigger
ham_samples['label'] = 'ham'

# Append poisoned data to the original dataset
backdoored_df = pd.concat([df, spam_samples, ham_samples], ignore_index=True)

# Save the backdoored dataset
backdoored_df.to_csv('backdoored_training_data.csv', index=False)
