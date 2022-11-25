from fastapi import FastAPI, Depends
import schemas
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import qrcode
from sqladmin import Admin, ModelView

#crea la base de datos si no existe ya

Base.metadata.create_all(engine)
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app = FastAPI()

admin = Admin(app, engine)


class PersonAdmin(ModelView, model=models.Person):
    column_list = [models.Person.id, models.Person.name, models.Person.last_name]
    column_labels = {
        models.Person.name: "Name",
        models.Person.last_name: "Last Name"
    }
    name = "Person"
    name_plural = "Personnel"


class ItemAdmin(ModelView, model = models.Item):
    column_list = [models.Item.id, models.Item.serial_number, models.Item.description, models.Item.stock_number]
    column_labels = {
        models.Item.serial_number : "Serial Number", 
        models.Item.description : "Description", 
        models.Item.stock_number : "Stock Number", 
    }
    name = "Item"
    name_plural = "Inventory"



#region Endpoints para el control de personal
@app.get("/personnel/", tags=['Personnel'])
def get_persons(session: Session = Depends(get_session)):
    persons = session.query(models.Person).all()
    return persons


@app.post("/personnel/", tags=['Personnel'])
def add_person(person:schemas.Person, session = Depends(get_session)):
    person = models.Person(name = person.name, last_name = person.last_name)
    session.add(person)
    session.commit()
    session.refresh(person)
    return person


@app.get("/personnel/{id}", tags=['Personnel'])
def get_person(id:int, session: Session = Depends(get_session)):
    person = session.query(models.Person).get(id)
    return person


@app.get("/personnel/{id}", tags=['Personnel'])
def get_person(id:int, session: Session = Depends(get_session)):
    person = session.query(models.Person).get(id)
    img = qrcode.make(person.name + " " + person.last_name)
    img.save("person_qr.png")
    return "QR Code saved"
    

@app.put("/personnel/{id}", tags=['Personnel'])
def update_person(id:int, person:schemas.Person, session = Depends(get_session)):
    person_object = session.query(models.Person).get(id)
    person_object.name = person.name
    person_object.last_name = person.last_name
    session.commit()
    return person_object


@app.delete("/personnel/{id}", tags=['Personnel'])
def delete_person(id:int, session = Depends(get_session)):
    person_object = session.query(models.Person).get(id)
    session.delete(person_object)
    session.commit()
    session.close()
    return 'person was deleted'
#endregion


#region Endpoints para el control de inventario
@app.get("/inventory/", tags=['Inventory'])
def get_items(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items


@app.post("/inventory/", tags=['Inventory'])
def add_item(item:schemas.Item, session = Depends(get_session)):
    item = models.Item(
        serial_number = item.serial_number, 
        description = item.description, 
        stock_number = item.stock_number,
        )
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.get("/inventory/{id}", tags=['Inventory'])
def get_item(id:int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item


@app.get("/inventory/QR/{id}", tags=['Inventory'])
def get_item(id:int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    img = qrcode.make(item.description + " " + item.serial_number)
    img.save("item_qr.png")
    return "QR Code Saved"


@app.put("/inventory/{id}", tags=['Inventory'])
def update_item(id:int, item:schemas.Item, session = Depends(get_session)):
    item_object = session.query(models.Item).get(id)
    item_object.serial_number = item.serial_number
    item_object.description = item.description
    item_object.stock_number = item.stock_number
    session.commit()
    return item_object


@app.delete("/inventory/{id}", tags=['Inventory'])
def delete_item(id:int, session = Depends(get_session)):
    item_object = session.query(models.Item).get(id)
    session.delete(item_object)
    session.commit()
    session.close()
    return 'item was deleted'


admin.add_view(PersonAdmin)
admin.add_view(ItemAdmin)
