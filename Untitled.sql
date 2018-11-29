SET SQL_SAFE_UPDATES=0;
select * from customer where customer_password="pbkdf2:sha256:50000$vBkdHuQO$6cdeda905af69fe77036db7ac9ee229e5674036f60d1eed6f04adba423c84cdc" and email_id="c@c.com";
select * from customer where email_id="c@c.com" and customer_password="pbkdf2:sha256:50000$M6136T89$1b524f1fc1cf1a433bd588eb4c23385d07c0cfa07f27462df5abdbf3d08b5303";
update customer set customer_password="pbkdf2:sha256:50000$PJ8gdds4$21c76a7ebbe9fd90740db011db11d1945c9806ff5b312a49ee362f9cc423416e";
delete from customer where email_id="c@c.com";
select * from customer;
select * from csp;
select * from ca;
select * from order_;
select * from bill;
select * from machine;
select * from order_ where customer_id="11242";
update machine set customer_id="11242" where customer_id is NULL  order by price limit 1;
insert into csp
        (
			csp_id,
            email_id,
			csp_name,
			csp_password,
			csp_join_date,
			csp_bank_account_number
        )
        values
        (
			1,
            "a@a.com",
			"aws",
			"aws",
			"2018-02-02",
			"1234"
        );
insert into ca
        (
			ca_id,
            email_id,
			ca_name,
			ca_password,
			ca_bank_account
        )
        values
        (
			1,
            "a@a.com",
			"multicloud",
			"multicloud",
			"1234"
        );
insert into offer
        (
			offer_id,
			offer_name,
			rebate,
			ca_id
        )
        values
        (
			1,
			"offer1",
			"20",
			"1"
        );
insert into customer
        (
			customer_id,
            email_id,
			customer_name,
			customer_password,
			join_date,
			customer_bank_account,
            offer_id
        )
        values
        (
			1,
            "c@c.com",
			"maulik",
			"maulik",
			"2018-02-02",
			"1234",
            "1"
        );
insert into order_
        (
			order_id,
            order_date,
			number_of_machines,
			ca_id,
			customer_id,
            bill_id,
            cpu_cores,
            ram,
            disk_size,
            order_end_date
        )
        values
        (
			"1332",
			"2018-02-02",
            "20",
            "12121",
			"11242", "1", "4", "2", "256", "2018-02-10"
        );
        
select * from bill;
select * from bill where customer_id="11242";
insert into bill values (122,3000,1235,232323,11242,'04','2018',4325);
insert into order_ values(23,'2000-02-01',5,12121,11242,0001,16,16,6,null);

UPDATE mysql.user SET Password=PASSWORD('MyNewPass') WHERE User='root'; 
FLUSH PRIVILEGES;

delimiter $$
DROP PROCEDURE IF EXISTS sp_create_order;
	create definer=`root`@`localhost` procedure `sp_create_order`(
		in sp_email_id varchar(255),
		in sp_ram int,
		in sp_cpu int,
		in sp_disk_size int,
		in sp_no_of_machines int,
		in sp_customer_id int
	)
	begin
	if ( (select count(*) from machine where customer_id is null) > sp_no_of_machines ) then

	select (select count(*) from machine where customer_id is null);

	else

	select 'Not enough resources available!!';

	end if;
	end$$
delimiter ;