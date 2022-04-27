USE dbms_mini_project;


-- drop table Company;
-- drop table Models;
-- drop table Employee;
-- drop table Bug_Track;


-- Company table
CREATE TABLE Company(
    company_id VARCHAR(10),
    company_name VARCHAR(40),
    company_email VARCHAR(30),
    employee_count int,
    password_comp VARCHAR(30), 
    primary key(company_id)
);

insert into Company values("C-00000001","Microsoft","admin@microsoft.com",0);

update Company set employee_count = employee_count+1 where company_id = "C-00000001";

select * from Company;

-- Models table
CREATE TABLE Models(
    model_id VARCHAR(10),
    model_name VARCHAR(40),
    company_id VARCHAR(10),
    bug_count int,
    primary key(model_id),
    foreign key (company_id) references Company(company_id)
);

insert into Models values("M-00000001","Azure","C-00000001",0);

-- update Models set bug_count = bug_count+1 where model_id="M-00000001";

select * from Models;

-- employee table
CREATE TABLE Employee(
    employee_id VARCHAR(10),
    employee_email VARCHAR(30),
    company_id VARCHAR(10),
    pass VARCHAR(40),
    primary key(employee_id),
    foreign key(company_id) references Company(company_id)
);

insert into Employee values("E-00000001","Onkar","onkar@microsoft.com","C-00000001");

select * from Employee;

-- Bug track
CREATE TABLE Bug_Track(
    bug_id VARCHAR(10),
    bug_steps VARCHAR(300),
    bug_link VARCHAR(100),
    bug_status VARCHAR(20),
    company_id VARCHAR(10),
    employee_id VARCHAR(10),
    model_id VARCHAR(10),
    primary key(bug_id),
    foreign key(company_id) references Company(company_id),
    foreign key(employee_id) references Employee(employee_id),
    foreign key(model_id) references Models(model_id)
);

insert into Bug_Track values("B-00000001","1) Open website and navigate to model 2) Click on start now button","www.google.com","Open","C-00000001","E-00000001","M-00000001");

select * from Bug_Track;
