create table dmca (
  id serial primary key,
  copy_link int references copy_content(id),
  copyright int references product(id),
  created_at text,
  request text default 'No',
  dmca_date text
);



-- insert into dmca (copy_link,copyright,created_at) values(517,14,'2020/06/15');

insert into dmca (copy_link,copyright,created_at) values(569,8,'2020/06/15');
insert into dmca (copy_link,copyright,created_at) values(956,74,'2020/06/15');
insert into dmca (copy_link,copyright,created_at) values(395,35,'2020/06/15');
insert into dmca (copy_link,copyright,created_at) values(98,58,'2020/06/15');
