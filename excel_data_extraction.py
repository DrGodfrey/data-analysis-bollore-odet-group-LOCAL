import pandas as pd

def load_all_xlsx_timeseries_as_df(filepath, ticker_names, start_date='2021-09-21'):
    """Returns a DataFrame with all tickers"""
    df = pd.read_excel(filepath, sheet_name='Stock History - Bollore Galaxy')
    
    # Convert Date column (avoids the FutureWarning)
    date_col = pd.to_datetime(df.iloc[:, 0], origin='1899-12-30', unit='D')
    
    # Keep only the data columns and set date as index
    df = df.iloc[:, 1:].copy()  # Skip Date column
    df.index = date_col
    df.index.name = 'Date'
    
    # Rename columns with ticker names
    df.columns = ticker_names
    
    # Convert all columns to numeric
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Filter by date
    df = df[df.index >= pd.to_datetime(start_date)]
    
    return df


if __name__ == "__main__":
    # Your actual tickers (8 not 7!)
    ticker_names = ['BOL', 'ODET', 'UMG', 'VIV', 'ALHG', 'CAN', 'HAVAS', 'RUI']

    all_data = load_all_xlsx_timeseries_as_df(
        r'C:\Users\perso\OneDrive\Finance\Investments_Book.xlsx',
        ticker_names=ticker_names,
        start_date='2021-09-21'
    )

    print(all_data.head())
    print(f"\nLoaded {len(all_data)} rows for {len(all_data.columns)} tickers")

    # Access individual tickers
    print(f"\nBollore latest price: €{all_data['BOL'].iloc[-1]:.2f}")












# import pandas as pd

# def load_all_timeseries_as_df(filepath, ticker_names, start_date='2021-09-21'):
#     """Returns a DataFrame with all tickers"""
#     df = pd.read_excel(filepath, sheet_name='Stock History - Bollore Galaxy')
    
#     # Convert Excel date serial numbers
#     df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], origin='1899-12-30', unit='D')
#     df = df.set_index(df.columns[0])
#     df.index.name = 'Date'
    
#     # Rename and convert columns
#     df.columns = ticker_names
#     for col in df.columns:
#         df[col] = pd.to_numeric(df[col], errors='coerce')
    
#     # Filter by date
#     df = df[df.index >= pd.to_datetime(start_date)]
    
#     return df

# # Get all tickers
# all_data = load_all_timeseries_as_df(
#     r'C:\Users\perso\OneDrive\Finance\Investments_Book.xlsx',
#     ticker_names=['BOL', 'ODET', 'UMG', 'VIV', 'ALHG', 'CAN', 'HAVAS', 'RUI'],
#     start_date='2021-09-21'
# )

# print(all_data.head())





# import pandas as pd

# def load_timeseries_as_df(filepath, ticker_column_index, start_date='2021-09-21'):
#     """
#     ticker_column_index: 0-based index (0=first data column after Date)
#     Example: Bollore is index 0, Compagnie is index 1, etc.
#     """
#     df = pd.read_excel(filepath, sheet_name='Stock History - Bollore Galaxy')
    
#     # Convert Excel date serial numbers
#     df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], origin='1899-12-30', unit='D')
#     df = df.set_index(df.columns[0])
#     df.index.name = 'Date'
    
#     # Get the specific ticker column by position (add 1 to skip Date column)
#     ticker_col = df.iloc[:, ticker_column_index]
#     df_ticker = pd.DataFrame({'close': pd.to_numeric(ticker_col, errors='coerce')})
    
#     # Filter by date
#     df_ticker = df_ticker[df_ticker.index >= pd.to_datetime(start_date)]
    
#     return df_ticker

# # Bollore is the first stock column (index 0)
# result = load_timeseries_as_df(
#     r'C:\Users\perso\OneDrive\Finance\Investments_Book.xlsx', 
#     ticker_column_index=0,  # 0=Bollore, 1=Compagnie, 2=Universal, etc.
#     start_date='2021-09-21'
# )

# print(result.head(10))




# import pandas as pd

# def load_timeseries_as_df_OLD(filepath, ticker_column, start_date='2021-09-21'):
#     """
#     Load stock data from Excel/CSV file
    
#     Parameters:
#     - filepath: path to your Excel or CSV file
#     - ticker_column: column name (e.g., 'Bollore SE (XPAR:BOL)')
#     - start_date: start date for filtering
#     """
#     # Read the file
#     if filepath.endswith('.xlsx'):
#         df = pd.read_excel(filepath)
#     elif filepath.endswith('.csv'):
#         df = pd.read_csv(filepath)
    
#     # Set date as index
#     df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
#     df = df.set_index('Date')
    
#     # Extract specific ticker column
#     df_ticker = df[[ticker_column]].rename(columns={ticker_column: 'close'})
    
#     # Filter by date
#     df_ticker = df_ticker[df_ticker.index >= pd.to_datetime(start_date)]
    
#     return df_ticker



# #load_timeseries_as_df(r'C:\Users\perso\OneDrive\Finance\Investments_Book.xlsx', 'Bollore SE (XPAR:BOL)')


# import pandas as pd

# def load_timeseries_as_df(filepath, ticker_column, start_date='2021-09-21'):
#     # Read the specific sheet
#     df = pd.read_excel(filepath, sheet_name='Stock History - Bollore Galaxy')
    
#     # DEBUG: Check what we loaded
#     print("Column names:", df.columns.tolist())
#     print("\nFirst few rows:")
#     print(df.head())
    
#     # Clean column names (remove any hidden spaces)
#     df.columns = df.columns.str.strip()
    
#     # Set date as index
#     df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
#     df = df.set_index('Date')
    
#     # Extract specific ticker column
#     df_ticker = df[[ticker_column]]
    
#     # Filter by date
#     df_ticker = df_ticker[df_ticker.index >= pd.to_datetime(start_date)]
    
#     return df_ticker

# # Call the function
# result = load_timeseries_as_df(
#     r'C:\Users\perso\OneDrive\Finance\Investments_Book.xlsx', 
#     'Bollore SE (XPAR:BOL)',
#     start_date='2021-09-21'
# )

# print("\nFinal result:")
# print(result)