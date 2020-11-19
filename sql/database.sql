-- drop table if exists public.logwatch_entries;


-- create table if not exists public.logwatch_entries (
--     id serial primary key,
--     server varchar(32),
--     log_date date,
--     service varchar(32),
--     ip varchar(15),
--     comment varchar(250),
--     logwatch_file varchar(250)
-- );

select * from public.logwatch_entries limit 30;

--- insert into public.logwatch_entries (server, log_date, service, ip, comment, logwatch_file) values (
---     "tr", "2020-02-02", "sssds", "192.168.0.1", "test", "żadna tam"
--- );


select count(*) ile_all  from public.logwatch_entries;

select count(*) ile_distinct from (select distinct server, log_date, service, ip, comment, logwatch_file from public.logwatch_entries) s;

select * from public.logwatch_entries where server = 'backup' and log_date = '2013-12-10';


-- views

-- all logs for backup and hrankiety
create view public.hrankiety_ips as select * from public.logwatch_entries where server = 'hrankiety';
create view public.backup_ips as select * from public.logwatch_entries where server = 'backup';

-- httpd view
create view public.httpd_ips as select * from public.logwatch_entries where service = 'httpd';
select ip, count(*) hrankiety_httpd_actions from public.hrankiety_ips where service = 'httpd' group by ip order by count(*) desc;
select ip, count(*) backup_httpd_actions from public.backup_ips where service = 'httpd' group by ip order by count(*) desc;


-- sshd view
create view public.sshd_ips as select * from public.logwatch_entries where service = 'sshd';
select ip, count(*) hrankiety_sshd_actions from public.hrankiety_ips where service = 'sshd' group by ip order by count(*) desc;
select ip, count(*) backup_sshd_actions from public.backup_ips where service = 'sshd' group by ip order by count(*) desc;


-- TODO: min_date, max_date (backup_sshd_min_date, ....)

-- quality check
-- --------------

-- find duplicates
create view public.hrankiety_httpd_ips as select ip,
select
    id,
    server,
    log_date,
    service,
    ip,
    logwatch_file,
    count(*) ile
from public.logwatch_entries
group by
    id,
    server,
    log_date,
    service,
    ip,
    logwatch_file
having count(*) > 1
limit 10;

-- analiza

-- jakie ip mnie testowały
select ip, count(*) ile from public.logwatch_entries where service = 'httpd' group by ip order by count(*) desc;

-- jakie ip się logowały przez ssh
select ip, count(*) ile from public.logwatch_entries where service = 'sshd' group by ip order by count(*) desc;

