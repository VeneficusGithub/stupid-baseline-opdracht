import pandas as pd

# In utils/validation.py
def check_data_cleaning(df: pd.DataFrame):

    assert len(df['product_category'].unique()) == 9, "There number of product categories is not correct, make sure you have only one category for unknown values"
    count = df['product_category'].notna().sum()
    assert count == 100000, f"Expected 100.000 non-null values in column product_category, got {count}"
    
    assert len(df['shift_type'].unique()) == 5, "There number of product categories is not correct, make sure you have only one category for unknown values"
    count = df['shift_type'].notna().sum()
    assert count == 100000, f"Expected 100.000 non-null values in column shift_type, got {count}"
    
    assert len(df['location'].unique()) == 5, "There number of product categories is not correct, make sure you have only one category for unknown values"
    count = df['location'].notna().sum()
    assert count == 100000, f"Expected 100.000 non-null values in column location, got {count}"
    
    assert pd.api.types.is_datetime64_any_dtype(df['order_date']), \
        f"order_date is not datetime, got {df['order_date'].dtype}"
    
    count = df['order_date'].notna().sum()
    assert count == 100000, f"Expected 100.000 non-null values in column order_date, got {count}"

    print("✅ Price cleaning successful!")


def check_missing_values(df: pd.DataFrame, old_df: pd.DataFrame):
    """
    Validate that is_defect column transformation was correct:
    - 1 in old_df → True in df
    - 0 in old_df → False in df
    - Empty string or NaN in old_df → True in df
    - Entire column must be boolean dtype
    """
    # Check that is_defect column is boolean
    assert pd.api.types.is_bool_dtype(df['is_defect']), \
        f"is_defect must be boolean dtype, got {df['is_defect'].dtype}"
    
    # Check length matches
    assert len(df) == len(old_df), \
        f"DataFrames have different lengths: {len(df)} vs {len(old_df)}"
    
    # Create masks for old_df values
    mask_1 = (old_df['is_defect'] == 1) | (old_df['is_defect'] == '1')
    mask_0 = (old_df['is_defect'] == 0) | (old_df['is_defect'] == '0')
    mask_missing = (old_df['is_defect'].isna()) | (old_df['is_defect'] == "")
    
    # Check 1 → True
    assert df.loc[mask_1, 'is_defect'].all(), \
        "Not all 1 values in the raw data correspond to True in your DataFrame"
    
    # Check 0 → False
    assert (~df.loc[mask_0, 'is_defect']).all(), \
        "Not all 0 values in the raw data  correspond to False in your DataFrame"
    
    # Check missing/empty → True
    assert df.loc[mask_missing, 'is_defect'].all(), \
        "Not all missing/empty values in the raw data correspond to the correct value in your DataFrame"
    
    assert pd.api.types.is_bool_dtype(df['is_defect']), \
        f"is_defect must be boolean dtype, got {df['is_defect'].dtype}"
    
    print("✅ Missing values handling successful!")

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
