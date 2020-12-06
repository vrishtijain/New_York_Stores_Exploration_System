select ls.license_type_code, count(ls.license_type_code)
from authorised_liquor_store ls
where ls.license_issued_date >= '02/03/2019'
and 
ls.license_expiration_date <= '04/04/2022'  
group by ls.license_type_code 
 having count (distinct ls.license_expiration_date) >= '10'
order by ls.license_type_code; 