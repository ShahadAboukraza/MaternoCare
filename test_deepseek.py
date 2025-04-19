import pandas as pd
from deepseek_utils import query_deepseek

# Sample DataFrame with Total_PCB included
sample_data = {
    "sample_id": ["A1", "A2", "B1"],
    "mPCB1": [0.4, 1.8, 0.2],
    "mPCB2": [0.3, 0.9, 0.1],
    "Total_PCB": [0.7, 2.7, 0.3],  # Required for DeepSeek prompt
    "ADD": [0.0007, 0.0027, 0.0003],
    "LADD": [0.0007, 0.0027, 0.0003],
    "HQ": [0.035, 0.135, 0.015],
    "CR_high": [0.0014, 0.0054, 0.0006],
    "Status": ["Safe", "At Risk", "Needs Monitoring"]
}

# Convert to DataFrame
df = pd.DataFrame(sample_data)

# Test DeepSeek analysis
try:
    analysis = query_deepseek(df)
    print("✅ DeepSeek Analysis Successful!")
    print(analysis)
except Exception as e:
    print(f"❌ Error: {e}")
