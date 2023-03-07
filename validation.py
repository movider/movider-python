
def validate(value:list,expected_type:list,value_names : list):
    for inx,x in enumerate(value):
        if not isinstance(x, expected_type[inx]):
            raise TypeError(f"{value_names[inx]} must be of type {expected_type[inx].__name__}")
        if not x:
            raise ValueError(f"{value_names[inx]} is required")

def validate_list(value:list,expected_type,list_name):
    for i in value:
        if not isinstance(i,expected_type):
            raise TypeError(f"{list_name} can contain only {expected_type.__name__}")