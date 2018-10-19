
def merge_two_dicts(x, y):
    """from https://stackoverflow.com/a/26853961/4386191"""
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z
