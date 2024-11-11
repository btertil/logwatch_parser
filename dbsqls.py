# sqls used to drop, creat and re-create of tables and views in logwach_parser database

drop_logwatch_entries_sql = "drop table if exists public.logwatch_entries cascade"
create_logwatch_entries_sql = """
create table if not exists public.logwatch_entries (
    id serial primary key,
    server varchar(32),
    log_date date,
    service varchar(32),
    ip varchar(15),
    comment varchar(250),
    logwatch_file varchar(250),
    entered timestamp default current_timestamp
)
"""

create_views_list = [
    """
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
    """,

    """
    create or replace view public.v_hrankiety_ips as select * from public.logwatch_entries where server = 'hrankiety'
    """,

    """
    create or replace view public.v_backup_ips as select * from public.logwatch_entries where server = 'backup'
    """,

    """
    create or replace view public.v_httpd_ips as select * from public.logwatch_entries where service = 'httpd'
    """,

    "create or replace view public.v_sshd_ips as select * from public.logwatch_entries where service = 'sshd'",

    """
    create or replace view public.v_hrankiety_httpd_ips as
    select
        ip,
        count(*) hrankiety_httpd_actions,
        min(log_date) hrankiety_httpdd_min_date,
        max(log_date) hrankiety_httpd_max_date
    from public.v_hrankiety_ips
    where service = 'httpd'
    group by ip
    order by count(*) desc
    """,

    """
    create or replace view public.v_backup_httpd_ips as
    select
        ip,
        count(*) backup_httpd_actions,
        min(log_date) backup_httpdd_min_date,
        max(log_date) backup_httpd_max_date
    from public.v_backup_ips
    where service = 'httpd'
    group by ip
    order by count(*) desc
    """,

    """
    create or replace view public.v_hrankiety_sshd_ips as
    select
        ip,
        count(*) hrankiety_sshd_actions,
        min(log_date) hrankiety_sshd_min_date,
        max(log_date) hrankiety_sshd_max_date
    from public.v_hrankiety_ips
    where service = 'sshd'
    group by ip
    order by count(*) desc
    """,

    """
    create or replace view public.v_backup_sshd_ips as
    select
        ip,
        count(*) backup_sshd_actions,
        min(log_date) backup_sshd_min_date,
        max(log_date) backup_sshd_max_date
    from public.v_backup_ips
    where service = 'sshd'
    group by ip
    order by count(*) desc
    """,

    """
    create or replace view public.v_only_httpd_ips as
    select *
    from public.v_httpd_ips
    where ip not in (select ip from public.v_sshd_ips)
    """,

    """
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
    """,

    """
    create or replace view public.v_only_sshd_ips as
    select *
    from public.v_sshd_ips
    where ip not in (select ip from public.v_httpd_ips)
    """,

    """
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
    """,
]
