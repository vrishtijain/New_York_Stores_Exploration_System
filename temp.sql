-- select ls.license_type_code, count(ls.license_type_code)
-- from authorised_liquor_store ls
-- where ls.license_issued_date >= '02/03/2019'
-- and 
-- ls.license_expiration_date <= '04/04/2022'  
-- group by ls.license_type_code 
--  having count (distinct ls.license_expiration_date) >= '10'
-- order by ls.license_type_code; 

-- select rf.entity_name, rf.dba_name, rf.street_number, rf.street_name, rf.city, rf.state, gl.zip
-- from retail_food_stores rf, global_county_zip_code gl
-- where rf.entity_name like '%PHARMACY%' and square_footage >5000 and gl.zip=rf.zip_code

-- 42.735130
-- -73.677150