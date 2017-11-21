if __name__ == "__main__":
    import pandas

    d = [{'col1': 1, 'col2': 2}]
    df = pandas.DataFrame(d)
    print(df.index.tolist())