use multicloud;

create table Csp
( 
  Csp_id int not null,
  Email_id  varchar(20)  not null,
  Csp_bank_account_number int not null,
  Csp_Name varchar(20) not null,
  Csp_Password varchar(20) not null,
  Primary Key (Csp_id)
  );
 
 create table ORD
(
order_id int not null,
order_date date not null,
number_of_machines int not null,
instance_type varchar(20) not null,
ca_id int not null,
customer_id int not null,
Primary key (order_id),
);

create table CA
(
ca_id int not null,
email_id varchar(20) not null,
ca_name char(20) not null,
ca_bank_account int not null,
ca_password varchar(20) not null,
primary key(ca_id)
);

create table customer 
(
customer_id int not null,
email_id varchar(20) not null,
join_date date not null,
customer_password varchar(20) not null,
customer_name char(20) not null,
customer_bank_account int not null,
primary key(customer_id)
);

create table bill
(
bill_id int not null,
bill_start_date date not null,
bill_end_date date not null,
bill_amount int not null,
primary key(bill_id)
);

create table offer
(
offer_id int not null,
offer_name varchar(20) not null,
primary key(offer_id)
);

create table machine 
(
mac_id int not null,
csp_id int not null,
gpu varchar(20) not null,
disk_size varchar(30) not null,
ram int not null,
gpu_cores int not null,
os char(20) not null,
ip_address int not null,
primary key(mac_id, csp_id)
);

create table receives 
(
csp_id int not null,
order_id int not null,
primary key (csp_id,order_id)
);

create table onboards 
(
ca_id int not null,
customer_id int not null,
primary key (ca_id, customer_id)
);

create table avails 
(
offer_id int not null,
customer_id int not null,
from_date date not null,
primary key(offer_id, customer_id)
);

create table attached
(
bill_id int not null,
offer_id int not null,
primary key(bill_id, offer_id)
);

alter table ORD add constraint FK_ca_id Foreign key (ca_id) references CA(ca_id) ;
alter table ORD add constraint FK_customer_id Foreign key (customer_id) references customer(customer_id);
alter table bill add csp_id int not null;
alter table bill add ca_id int not null;
alter table bill add customer_id int not null;
alter table bill add constraint FK_csp_id Foreign key (csp_id) references Csp(csp_id);
alter table bill add constraint FK_c_id Foreign key (ca_id) references CA(ca_id);
alter table bill add constraint FK_cust_id Foreign key (customer_id ) references customer(customer_id);
alter table machine add constraint FK_cs_id Foreign key (csp_id) references Csp(csp_id);
alter table receives add constraint FK_cspid Foreign Key (csp_id) references Csp(csp_id);
alter table receives add constraint FK_order_id Foreign key (order_id ) references ORD(order_id);
alter table onboards add constraint FK_caid Foreign key (ca_id) references CA(ca_id);
alter table onboards add constraint FK_cust_id Foreign key (customer_id) references customer(customer_id);
alter table avails add constraint FK_offer_id Foreign key (offer_id) references offer(offer_id);
alter table avails add constraint FK_custo_id Foreign key (customer_id ) references customer(customer_id);
alter table attached add constraint FK_bill_id Foreign key (bill_id) references bill(bill_id);
alter table attached add constraint FK_off_id Foreign key(offer_id) references offer(offer_id);
