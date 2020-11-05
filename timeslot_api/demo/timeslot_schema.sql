CREATE TABLE timeslots ( 
id integer primary key,
dentist_name varchar2(30) NOT NULL,
patient_name varchar2(50),
day_of_week  varchar2(100) NOT NULL,
time_of_day  varchar2(100) NOT NULL,
date_appt varchar2(100) NOT NULL
);

-- mon to sunday (by spec: "everyday"), 9 to 5 