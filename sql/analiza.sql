
-- analiza

-- jakie ip testowały httpd
select ip, count(*) ile, min(log_date) min_date, max(log_date) max_date from public.logwatch_entries where service = 'httpd' group by ip order by count(*) desc;

-- jakie ip się logowały przez ssh
select ip, count(*) ile, min(log_date) min_date, max(log_date) max_date from public.logwatch_entries where service = 'sshd' group by ip order by count(*) desc;

-- wspólne logowania ssh
select * from public.v_hrankiety_sshd_ips h, public.v_backup_sshd_ips b where b.ip = h.ip;

-- wspólne proby httpd
select * from public.v_hrankiety_httpd_ips h, public.v_backup_httpd_ips b where b.ip = h.ip;


-- ONLY prod sshd ips
select * from public.v_hrankiety_sshd_ips where ip not in (select ip from public.v_backup_sshd_ips);

-- ONLY backup sshd ips
select * from public.v_backup_sshd_ips where ip not in (select ip from public.v_hrankiety_sshd_ips);


-- only ssh
select * from public.v_agg_only_sshd_ips limit 10;

-- only httpd
select * from public.v_agg_only_httpd_ips limit 10;