create table if not exists main_user (
	id serial primary key,
	vk_id integer not null,
	sex integer check(sex < 3),
	first_name varchar(40) not null,
	last_name varchar(40) not null,
	status varchar(200)
	);

create table if not exists candidates (
	vk_id integer not null unique,
	sex integer check(sex < 3),
	first_name varchar(40) not null,
	last_name varchar(40) not null,
	candidate_link varchar(100) not null unique,
	main_user_id integer references main_user(id)
	);
	
create table if not exists photos_of_candidates (
	id serial primary key,
	candidate_vk_id integer not null references candidates(vk_id),
	first_photo_likes_count integer not null,
	first_photo_link varchar(1050) not null unique,
	second_photo_likes_count integer not null,
	second_photo_link varchar(1050) not null unique,
	third_photo_likes_count integer not null,
	third_photo_link varchar(1050) not null unique
	);