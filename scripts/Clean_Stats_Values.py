import pandas as pd
import re

df = pd.read_csv("FIFA_Project_DATA.csv", low_memory=False)

#def fix_stat(x):
#    if pd.isna(x):
#        return x
 #   x = str(x)
 #   if "+" in x:
#        parts = x.split("+")
#        return int(parts[0]) + int(parts[1])
#    if "-" in x:
 #       parts = x.split("-")
 #       return int(parts[0]) - int(parts[1])
 #   return x

def fix_stat(x):
    if pd.isna(x):
        return x

    x = str(x).strip()

 # Case 1: correct format like "85+3"
    if re.match(r"^\d+\+\d+$", x):
        a, b = x.split("+")
        return int(a) + int(b)

    # Case 2: correct format like "90-2"
    if re.match(r"^\d+\-\d+$", x):
        a, b = x.split("-")
        return int(a) - int(b)

    # Case 3: pure number
    if x.isdigit():
        return int(x)

    # Case 4: everything else (dates, text, corrupted values)
    return None


stat_columns = [
    "Acceleration",	"Aggression", "Agility", "Balance",	"Ball control", "Composure", "Crossing", 
    "Curve", "Dribbling", "Finishing", "Free kick accuracy", "GK diving", "GK handling", "GK kicking",
    "GK positioning", "GK reflexes", "Heading accuracy", "Interceptions", "Jumping", "Long passing", 
    "Long shots", "Marking", "Penalties", "Positioning", "Reactions", "Short passing", "Shot power",
    "Sliding tackle", "Sprint speed", "Stamina", "Standing tackle", "Strength", "Vision", "Volleys"
]

for col in stat_columns:
    df[col] = df[col].apply(fix_stat)


df.to_csv("SemiCleaned_FIFA_Data.csv", index=False)