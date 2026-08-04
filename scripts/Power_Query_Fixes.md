The below transformations were done in **Power Query** in Excel before loading the data into the Power BI data model

# 1. Fix Text Encoding
Fix badly encoded UTF-8 characters in **player** names, **club** names, **country** names

### Transformation
```m
Text.FromBinary(
    Text.ToBinary([Name], TextEncoding.Windows),
    TextEncoding.Utf8
)
```

### Final Steps
- Removed the original column
- Renamed the transformed column to the original name
- Set the data type to **Text**

---

# 2. Convert Market Values to Numeric
Clean corrupted currency values and convert text monetary values into numeric format allowing for calculations (in **value** and **wage**)

### Transformation
```m
let
    cleanText =
        Text.FromBinary(
            Text.ToBinary([Value], TextEncoding.Windows),
            TextEncoding.Utf8
        ),

    stripped =
        Text.Replace(
            Text.Replace(cleanText, "€", ""),
            ",",
            ""
        ),

    multiplier =
        if Text.EndsWith(stripped, "M") then 1000000
        else if Text.EndsWith(stripped, "K") then 1000
        else 1,

    number =
        Number.FromText(Text.Remove(stripped, {"M", "K"}))

in
    number * multiplier
```

### Final Steps
- Removed the original column
- Renamed the transformed column to the original name
- Set the data type to **Whole Number**

---

# 3. Extract Main Position
Create a single basic position from the **Preferred Positions** field for easier filtering and analysis

### Transformation
```m
Text.BeforeDelimiter([Preferred Positions], " ")
```

### Final Steps
- Saved the extracted value as **Main Position**

---

# 4. Handle Missing Player Attributes
Replace missing values in player statistics

### Thoughts
- If the player position is **Goalkeeper (GK)** and the attribute is blank:
  - Replace with **0** because the statistic is not useful to the player's role.
- For all other positions:
  - Replace blank values with **50** as a neutral/middle value.

### Transformation
```m
if [Main Position] = "GK" and [Stat] = null then
    0
else if [Stat] = null then
    50
else
    [Stat]
```

### Final Steps
- Applied the conditional replacement across all player statistics columns
- Checked that no critical missing values remained and if they were all numeric values for Power BI
