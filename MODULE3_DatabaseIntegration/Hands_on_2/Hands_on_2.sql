-------HANDS ON 2 ----------------
-------DML QUERIES --------------


----- TASK 1 INSERT, UPDATE AND DELETE-----
--16
insert into students (first_name, last_name, email, date_of_birth, department_id,
enrollment_year) values
('cristiano','ronaldo', 'cristiano.ronaldo@college.edu','1975-02-05',1, 2001),
('lionel','messi','lionel.messi@college.edu','1987-06-10',2,2003);

--17
update enrollments set grade='B' where student_id=5 and course_id=1;

--18
delete from enrollments where grade is null;

--19
select count(*) from enrollments;



-------- TASK 2 SINGLE TABLE QUERIES AND FILTERING--------

--20
select * from students s inner join enrollments e on s.student_id=e.student_id where EXTRACT(year from e.enrollment_date)='2022' order by s.last_name ; 

--21
select course_name from courses where credits>3 order by credits desc;
--22
select prof_name from professors where salary between 80000 and 95000;

--23
select first_name, last_name from students where email like '%@college.edu';

--24
select extract(year from enrollment_date) as year, count(student_id) as enroll from enrollments group by extract(year from enrollment_date);




---------  TASK 3- MUTLI-TABLE JOINS

--25
select s.first_name, s.last_name, d.dept_name from students s inner join departments d on s.department_id=d.department_id;

--26
select e.*, concat(s.first_name , ' ', s.last_name) as studname, c.course_name from enrollments e inner join students s on e.student_id=s.student_id inner join courses c on e.course_id=c.course_id;

--27
select concat(s.first_name, ' ',s.last_name) as full_name from students s left join enrollments e on s.student_id=e.student_id where e.student_id IS NULL;

--28
select c.course_name, count(e.course_id) from courses c left join enrollments e on c.course_id=e.course_id group by c.course_name;

--29
select d.dept_name, p.prof_name, p.salary from departments d right join professors p on d.department_id=p.department_id;



-------TASK 4 AGGREGATIONS AND COUNTING -------

--30
select c.course_name, count(e.course_id) as enrollment_count from courses c inner join enrollments e on c.course_id=e.course_id group by c.course_name;

--31
select d.dept_name, round(avg(p.salary),2) from departments d inner join professors p on d.department_id=p.department_id group by d.dept_name;

--32
select dept_name from departments where budget>600000;

--33
select e.grade, count(e.grade) from enrollments e inner join courses c on e.course_id=c.course_id where c.course_code='CS101' group by e.grade;

--34
select d.dept_name from departments d inner join students s on d.department_id=s.department_id inner join enrollments e on s.student_id=e.student_id group by d.dept_name having count(e.student_id)>2;
