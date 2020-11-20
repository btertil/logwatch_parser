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


-- Weryfikacja po uruchomieniu parsera
______________________________________


-- przykłądowe rekordy
select * from public.logwatch_entries limit 30;

-- count and count distinct
select count(*) ile_all  from public.logwatch_entries;

-- id is always unique as it is a primary key
select count(*) ile_distinct from (select distinct server, log_date, service, ip, comment, logwatch_file from public.logwatch_entries) s;

-- spr vs mail
select * from public.logwatch_entries where server = 'backup' and log_date = '2013-12-10';


-- views analityczne

-- TODO: zmienić nazyw widoków na v_*
-- TODO: stare widoki dropnąć cascade
-- TODO: stworzyć nowe widoki z nazwami w konwencji: v_server_service
-- TODO: sformatować create view
-- TODO: dodać drop if exists wcześniej
-- TODO: oddzielnie analiza.sql a oddzielnie database.sql

-- all logs for backup and hrankiety
-- create view public.hrankiety_ips as select * from public.logwatch_entries where server = 'hrankiety';
-- create view public.backup_ips as select * from public.logwatch_entries where server = 'backup';

-- httpd view
-- create view public.httpd_ips as select * from public.logwatch_entries where service = 'httpd';
select ip, count(*) hrankiety_httpd_actions, min(log_date) hrankiety_httpd_min_date, max(log_date) hrankiety_httpd_max_date from public.hrankiety_ips where service = 'httpd' group by ip order by count(*) desc;
select ip, count(*) backup_httpd_actions, min(log_date) hrankiety_httpd_min_date, max(log_date) hrankiety_httpd_max_date from public.backup_ips where service = 'httpd' group by ip order by count(*) desc;


-- sshd view
-- create view public.sshd_ips as select * from public.logwatch_entries where service = 'sshd';
select ip, count(*) hrankiety_sshd_actions, min(log_date) hrankiety_sshd_min_date, max(log_date) hrankiety_sshd_max_date from public.hrankiety_ips where service = 'sshd' group by ip order by count(*) desc;
select ip, count(*) backup_sshd_actions, min(log_date) backup_sshd_min_date, max(log_date) backup_sshd_max_date from public.backup_ips where service = 'sshd' group by ip order by count(*) desc;


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

-- jakie ip testowały httpd
select ip, count(*) ile, min(log_date) min_date, max(log_date) max_date from public.logwatch_entries where service = 'httpd' group by ip order by count(*) desc;

-- jakie ip się logowały przez ssh
select ip, count(*) ile, min(log_date) min_date, max(log_date) max_date from public.logwatch_entries where service = 'sshd' group by ip order by count(*) desc;

