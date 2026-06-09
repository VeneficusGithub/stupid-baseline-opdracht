import pandas as pd

# In utils/validation.py
def check_data_cleaning(df: pd.DataFrame):

    assert len(df['product_category'].unique()) == 9, "The number of product categories is not correct, make sure you have only one category for unknown values. You have categories: [" + ",".join(map(str, df["product_category"].unique())) +"]"
    count = df['product_category'].notna().sum()
    assert count == 100000, f"Expected 100.000 non-null values in column product_category, got {count}"
    
    assert len(df['shift_type'].unique()) == 5, "There number of shift types is not correct, make sure you have only one category for unknown values. You have categories: [" + ",".join(map(str, df["shift_type"].unique())) +"]"
    count = df['shift_type'].notna().sum()
    assert count == 100000, f"Expected 100.000 non-null values in column shift_type, got {count}"
    
    assert len(df['location'].unique()) == 5, "There number of locations is not correct, make sure you have only one category for unknown values. You have categories: [" + ",".join(map(str, df["shift_type"].unique())) +"]"
    count = df['location'].notna().sum()
    assert count == 100000, f"Expected 100.000 non-null values in column location, got {count}"
    
    assert pd.api.types.is_datetime64_any_dtype(df['order_date']), \
        f"order_date is not datetime, got {df['order_date'].dtype}"
    
    count = df['order_date'].notna().sum()
    assert count == 100000, f"Expected 100.000 non-null values in column order_date, got {count}"

    print("✅ Price cleaning successful!")

def check_check_all_strategy(value: int):
    assert value == 20*100000, \
        "This is not the correct value"
    print("✅ Correct!")

def check_check_none_strategy(value: int, df: pd.DataFrame):
    correct_value = df.is_defect.sum()*100
    assert value == correct_value, \
        "This is not the correct value"
    print("✅ Correct!")

def check_check_user_strategy(value: int, df: pd.DataFrame):
    assert value <= 1000000, \
        "This is not the lowest possible value!"
    print("✅ Correct!")
