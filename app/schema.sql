drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username string not null,
  role_id integer not null
);