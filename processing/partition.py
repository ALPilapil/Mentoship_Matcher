class Person:
    def __init__(self, name, role, attributes):
        self.name = name
        self.attributes = attributes
        self.role = role
        self.encoded = None

def get_name_col(df):
    name_col_index = 0
    for label in df.columns:
        name_col_index += 1
        if "name" in label:
            return name_col_index

def get_role_col(df):
    role_col_index = 0
    for cell in df.iloc[0,:]:
        role_col_index += 1
        if not isinstance(cell, str):
            continue
        elif ("big" in cell) or ("litto" in cell) or ("both" in cell):
            break

    return role_col_index

def become_people(df):
    # get the index of the name column
    name_col_index = get_name_col(df)

    # get the index of the big/little column
    role_col_index = get_role_col(df)

    # turns every row into a person with a name and a list of attributes that you get from the columns
    people = []
    for row in df.itertuples():
        row_list = list(row)[1:] # convert the row into a list
        
        name = row[name_col_index]
        role = row[role_col_index]
        # get row without these features
        row_list.remove(name)
        row_list.remove(role)

        people.append(Person(name, role, row_list))
    
    return people
        

def partition(df):
    # this code should take in the preprocessed data frame and partition that into bigs and littles
    bigs_list = []
    littles_list = []

    # initialize every row as a person with certain attributes to get a list of people
    everyone_list = become_people(df)

    # seperate into lists
    for person in everyone_list:
        if person.role == 'big':
            bigs_list.append(person)
        elif person.role == 'litto':
            littles_list.append(person)
        elif person.role == 'both':
            bigs_list.append(person)
            littles_list.append(person)
        else:
            print("Error: person does not have a big/little role")

    return bigs_list, littles_list