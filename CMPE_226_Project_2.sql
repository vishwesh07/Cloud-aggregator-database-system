drop database multicloud;
create database multicloud;
use multicloud;

create table csp
( 
  csp_id int not null auto_increment,
  csp_email_id varchar(255)  not null,
  csp_name varchar(255) not null,
  csp_password varchar(255) not null,
  csp_join_date date not null,
  csp_bank_account_number int not null,
  primary key (csp_id)
);
 
create table order_
(
order_id int not null auto_increment,
order_date date not null,
number_of_machines int not null,
# instance_type varchar(255) not null,
ca_id int not null,
customer_id int not null,
bill_id int not null,
gpu_cores int not null,
ram int not null,
disk_size int not null,
order_end_date date not null,
primary key (order_id)
);


create table ca
(
ca_id int not null auto_increment,
ca_email_id varchar(255) not null,
ca_name char(255) not null,
ca_bank_account int not null,
ca_password varchar(255) not null,
primary key(ca_id)
);

create table customer 
(
customer_id int not null auto_increment,
customer_email_id varchar(255) not null,
customer_name char(255) not null,
customer_password varchar(255) not null,
customer_join_date date not null,
customer_bank_account int(16) not null,
customer_offer_id int,
primary key(customer_id)
);

create table bill
(
bill_id int not null auto_increment,
bill_amount int(12) not null,
csp_id int not null,
ca_id int not null,
customer_id int not null,
month int not null,
year int not null,
offer_id int not null,
primary key(bill_id)
);

create table offer
(
offer_id int not null auto_increment,
offer_name varchar(255) not null,
rebate int not null,
ca_id int not null,
primary key(offer_id)
);

create table machine 
(
mac_id int not null auto_increment,
csp_id int not null,
# gpu varchar(20) not null,
disk_size varchar(20) not null,
ram int(4) not null,
gpu_cores int(4) not null,
# os char(20) not null,
ip_address varchar(16) not null,
price int not null,
primary key(mac_id, csp_id)
);

create table receives 
(
csp_id int not null,
order_id int not null,
quantity int not null,
primary key (csp_id,order_id)
);

create table onboards 
(
ca_id int not null,
customer_id int not null,
primary key (ca_id, customer_id)
);

# create table avails 
# (
# offer_id int not null,
# customer_id int not null,
# from_date date not null,
# primary key(offer_id, customer_id)
# );

# create table attached
# (
# bill_id int not null,
# offer_id int not null,
# primary key(bill_id, offer_id)
# );

create table csp_contracts
(
ca_id int not null,
csp_id int not null,
primary key(ca_id,csp_id)
);

alter table order_ add constraint fk_order_ca_id foreign key (ca_id) references ca(ca_id) ;
alter table order_ add constraint fk_order_customer_id foreign key (customer_id) references customer(customer_id);

######alter table bill add csp_id int not null;
######alter table bill add ca_id int not null;
######alter table bill add customer_id int not null;
alter table bill add constraint fk_bill_csp_id foreign key (csp_id) references csp(csp_id);
alter table bill add constraint fk_bill_ca_id foreign key (ca_id) references ca(ca_id);
alter table bill add constraint fk_bill_cust_id foreign key (customer_id ) references customer(customer_id);
alter table bill add constraint fk_bill_offer_id foreign key (offer_id) references offer(offer_id);

alter table machine add constraint fk_machine_csp_id foreign key (csp_id) references csp(csp_id);

alter table receives add constraint fk_receives_csp_id foreign key (csp_id) references csp(csp_id);
alter table receives add constraint fk_receives_order_id foreign key (order_id) references order_(order_id);

alter table onboards add constraint fk_onboards_ca_id foreign key (ca_id) references ca(ca_id);
alter table onboards add constraint fk_onboards_customer_id foreign key (customer_id) references customer(customer_id);


#####alter table order_ add bill_id int not null;
alter table order_ add constraint fk_order_bill_id foreign key (bill_id) references bill(bill_id);
#####alter table order_ add cpu_cores int not null;
#####alter table order_ add ram int not null;
#####alter table order_ add disk_size int not null;
#####alter table order_ add order_end_date date not null;

#####alter table customer add customer_offer_id int;
alter table customer add constraint fk_customer_offer_id foreign key (customer_offer_id)  references offer(offer_id);

######alter table bill add month int not null;
######alter table bill add year int not null;
######alter table bill add offer_id int not null;

######alter table offer add rebate int not null;
######alter table offer add ca_id int not null;
alter table offer add constraint fk_offer_ca_id foreign key (ca_id) references ca(ca_id);

########alter table machine add price int not null;

########alter table receives add quantity int not null;
alter table csp_contracts add constraint fk_csp_contracts_csp_id foreign key (csp_id) references csp(csp_id);
alter table csp_contracts add constraint fk_csp_contracts_ca_id foreign key (ca_id) references ca(ca_id);


###### Ca
insert into ca values(12121,'abah@gmail.com','khas', 132121, 'asas');
insert into ca values(232323,'sds@gmail.com','dsds', 12434121, 'rwers');
insert into ca values(4324323,'fdfds@gmail.com','hgh',5454545, 'dfdfe');


###### Customer
insert into customer values (11224,'Rohit@gmail.com','Rohit',134,'2000-09-09',3434,null);
insert into customer values (11225,'Li@gmail.com','Li',135,'2000-09-19',3434,null);
insert into customer values (11226,'Rakesh@gmail.com','Rakesh',136,'2000-09-29',3434,null);
insert into customer values (11227,'Laxmi@gmail.com','Laxmi',137,'2000-01-09',3434,null);
insert into customer values (11228,'Ravi@gmail.com','Ravi',138,'2000-02-09',3434,null);
insert into customer values (11229,'John@gmail.com','John',139,'2000-03-09',3434,null);
insert into customer values (11220,'Wayne@gmail.com','Wayne',1311,'2000-04-09',3434,null);
insert into customer values (11241,'Kaka@gmail.com','Kaka',1341,'2000-09-05',3434,null);


###### CSP
insert into csp values (1234,'amazon@gmail.com','AWS',134,'2000-09-09',3434);
insert into csp values (1235,'google@gmail.com','Google',135,'2000-08-01',3435);
insert into csp values (1236,'microsoft@gmail.com','Azure',136,'2000-10-10',34346);
insert into csp values (12361,'VMwaret@gmail.com','vCloudAir',137,'2000-10-01',34347);
insert into csp values (12362,'Rackspace@gmail.com','RackConnect',138,'2000-11-10',34348);
insert into csp values (12363,'HPE@gmail.com','Right Mix',139,'2000-10-10',34349);
insert into csp values (12364,'EMC@gmail.com','VCE',1361,'2000-12-10',343461);


##### Machines
#AWS Machines
insert into machine values(1334151,1234,'6TB',16,1,'123.65.254.22',20);
insert into machine values(1334152,1234,'6TB',32,1,'123.65.251.22',145);
insert into machine values(1334153,1234,'6TB',8,2,'123.65.254.32',100);
insert into machine values(1334154,1234,'6TB',4,8,'123.65.254.52',250);
insert into machine values(1334155,1234,'10TB',8,8,'123.65.251.12',450);
insert into machine values(1334156,1234,'100TB',8,16,'123.65.252.12',4500);
insert into machine values(1334157,1234,'100TB',16,16,'123.65.253.12',450000);

#Google
insert into machine values(1234151,1235,'60TB',8,5,'123.65.254.22',545);
insert into machine values(1134151,1235,'16TB',16,5,'123.65.254.32',145);
insert into machine values(13134151,1235,'32TB',8,4,'123.65.254.42',2345);
insert into machine values(134151,1235,'8TB',8,10,'123.65.254.52',450);
insert into machine values(1354151,1235,'16TB',16,10,'123.65.254.62',45000);

#vCloud
insert into machine values(1114151,12361,'6TB',4,8,'121.65.254.12',100);
insert into machine values(1214151,12361,'6TB',8,8,'122.65.254.12',150);
insert into machine values(1314151,12361,'6TB',16,16,'124.65.254.12',250);

#Azure
insert into machine values(1334111,1236,'16TB',8,5,'123.65.254.11',145);
insert into machine values(1334121,1236,'8TB',8,5,'123.65.254.13',245);
insert into machine values(1334131,1236,'4TB',8,5,'123.65.254.12',415);
insert into machine values(1334141,1236,'32TB',8,5,'123.65.254.14',450);
insert into machine values(1334101,1236,'64TB',16,16,'123.65.254.15',4500);

#RackConnect
insert into machine values(1334111,12362,'16TB',8,5,'113.25.254.12',450);
insert into machine values(1334112,12362,'8TB',8,5,'113.26.254.12',100);
insert into machine values(1334113,12362,'16TB',16,5,'113.35.254.12',800);

#Right Mix
insert into machine values(1034151,12363,'16TB',4,5,'120.65.254.12',415);
insert into machine values(1934151,12363,'16TB',8,5,'129.65.254.12',425);
insert into machine values(1834151,12363,'16TB',16,5,'183.65.254.12',435);

#VCE
insert into machine values(1534151,12364,'8TB',8,5,'123.85.254.12',4500);
insert into machine values(1634151,12364,'32TB',16,5,'123.75.254.12',4590);
insert into machine values(1734151,12364,'16TB',16,5,'123.55.254.12',4580);


###### CSP_Contracts
insert into csp_contracts values(12121,1234);
insert into csp_contracts values(12121,1235);
insert into csp_contracts values(12121,12361);
insert into csp_contracts values(12121,12364);

insert into csp_contracts values(232323,1234);
insert into csp_contracts values(232323,1235);
insert into csp_contracts values(232323,1236);
insert into csp_contracts values(232323,12364);

insert into csp_contracts values(4324323,1234);
insert into csp_contracts values(4324323,1235);
insert into csp_contracts values(4324323,1236);
insert into csp_contracts values(4324323,12361);
insert into csp_contracts values(4324323,12362);
insert into csp_contracts values(4324323,12363);
insert into csp_contracts values(4324323,12364);

###### Onboards
insert into onboards values (12121,11224);
insert into onboards values (12121,11225);
insert into onboards values (12121,11220);
insert into onboards values (12121,11241);

insert into onboards values (232323,11224);
insert into onboards values (232323,11225);
insert into onboards values (232323,11226);
insert into onboards values (232323,11227);
insert into onboards values (232323,11228);
insert into onboards values (232323,11229);
insert into onboards values (232323,11220);
insert into onboards values (232323,11241);

insert into onboards values (4324323,11224);
insert into onboards values (4324323,11225);
insert into onboards values (4324323,11226);
insert into onboards values (4324323,11227);
insert into onboards values (4324323,11228);
insert into onboards values (4324323,11229);
insert into onboards values (4324323,11220);
insert into onboards values (4324323,11241);


##### Offer
insert into offer values (4321,'Big Bang Offer',9,12121);
insert into offer values (4322,'Bumpper Offer',11,232323);
insert into offer values (4323,'Super Deal Offer',5,232323);
insert into offer values (4324,'Platinum Offer',20,4324323);
insert into offer values (4325,'Gold Bang Offer',15,4324323);

##### Bill
insert into bill values (0001,5000,1234,12121,11224,'01','2000',4321);
insert into bill values (0002,1000,12361,12121,11227,'01','2000',4323);
insert into bill values (0003,2000,12364,12121,11220,'01','2000',4325);


insert into bill values (1004,3000,1235,232323,11225,'02','2000',4325);
insert into bill values (1005,53000,12362,232323,11228,'03','2000',4321);
insert into bill values (1006,51000,1236,232323,11241,'01','2000',4323);

insert into bill values (2004,4000,1236,4324323,11226,'07','2000',4322);
insert into bill values (2005,43000,12364,4324323,11229,'08','2000',4324);
insert into bill values (2006,41000,1235,4324323,11241,'09','2000',4325);

##### Order
insert into order_ values(0010,'2000-02-01',5,12121,11224,0001,16,16,6,'2000-10-10');
insert into order_ values(0011,'2000-03-01',10,4324323,11227,0002,16,16,6,'2000-10-10');
insert into order_ values(0012,'2000-04-01',4,232323,11226,2004,16,16,10,'2000-10-10');

insert into order_ values(1010,'2000-11-01',5,232323,11225,1004,32,16,100,'2001-10-10');
insert into order_ values(1011,'2000-12-01',5,12121,11228,1005,4,16,16,'2001-10-10');
insert into order_ values(1012,'2000-02-01',5,4324323,11229,2005,8,16,8,'2000-10-10');

insert into order_ values(2011,'2000-01-01',5,12121,11220,0003,8,16,16,'2000-10-10');
insert into order_ values(2012,'2000-11-01',15,4324323,11241,2006,8,16,100,'2001-10-10');
insert into order_ values(2013,'2000-01-01',5,4324323,11229,2005,8,16,100,'2000-10-10');

##### Receives
insert into receives values(1234,0010,5);
insert into receives values(12361,0011,10);
insert into receives values(1236,0012,4);
insert into receives values(1235,1010,5);
insert into receives values(12362,1011,5);
insert into receives values(12364,1012,5);
insert into receives values(12364,2011,5);
insert into receives values(1235,2012,15);
insert into receives values(12364,2013,5);


delimiter $$
create definer=`root`@`localhost` procedure `sp_create_user`(
    in sp_email_id varchar(255),
    in sp_name varchar(255),
    in sp_password varchar(255),
    in sp_join_date date,
    in sp_bank_account_number int,
    in sp_offer_id int
)
begin
    if ( select exists (select 1 from customer where customer_email_id = sp_email_id) ) then
     
        select 'username exists !!';
     
    else
     
        insert into customer
        (
            customer_email_id,
			customer_name,
			customer_password,
			customer_join_date,
			customer_bank_account,
            customer_offer_id
        )
        values
        (
            sp_email_id,
			sp_name,
			sp_password,
			sp_join_date,
			sp_bank_account_number,
            null
        );
     
    end if;
end$$
delimiter ;

delimiter $$
create definer=`root`@`localhost` procedure `sp_create_csp`(
    in c_email_id varchar(200),
    in c_name varchar(200),
    in c_password varchar(200),
    in c_join_date date,
    in c_bank_account_number int
)
begin
    if ( select exists (select 1 from csp where csp_email_id = c_email_id) ) then

        select 'username exists !!';

    else

        insert into csp
        (
            csp_email_id,
			csp_name,
			csp_password,
			csp_join_date,
			csp_bank_account_number
        )
        values
        (
            c_email_id,
			c_name,
			c_password,
			c_join_date,
			c_bank_account_number
        );

    end if;
end$$
delimiter ;
