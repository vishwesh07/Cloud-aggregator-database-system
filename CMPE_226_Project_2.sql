# drop database multicloud;

create database multicloud;

use multicloud;

create table Csp
( 
  Csp_id int not null,
  Email_id  varchar(200)  not null,
  Csp_Name varchar(200) not null,
  Csp_Password varchar(200) not null,
  Csp_Join_Date date not null,
  Csp_bank_account_number int not null,
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
Primary key (order_id)
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
customer_id int not null auto_increment,
email_id varchar(200) not null,
customer_name char(200) not null,
customer_password varchar(200) not null,
join_date date not null,
customer_bank_account int not null,
primary key(customer_id)
);

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN c_email_id varchar(200),
    IN c_name VARCHAR(200),
    IN c_password varchar(200),
    IN c_join_date date,
    IN c_bank_account_number int
)
BEGIN
    if ( select exists (select 1 from customer where email_id = c_email_id) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into customer
        (
            email_id,
			customer_name,
			customer_password,
			join_date,
			customer_bank_account
        )
        values
        (
            c_email_id,
			c_name,
			c_password,
			c_join_date,
			c_bank_account_number
        );
     
    END IF;
END$$
DELIMITER ;

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

create table csp_contracts
(
ca_id int not null,
csp_id int not null,
primary key(ca_id,csp_id)
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


insert into CA values(12121,'abah@gmail.com','khas', 132121, 'asas')
insert into CA values(232323,'sds@gmail.com','dsds', 12434121, 'rwers')
insert into CA values(4324323,'fdfds@gmail.com','hgh',5454545, 'dfdfe')

insert into attached values(232213, 4545345)
insert into attached values(576576, 78478654)
insert into attached values(5435454, 131231132)

insert into avails values(234234, 34324, '2018-09-09')
insert into avails values(34344, 646456, '2017-08-08')
insert into avails values(656546, 7766677, '2016-11-11')

insert into bill values(21321, '2018-09-09' , '2018-11-11', 1000, 2132112, 45345, 5345543)
alter table ORD add bill_id int not null;
alter table ORD add constraint FK_bill_id foreign key (bill_id) references bill(bill_id);
alter table ORD add CPU_cores int not null;
alter table ORD add ram int not null;
alter table ORD add disk_size int not null;
alter table ORD add order_end_date date not null;
alter table customer add offer_id int not null;

alter table customer add constraint FK_offers_id foreign key (offer_id) references offer(offer_id);

alter table bill add month int not null;
alter table bill add year int not null;
alter table bill add offer_id int not null;
alter table bill add constraint FK_offer_i foreign key (offer_id) references offer(offer_id);

alter table offer add rebate int not null;
alter table offer add ca_id int not null;
alter table offer add constraint FK_cas_id foreign key (ca_id) references CA(ca_id);

alter table machine add price int not null;

alter table receives add quantity int not null;
alter table csp_contracts add constraints FK_csp_ca foreign key (csp_id) references Csp(csp_id);


drop table avails;
drop table attached;

alter table machine
drop column os,
drop column gpu;

alter table bill
drop column bill_start_date,
drop column bill_end_date;

alter table ORD 
drop column instance_type;