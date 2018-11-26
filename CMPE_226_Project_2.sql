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
primary key(customer_id)
);

create table bill
(
bill_id int not null auto_increment,
# bill_start_date date not null,
# bill_end_date date not null,
bill_amount int(12) not null,
primary key(bill_id)
);

create table offer
(
offer_id int not null auto_increment,
offer_name varchar(255) not null,
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
alter table bill add csp_id int not null;
alter table bill add ca_id int not null;
alter table bill add customer_id int not null;
alter table bill add constraint fk_bill_csp_id foreign key (csp_id) references csp(csp_id);
alter table bill add constraint fk_bill_ca_id foreign key (ca_id) references ca(ca_id);
alter table bill add constraint fk_bill_cust_id foreign key (customer_id ) references customer(customer_id);
alter table machine add constraint fk_machine_csp_id foreign key (csp_id) references csp(csp_id);
alter table receives add constraint fk_receives_csp_id foreign key (csp_id) references csp(csp_id);
alter table receives add constraint fk_receives_order_id foreign key (order_id) references order_(order_id);
alter table onboards add constraint fk_onboards_ca_id foreign key (ca_id) references ca(ca_id);
alter table onboards add constraint fk_onboards_customer_id foreign key (customer_id) references customer(customer_id);
# alter table avails add constraint fk_avails_offer_id foreign key (offer_id) references offer(offer_id);
# alter table avails add constraint fk_avails_customer_id foreign key (customer_id) references customer(customer_id);
# alter table attached add constraint fk_attached_bill_id foreign key (bill_id) references bill(bill_id);
# alter table attached add constraint fk_attached_offer_id foreign key (offer_id) references offer(offer_id);

alter table order_ add bill_id int not null;
alter table order_ add constraint fk_order_bill_id foreign key (bill_id) references bill(bill_id);
alter table order_ add cpu_cores int not null;
alter table order_ add ram int not null;
alter table order_ add disk_size int not null;
alter table order_ add order_end_date date not null;

alter table customer add customer_offer_id int;
alter table customer add constraint fk_customer_offer_id foreign key (customer_offer_id)  references offer(offer_id);

alter table bill add month int not null;
alter table bill add year int not null;
alter table bill add offer_id int not null;
alter table bill add constraint fk_bill_offer_id foreign key (offer_id) references offer(offer_id);

alter table offer add rebate int not null;
alter table offer add ca_id int not null;
alter table offer add constraint fk_offer_ca_id foreign key (ca_id) references ca(ca_id);

alter table machine add price int not null;

alter table receives add quantity int not null;
alter table csp_contracts add constraint fk_csp_contracts_csp_id foreign key (csp_id) references csp(csp_id);

# drop table avails;
# drop table attached;

# alter table machine
# drop column os,
# drop column gpu;

# alter table bill
# drop column bill_start_date,
# drop column bill_end_date;

# alter table order_ 
# drop column instance_type;

insert into ca values(12121,'abah@gmail.com','khas', 132121, 'asas');
insert into ca values(232323,'sds@gmail.com','dsds', 12434121, 'rwers');
insert into ca values(4324323,'fdfds@gmail.com','hgh',5454545, 'dfdfe');

# insert into attached values(232213, 4545345);
# insert into attached values(576576, 78478654);
# insert into attached values(5435454, 131231132);

# insert into avails values(234234, 34324, '2018-09-09');
# insert into avails values(34344, 646456, '2017-08-08');
# insert into avails values(656546, 7766677, '2016-11-11');

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
