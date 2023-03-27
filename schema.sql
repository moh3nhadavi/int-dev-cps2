-- create table if not exists room_status(
--     id integer primary key autoincrement,
--     name text not null,
--     value text not null
-- );

-- create table if not exists rules(
--   id integer primary key autoincrement ,
--   conditions text not null,
--   action text not null
-- );

-- create table if not exists stores(
--     id integer primary key autoincrement,
--     value text not null,
--     period text not null,
--     path text not null
-- );

create table if not exists services
(
    id       integer primary key autoincrement,
    name     text not null,
    icon_url text
);

create table if not exists devices
(
    id         integer primary key autoincrement,
    service_id integer not null,
    name       text    not null,
    ip         text    not null,
    foreign key (service_id) references services (id)
);

create table if not exists conditions
(
    id           integer primary key autoincrement,
    service_id   integer not null,
    name         text    not null,
    type         text    not null,
    endpoint     text,
    request_type text,
    foreign key (service_id) references services (id)
);

create table if not exists actions
(
    id           integer primary key autoincrement,
    service_id   integer not null,
    name         text    not null,
    endpoint     text,
    request_type text,
    foreign key (service_id) references services (id)
);

create table if not exists rules
(
    id                   integer primary key autoincrement,
    action_id            integer not null,
    condition_id         integer not null,
    action_device_id     integer not null,
    condition_device_id  integer not null,
    condition_value      text    not null,
    condition_type_value text,
    foreign key (action_id) references actions (id),
    foreign key (condition_id) references conditions (id),
    foreign key (action_device_id) references devices (id),
    foreign key (condition_device_id) references devices (id)
);