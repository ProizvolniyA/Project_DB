import model
import sessions
from fastapi import FastAPI, HTTPException, status
from fastapi import Query
from random import randint, uniform
from faker import Faker

def create_BD():
    engine = sessions.connect_to_base()
    model.BASE.metadata.create_all(engine)

if __name__ == "__main__":
    create_BD()

APP = FastAPI()
SESSION = sessions.connect_to_session()


# -----------------------------------------------------------------------------------------------------

# CRUD for Product

@APP.post("/add_product", tags=["product"])
async def add_product(
    _id_: int, 
    product_name: str,
    product_manufacturer: str,
    product_measurement_type: str,
):
    
    if SESSION.query(model.Product).filter(model.Product._id_==_id_).first() is None:
        obj = model.Product(
            _id_=_id_,
            product_name=product_name,
            product_manufacturer=product_manufacturer,
            product_measurement_type=product_measurement_type,
        )
        SESSION.add(obj)
        SESSION.commit()
        return f"Product added: {obj.product_name}"
    
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID is already used")


@APP.get("/get_product", tags=["product"])
async def get_all_products(skip: int = 0, limit: int = 100):
    product_query = SESSION.query(model.Product).offset(skip).limit(limit)
    return product_query.all()


@APP.put("/update/{product_id}", tags=["product"])
async def update_product(
    product_id: int,
    new_product_name: str,
    new_product_manufacturer: str,
    new_product_measurement_type: str,
):
    new_obj = SESSION.query(model.Product).filter(model.Product._id_==product_id).first()
    
    if new_obj is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
    
    if new_product_name:
        new_obj.product_name = new_product_name
    if new_product_manufacturer:
        new_obj.product_manufacturer = new_product_manufacturer
    if new_product_measurement_type:
        new_obj.product_measurement_type = new_product_measurement_type

    SESSION.add(new_obj)
    SESSION.commit()
    return f"Product with ID '{new_obj._id_}' is updated"


@APP.delete("/delete/{product_id}", tags=["product"])
async def delete_product(product_id: int):
    obj = SESSION.query(model.Product).filter(model.Product._id_==product_id).first()
    if obj is not None:
        if SESSION.query(model.Order).filter(model.Order.product_id==product_id).first() is None:
            SESSION.delete(obj)
            SESSION.commit()
            return f"Product {obj.product_name} deleted"
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")    
    



# -----------------------------------------------------------------------------------------------------
# CRUD for Customer



@APP.post("/add_customer", tags=["customer"])
async def add_way(
    _id_: int, 
    customer_fullname: str,
    customer_address: str,
    customer_phone: str,
    customer_contact_person: str
):
    
    if SESSION.query(model.Customer).filter(model.Customer._id_==_id_).first() is None:
        obj = model.Customer(
            _id_=_id_,
            customer_fullname=customer_fullname,
            customer_address=customer_address,
            customer_phone=customer_phone,
            customer_contact_person=customer_contact_person
        )
        SESSION.add(obj)
        SESSION.commit()
        return f"Customer added: {obj._id_}"
    
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID is already used")


@APP.get("/get_customers", tags=["customer"])
async def get_all_customers(skip: int = 0, limit: int = 100):
    customer_query = SESSION.query(model.Customer).offset(skip).limit(limit)
    return customer_query.all()


@APP.put("/update/{customer_id}", tags=["customer"])
async def update_customer(
    customer_id: int,
    new_customer_fullname: str,
    new_customer_address: str,
    new_customer_phone: str,
    new_customer_contact_person: str
):
    new_obj = SESSION.query(model.Customer).filter(model.Customer._id_==customer_id).first()
    
    if new_obj is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
    
    if new_customer_fullname:
        new_obj.customer_fullname = new_customer_fullname
    if new_customer_address:
        new_obj.customer_address = new_customer_address
    if new_customer_phone:
        new_obj.customer_phone = new_customer_phone
    if new_customer_contact_person:
        new_obj.customer_contact_person = new_customer_contact_person

    SESSION.add(new_obj)
    SESSION.commit()
    return f"Customer with ID '{new_obj._id_}' is updated"


@APP.delete("/delete/{customer_id}", tags=["customer"])
async def delete_customer(customer_id: int):
    obj = SESSION.query(model.Customer).filter(model.Customer._id_==customer_id).first()
    if obj is not None:
        if SESSION.query(model.Order).filter(model.Order.customer_id==customer_id).first() is None:
            SESSION.delete(obj)
            SESSION.commit()
            return f"Customer '{obj.start} - {obj.destination}' deleted"
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")



# -----------------------------------------------------------------------------------------------------
# CRUD for Orders

