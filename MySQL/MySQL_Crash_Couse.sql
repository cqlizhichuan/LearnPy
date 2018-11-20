-- sub querys --
select order_num from orderitems where prod_id = 'TNT2';
select cust_id from orders where order_num in (20005, 20007);

select cust_id 
from orders 
where order_num in(select order_num
                    from orderitems
                    where prod_id = 'TNT2');

select cust_name, cust_contact
from customers
where cust_id in (select cust_id
                    from orders 
                    where order_num in(select order_num
                                        from orderitems
                                        where prod_id = 'TNT2'));

select  cust_name, 
        cust_state,
        (select count(*)
          from orders
          where orders.cust_id = customers.cust_id) as orders
from customers
order by cust_name;

-- join tables --
-- 实际上是将第一个表中的每一行与第二个表中的每一行配对 --
-- 用 where 来作为条件过滤 --
-- 没有where语句，表1的每行将和表2的每行配对 --
-- 而不管逻辑上是否可以陪在一起 --
select vend_name, prod_name, prod_price
from vendors, products
where vendors.vend_id = products.vend_id
order by vend_name, prod_name;

-- 不用where过滤，则直接笛卡尔积 --
-- 结果就是下面的count(*)行 --
select vend_name, prod_name, prod_price
from vendors, products
order by vend_name, prod_name;

select count(*) from vendors, products;

-- 内部联结 --
-- 如果没有on xxx = xxx，求出来也是个笛卡尔积 --
select vend_name, prod_name, prod_price
from vendors inner join products
on vendors.vend_id = products.vend_id;

-- 联结多个表 --
select order_num, prod_name, vend_name, prod_price, quantity
from orderitems, products, vendors
where products.vend_id = vendors.vend_id
    and orderitems.prod_id = products.prod_id
    and order_num = 20005;

-- 高级联结 --
select concat(rtrim(vend_name), '(', rtrim(vend_country), ')')
as vend_title
from vendors
order by vend_name;

-- 查询某供应商提供的其他产品 --
select prod_id, prod_name
from products
where vend_id = (select vend_id
                 from products
                 where prod_id = 'DTNTR');

select p1.prod_id, p1.prod_name
from products as p1, products as p2
where p1.vend_id = p2.vend_id
        and p2.prod_id = 'DTNTR';

select c.*, o.order_num, o.order_date,
        oi.prod_id, oi.quantity, oi.item_price
from customers as c, orders as o, orderitems as oi
where c.cust_id = o.cust_id
    and oi.order_num = o.order_num
    and prod_id = 'FB';

-- 外联结 --
-- 只会查询出有订单的客户 --
select customers.cust_id, orders.order_num
from customers inner join orders
on customers.cust_id = orders.cust_id;

select customers.cust_id, orders.order_num
from customers left outer join orders
on customers.cust_id = orders.cust_id;

select customers.cust_id, orders.order_num
from customers right outer join orders
on customers.cust_id = orders.cust_id;

-- 使用带聚集函数的联结 --
select customers.cust_name,
        customers.cust_id,
        count(orders.order_num) as num_ord
from customers inner join orders
on customers.cust_id = orders.cust_id
group by customers.cust_id;

-- union --
select vend_id, prod_id, prod_price
from products
where prod_price <= 5
union
select vend_id, prod_id, prod_price
from products
where vend_id in (1001, 1002);

-- 上面的union语句其实用or也可以 --
select vend_id, prod_id, prod_price
from products
where prod_price <= 5 or vend_id in (1001, 1002);


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











