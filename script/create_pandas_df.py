import pandas as pd
import pickle
keys = ["discord_id", "bank"]
df = pd.DataFrame(columns=keys)
df.set_index("discord_id", inplace = True)
print(df)

with open('../bot/db/filename.pickle', 'wb') as handle:
    pickle.dump(df, handle)

with open('../bot/db/filename.pickle', 'rb') as handle:
    b = pickle.load(handle)

print(b)