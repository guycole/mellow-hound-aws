--
-- mysql -u root < mysql_create.sql
--
create database mellow_hound_v1;
--
-- create user 'gsc' identified by 'bogus';
--
-- use mysql;
-- update user set password = PASSWORD('fresh') where User='gsc';
--
-- create user 'mellow' identified by 'bogus';
grant all on mellow_hound_v1.* to 'mellow';
--
create user 'hound' identified by 'bogus';
grant select,insert,update on mellow_hound_v1.* to 'hound';
--
