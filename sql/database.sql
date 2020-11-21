-- drop table if exists public.logwatch_entries cascade;


-- create table if not exists public.logwatch_entries (
--     id serial primary key,
--     server varchar(32),
--     log_date date,
--     service varchar(32),
--     ip varchar(15),
--     comment varchar(250),
--     logwatch_file varchar(250)
-- );



-- Weryfikacja po uruchomieniu parsera / quality check
-- ---------------------------------------------------


-- find duplicates

create or replace view public.v_duplicates as
    select
        server,
        log_date,
        service,
        ip,
        logwatch_file,
        count(*) ile
    from public.logwatch_entries
    group by
        server,
        log_date,
        service,
        ip,
        logwatch_file
    having count(*) > 1;

select * from public.v_duplicates;
select count(*) duplicates from public.v_duplicates;

-- przykłądowe rekordy
select * from public.logwatch_entries order by ip limit 30;
select * from public.logwatch_entries order by ip desc limit 30;


-- count and count distinct
select count(*) ile_all  from public.logwatch_entries;

-- id is always unique as it is a primary key
select count(*) ile_distinct from (select distinct server, log_date, service, ip, comment, logwatch_file from public.logwatch_entries) s;

-- spr vs mail
select * from public.logwatch_entries where server = 'backup' and log_date = '2013-12-10';



-- views analityczne
-- -----------------


-- all logs for backup and hrankiety
-- drop view if exists public.v_hrankiety_ips cascade;
create or replace view public.v_hrankiety_ips as select * from public.logwatch_entries where server = 'hrankiety';
select * from public.v_hrankiety_ips limit 20;

-- drop view if exists public.backup_ips cascade;
create or replace view public.v_backup_ips as select * from public.logwatch_entries where server = 'backup';
select * from public.v_backup_ips limit 20;

-- httpd view
-- drop view if exists public.v_httpd_ips;
create or replace view public.v_httpd_ips as select * from public.logwatch_entries where service = 'httpd';
select * from public.v_httpd_ips limit 20;

-- sshd view
-- drop view if exists public.v_sshd_ips;
create or replace view public.v_sshd_ips as select * from public.logwatch_entries where service = 'sshd';
select * from public.v_sshd_ips limit 20;


-- drop view if exists public.v_hrankiety_httpd_ips;
create or replace view public.v_hrankiety_httpd_ips as
    select
        ip,
        count(*) hrankiety_httpd_actions,
        min(log_date) hrankiety_httpdd_min_date,
        max(log_date) hrankiety_httpd_max_date
    from public.v_hrankiety_ips
    where service = 'httpd'
    group by ip
    order by count(*) desc;

select * from public.v_hrankiety_httpd_ips;


-- drop view if exists public.v_backup_httpd_ips;
create or replace view public.v_backup_httpd_ips as
    select
        ip,
        count(*) backup_httpd_actions,
        min(log_date) backup_httpdd_min_date,
        max(log_date) backup_httpd_max_date
    from public.v_backup_ips
    where service = 'httpd'
    group by ip
    order by count(*) desc;

select * from public.v_backup_httpd_ips;


-- drop view if exists public.v_hrankiety_sshd_ips;
create or replace view public.v_hrankiety_sshd_ips as
    select
        ip,
        count(*) hrankiety_sshd_actions,
        min(log_date) hrankiety_sshd_min_date,
        max(log_date) hrankiety_sshd_max_date
    from public.v_hrankiety_ips
    where service = 'sshd'
    group by ip
    order by count(*) desc;

select * from public.v_hrankiety_sshd_ips;


-- drop view if exists public.v_backup_sshd_ips;
create or replace view public.v_backup_sshd_ips as
    select
        ip,
        count(*) backup_sshd_actions,
        min(log_date) backup_sshd_min_date,
        max(log_date) backup_sshd_max_date
    from public.v_backup_ips
    where service = 'sshd'
    group by ip
    order by count(*) desc;

select * from public.v_backup_sshd_ips;


-- only httpd but not sshd
create or replace view public.v_only_httpd_ips as
    select *
    from public.v_httpd_ips
    where ip not in (select ip from public.v_sshd_ips);

select * from public.v_only_httpd_ips limit 10;


create or replace view public.v_agg_only_httpd_ips as
    select
        ip,
        count(*) httpd_probes,
        min(log_date) httpd_probes_min_date,
        max(log_date) httpd_probes_max_date
    from public.v_httpd_ips
    where ip not in (select ip from public.v_sshd_ips)
    group by ip
    order by count(*) desc
;

select * from public.v_agg_only_httpd_ips limit 10;


-- only sshd but not httpd
create or replace view public.v_only_sshd_ips as
    select *
    from public.v_sshd_ips
    where ip not in (select ip from public.v_httpd_ips)
;

select * from public.v_only_sshd_ips limit 10;


create or replace view public.v_agg_only_sshd_ips as
    select
        ip,
        count(*) sshd_logins,
        min(log_date) sshd_logins_min_date,
        max(log_date) sshd_logins_max_date
    from public.v_sshd_ips
    where ip not in (select ip from public.v_httpd_ips)
    group by ip
    order by count(*) desc
;

select * from public.v_agg_only_sshd_ips limit 10;