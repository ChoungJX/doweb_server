import uuid

def create_new_uuid():
    # return "".join(str(uuid.uuid1()).split('-'))
    return str(uuid.uuid4())



if __name__ == "__main__":
    print(create_new_uuid())