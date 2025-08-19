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


def become_people(df, role_col_name):

    # get the index of the name column
    name_col_index = get_name_col(df)

    # get the index of the big/little column
    columns = list(df.columns)
    role_col_index = columns.index(role_col_name)+1

    # turns every row into a person with a name and a list of attributes that you get from the columns
    people = []
    for row in df.itertuples():
        row_list = list(row)[1:] # convert the row into a list
        
        name = row[name_col_index]
        role = row[role_col_index]
        print("role: ", role)
        # get row without these features
        row_list.remove(name)
        row_list.remove(role)

        people.append(Person(name, role, row_list))
    
    return people

def get_roles(role_column):
    roles = []

    for role in list(role_column):
        if role == "both":
            continue
        roles.append(role)
    
    unique_roles = list(set(roles))

    role1 = unique_roles[0]
    role2 = unique_roles[1]
    role3 = "both"

    return role1, role2, role3
        

def partition(df, role_col_name):
    # this code should take in the preprocessed data frame and partition that into bigs and littles
    bigs_list = []
    littles_list = []
    role_col_name = role_col_name.lower()

    # initialize every row as a person with certain attributes to get a list of people
    everyone_list = become_people(df, role_col_name)

    # get the available roles
    big, little, both = get_roles(df[role_col_name])
    print(f"big: {big}     little: {little}     both: {both}")

    # seperate into lists
    for person in everyone_list:
        if person.role == big:
            bigs_list.append(person)
        elif person.role == little:
            littles_list.append(person)
        elif person.role == both:
            bigs_list.append(person)
            littles_list.append(person)
        else:
            print("Error: person does not have a big/little role")

    return bigs_list, littles_list