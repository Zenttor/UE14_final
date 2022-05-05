create table fim_rules
(
    fim_rule_id integer,
    fim_rule_name varchar(255),
    path varchar(255),
    start_inode integer,
    inode boolean,
    parent boolean,
    name boolean,
    type boolean,
    mode boolean,
    nlink boolean,
    uid boolean,
    gid boolean,
    size boolean,
    atime boolean,
    mtime boolean,
    md5 boolean,
    sha1 boolean,
    ctime boolean,
    primary key(fim_rule_id)
);

create table stat_files
(
    file_inode integer,
    parent_id integer,
    file_name varchar(255),
    file_type text,
    file_mode varchar(255),
    file_nlink integer,
    file_uid integer,
    file_gid integer,
    file_size integer,
    file_atime timestamp,
    file_mtime timestamp,
    file_ctime timestamp,
    file_md5 varchar(255),
    file_SHA1 varchar(255),
    primary key(file_inode)
);

create table ref_images
(
    image_id integer,
    file_inode integer,
    datetime_image timestamp,
    parent_id integer,
    file_name varchar(255),
    file_type text,
    file_mode varchar(255),
    file_nlink integer,
    file_uid integer,
    file_gid integer,
    file_size integer,
    file_atime timestamp,
    file_mtime timestamp,
    file_ctime timestamp,
    file_md5 varchar(255),
    file_SHA1 varchar(255),
    primary key(image_id)
);

create table sa_jobs
(
    sa_job_id integer,
    sa_job_name varchar(255),
    script boolean,
    command_script varchar(255),
    expected_result varchar(255),
    alert_message varchar(255),
    primary key(sa_job_id)
);

create table sa_sets
(
    sa_set_id integer,
    sa_job_id integer,
    sa_set_name varchar(255),
    schedule integer,
    primary key(sa_set_id),
    foreign key(sa_job_id) references sa_jobs(sa_job_id)
);

create table sa_events
(
    sa_event_id integer key autoincrement,
    sa_set_id integer,
    sa_job_id integer,
    datetime_event timestamp,
    except_active boolean,
    primary key(sa_event_id),
    foreign key(sa_set_id) references sa_sets(sa_set_id),
    foreign key (sa_job_id) references sa_jobs(sa_job_id)

);

create table fim_sets
(
    fim_set_id integer,
    fim_rule_id integer,
    fim_set_name varchar(255),
    schedule integer,
    primary key(fim_set_id),
    foreign key(fim_rule_id) references fim_rules(fim_rule_id)
);

create table fim_events
(
    fim_event_id   integer key autoincrement,
    fim_set_id     integer,
    fim_rule_id    integer,
    image_id       integer,
    file_inode     integer,
    datetime_event timestamp,
    except_msg     varchar(255),
    except_active  boolean,
    primary key (fim_event_id),
    foreign key (fim_set_id) references fim_sets(fim_set_id),
    foreign key (fim_rule_id) references fim_rules (fim_rule_id),
    foreign key (image_id) references ref_images (image_id),
    foreign key (file_inode) references stat_files (file_inode)
);