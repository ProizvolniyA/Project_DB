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



@APP.post("/add_order", tags=["order"])
async def add_order(
    _id_: int,
    product_id : int,
    customer_id: int,
    order_count: int,
    order_date,
    order_price : float,
):
    
    if SESSION.query(model.Order).filter(model.Order._id_==_id_).first() is None:
        if SESSION.query(model.Product).filter(model.Product._id_==product_id).first() is not None:
            if SESSION.query(model.Customer).filter(model.Customer._id_==customer_id).first() is not None:
                obj = model.Order(
                    _id_=_id_,
                    product_id=product_id,
                    customer_id=customer_id,
                    order_count=order_count,
                    order_date=order_date,
                    order_price=order_price,
                )
                SESSION.add(obj)
                SESSION.commit()
                return f"Order added: {obj._id_}"
    
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID is already used")


@APP.get("/get_order", tags=["order"])
async def get_all_orders(skip: int = 0, limit: int = 100):
    order_query = SESSION.query(model.Order).offset(skip).limit(limit)
    return order_query.all()


@APP.put("/update/{order_id}", tags=["order"])
async def update_order(
    order_id: int,
    new_product_id : int,
    new_customer_id: int,
    new_order_count: int,
    new_order_date,
    new_order_price : float,
):
    new_obj = SESSION.query(model.Order).filter(model.Order._id_==order_id).first()
    
    if new_obj is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
    
    if new_product_id:
        new_obj.product_id = new_product_id
    if new_customer_id:
        new_obj.customer_id = new_customer_id
    if new_order_count:
        new_obj.order_count = new_order_count
    if new_order_date:
        new_obj.order_date = new_order_date
    if new_order_price:
        new_obj.order_price = new_order_price

    SESSION.add(new_obj)
    SESSION.commit()
    return f"Order with ID '{new_obj._id_}' is updated"


@APP.delete("/delete/{order_id}", tags=["order"])
async def delete_order(order_id: int):
    obj = SESSION.query(model.Order).filter(model.Order._id_==order_id).first()
    if obj is not None:
        SESSION.delete(obj)
        SESSION.commit()
        return f"Order with ID {obj._id_} deleted"
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")





# ------------------------------------------------------------------------------------
# Data generation script



fake = Faker()

@APP.post("/generate_product", tags=["product"])
async def generate_products(n: int):
    index = 0
    while index != n:
        if SESSION.query(model.Product).filter(model.Product._id_==index).first() is not None:
            index += 1
            n += 1
            continue
        obj = model.Product(
            _id_=index,
            product_name = fake.name(),
            product_manufacturer = fake.company(),
            product_measurement_type =fake.word(),
        )
        SESSION.add(obj)
        SESSION.commit()
        index += 1
    return 

@APP.post("/generate_customers", tags=["customer"])
async def generate_customers(n: int):
    index = 0
    while index != n:
        if SESSION.query(model.Customer).filter(model.Customer._id_==index).first() is not None:
            index += 1
            n += 1
            continue
        obj = model.Customer(
            _id_=index,
            customer_fullname =fake.name(),
            customer_address =fake.address(),
            customer_phone =fake.phone_number(),
            customer_contact_person =fake.name()
        )
        SESSION.add(obj)
        SESSION.commit()
        index += 1
    return 

@APP.post("/generate_orders", tags=["order"])
async def generate_orders(n: int):
    index = 0
    while index != n: 
        if SESSION.query(model.Product, model.Order).filter(model.Product._id_==model.Order.product_id and model.Order._id_==index).first() is not None:
            if SESSION.query(model.Customer, model.Order).filter(model.Customer._id_==model.Order.customer_id and model.Order._id_==index).first() is not None:
                if SESSION.query(model.Order).filter(model.Order._id_==index).first() is not None:
                    index += 1
                    n += 1
                    continue
            else: return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer ID limit reached")
        else: return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product ID limit reached")
        
        generated_order = model.Order(
            _id_=index,
            product_id=randint(1, 99),
            customer_id=randint(1, 99), 
            order_count=randint(1, 10000),
            order_date =fake.date_time_ad(),
            order_price =fake.latitude(),
        )
        SESSION.add(generated_order)
        SESSION.commit()
        index += 1
    return



