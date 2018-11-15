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
