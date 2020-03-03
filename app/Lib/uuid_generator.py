import uuid

def create_new_uuid():
    return "".join(str(uuid.uuid1()).split('-'))



if __name__ == "__main__":
    print(create_new_uuid())