-- create view and use view--
create view productcustomer as
select cust_name, cust_contact, prod_id
from customers, orders, orderitems
where customers.cust_id = orders.cust_id
    and orderitems.order_num = orders.order_num;
select cust_name, cust_contact
from productcustomer
where prod_id = 'TNT2';

-- create procedure --
delimiter //
create procedure product_pricing()
begin
    select avg(prod_price) from products;
end //
delimiter ;

delimiter //
create procedure product_pricing(
  out pl decimal(8, 2),
  out ph decimal(8, 2),
  out pa decimal(8, 2)
)
begin
  select min(prod_price) into pl from products;
  select max(prod_price) into ph from products;
  select avg(prod_price) into pa from products;
end//
delimiter ;

call product_pricing(@price_low, @price_high, @price_avg);

delimiter //
create procedure order_total(
  in onumber int,
  out ototal decimal(8, 2)
)
begin
  select sum(item_price * quantity)
  from orderitems
  where order_num = onumber
  into ototal;
end //
delimiter ;

call order_total(20005, @total);

delimiter //
create procedure order_total(
  in onumber int,
  in taxable boolean,
  out ototal decimal(8, 2)
)
begin
  declare total decimal(8, 2);
  declare tax_rate int default 6;
  
  select sum(item_price * quantity)
  from orderitems
  where order_num = onumber
  into total;
  
  if taxable then
    select total + (total / 100 * tax_rate) into total;
  end if;
  
  select total into ototal;
end //
delimiter ;

call order_total(20005, 0, @total);
select @total;

-- cursor --


delimiter //
create procedure process_orders()
begin
    
    -- declare local variables
    declare done boolean default 0;
    declare o int;
    declare t decimal(8, 2);
    
    -- declare the cursor
    declare order_numbers cursor
    for 
    select order_num from orders;
    
    -- declare continue handler
    declare continue handler for sqlstate '02000' set done = 1;
    
    create table if not exists order_totals
    (order_num int, total decimal(8, 2));
    
    -- open the cursor
    open order_numbers;
    
    -- loop through all rows
    repeat
        fetch order_numbers into o;
        call order_total(o, 1, t);
        insert into order_totals(order_num, total)
        values (o, t);
    until done end repeat;
    
    -- close the cursor
    close order_numbers;
end //
delimiter ;

-- trigger --

-- Will got 'Not allowed to return a result set from a trigger'
create trigger new_product after insert on products
for each row select 'Product added';

drop trigger new_product;

create trigger neworder after insert on orders
for each row select NEW.order_num;











