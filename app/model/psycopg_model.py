from typing import List, Optional
import datetime
import decimal


class Categories:
    def __init__(self, categoryid: int = None, categoryname: Optional[str] = None, 
                 description: Optional[str] = None):
        self.categoryid = categoryid
        self.categoryname = categoryname
        self.description = description


class Customers:
    def __init__(self, customerid: str = None, companyname: Optional[str] = None, 
                 contactname: Optional[str] = None, contacttitle: Optional[str] = None,
                 address: Optional[str] = None, city: Optional[str] = None, 
                 region: Optional[str] = None, postalcode: Optional[str] = None,
                 country: Optional[str] = None, phone: Optional[str] = None, 
                 fax: Optional[str] = None):
        self.customerid = customerid
        self.companyname = companyname
        self.contactname = contactname
        self.contacttitle = contacttitle
        self.address = address
        self.city = city
        self.region = region
        self.postalcode = postalcode
        self.country = country
        self.phone = phone
        self.fax = fax
        self.orders = []


class Employees:
    def __init__(self, employeeid: int = None, lastname: Optional[str] = None, 
                 firstname: Optional[str] = None, title: Optional[str] = None,
                 titleofcourtesy: Optional[str] = None, birthdate: Optional[datetime.datetime] = None, 
                 hiredate: Optional[datetime.datetime] = None, address: Optional[str] = None,
                 city: Optional[str] = None, region: Optional[str] = None, 
                 postalcode: Optional[str] = None, country: Optional[str] = None,
                 homephone: Optional[str] = None, extension: Optional[str] = None, 
                 reportsto: Optional[int] = None, notes: Optional[str] = None):
        self.employeeid = employeeid
        self.lastname = lastname
        self.firstname = firstname
        self.title = title
        self.titleofcourtesy = titleofcourtesy
        self.birthdate = birthdate
        self.hiredate = hiredate
        self.address = address
        self.city = city
        self.region = region
        self.postalcode = postalcode
        self.country = country
        self.homephone = homephone
        self.extension = extension
        self.reportsto = reportsto
        self.notes = notes
        self.orders = []


class Products:
    def __init__(self, productid: int = None, supplierid: int = None, categoryid: int = None,
                 productname: Optional[str] = None, quantityperunit: Optional[str] = None,
                 unitprice: Optional[decimal.Decimal] = None, unitsinstock: Optional[int] = None,
                 unitsonorder: Optional[int] = None, reorderlevel: Optional[int] = None,
                 discontinued: Optional[str] = None):
        self.productid = productid
        self.supplierid = supplierid
        self.categoryid = categoryid
        self.productname = productname
        self.quantityperunit = quantityperunit
        self.unitprice = unitprice
        self.unitsinstock = unitsinstock
        self.unitsonorder = unitsonorder
        self.reorderlevel = reorderlevel
        self.discontinued = discontinued
        self.order_details = []


class Shippers:
    def __init__(self, shipperid: int = None, companyname: Optional[str] = None, 
                 phone: Optional[str] = None):
        self.shipperid = shipperid
        self.companyname = companyname
        self.phone = phone


class Suppliers:
    def __init__(self, supplierid: int = None, companyname: Optional[str] = None, 
                 contactname: Optional[str] = None, contacttitle: Optional[str] = None,
                 address: Optional[str] = None, city: Optional[str] = None, 
                 region: Optional[str] = None, postalcode: Optional[str] = None,
                 country: Optional[str] = None, phone: Optional[str] = None,
                 fax: Optional[str] = None, homepage: Optional[str] = None):
        self.supplierid = supplierid
        self.companyname = companyname
        self.contactname = contactname
        self.contacttitle = contacttitle
        self.address = address
        self.city = city
        self.region = region
        self.postalcode = postalcode
        self.country = country
        self.phone = phone
        self.fax = fax
        self.homepage = homepage


class Orders:
    def __init__(self, orderid: int = None, customerid: str = None, employeeid: int = None,
                 orderdate: Optional[datetime.datetime] = None, requireddate: Optional[datetime.datetime] = None,
                 shippeddate: Optional[datetime.datetime] = None, freight: Optional[decimal.Decimal] = None,
                 shipname: Optional[str] = None, shipaddress: Optional[str] = None,
                 shipcity: Optional[str] = None, shipregion: Optional[str] = None,
                 shippostalcode: Optional[str] = None, shipcountry: Optional[str] = None,
                 shipperid: Optional[int] = None):
        self.orderid = orderid
        self.customerid = customerid
        self.employeeid = employeeid
        self.orderdate = orderdate
        self.requireddate = requireddate
        self.shippeddate = shippeddate
        self.freight = freight
        self.shipname = shipname
        self.shipaddress = shipaddress
        self.shipcity = shipcity
        self.shipregion = shipregion
        self.shippostalcode = shippostalcode
        self.shipcountry = shipcountry
        self.shipperid = shipperid
        self.order_details = []
        self.customers = None
        self.employees = None


class OrderDetails:
    def __init__(self, orderid: int = None, productid: int = None, 
                 unitprice: Optional[decimal.Decimal] = None, quantity: Optional[int] = None,
                 discount: Optional[decimal.Decimal] = None):
        self.orderid = orderid
        self.productid = productid
        self.unitprice = unitprice
        self.quantity = quantity
        self.discount = discount
        self.orders = None
        self.products = None
