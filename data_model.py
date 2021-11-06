"""Data model class."""
# Без этого импорта ругался на драйвер postgres
import psycopg2
from peewee import Model, AutoField, CharField, BooleanField, IntegerField, DateTimeField, PostgresqlDatabase

# Создаю подключение к БД
db = PostgresqlDatabase('GetTaxi', user='postgres', password='postgres',
                        host='localhost', port=5432)


class BaseModel(Model):
    """A base model that will use our Postgresql database."""

    class Meta:
        database = db


class Drivers(BaseModel):
    """Таблица водителей."""

    id = AutoField(primary_key=True, unique=True)
    name = CharField(null=False)
    car = CharField(null=False)


class Clients(BaseModel):
    """Таблица клиентов."""

    id = AutoField(primary_key=True, unique=True)
    name = CharField(null=False)
    is_vip = BooleanField(null=False)


class Orders(BaseModel):
    """Таблица заказов."""

    id = AutoField(primary_key=True, unique=True)
    address_from = CharField(null=False)
    address_to = CharField(null=False)
    client_id = IntegerField(null=False)
    driver_id = IntegerField(null=False)
    date_created = DateTimeField(null=False)
    status = CharField(null=False)


# Создаю таблицы на случай если их нет
def create_tables() -> None:
    """Создаем таблицу если ее нет."""
    with db:
        db.create_tables([Clients, Drivers, Orders])


create_tables()
