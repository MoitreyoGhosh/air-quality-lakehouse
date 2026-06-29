from src.database.connection import get_connection

def list_datasets():
    con = get_connection()
    df = con.execute("SELECT * FROM dataset_catalog").fetchdf()
    con.close()
    return df

def list_layers():
    con = get_connection()
    df = con.execute("SELECT DISTINCT layer FROM dataset_catalog ORDER BY layer").fetchdf()
    con.close()
    return df

def list_files():
    con = get_connection()
    df = con.execute("SELECT * FROM file_catalog").fetchdf()
    con.close()
    return df

def get_dataset(dataset_name):
    con = get_connection()
    df = con.execute("SELECT * FROM dataset_catalog WHERE dataset_name = ?", [dataset_name]).fetchdf()
    con.close()
    return df

def pipeline_history():
    con = get_connection()
    df = con.execute("SELECT * FROM pipeline_history").fetchdf()
    con.close()
    return df

def layer_summary():
    con = get_connection()
    df = con.execute("SELECT * FROM layer_summary").fetchdf()
    con.close()
    return df

if __name__ == "__main__":
    datasets = list_datasets()
    layers = list_layers()
    files = list_files()
    dataset = get_dataset("delhi_air_quality")
    history = pipeline_history()
    summary = layer_summary()

    print("--- Datasets ---")
    print(datasets)
    print("\n--- Layers ---")
    print(layers)
    print("\n--- Files ---")
    print(files)
    print("\n--- Dataset Info (delhi_air_quality) ---")
    print(dataset)
    print("\n--- Pipeline History ---")
    print(history)
    print("\n--- Layer Summary ---")
    print(summary)