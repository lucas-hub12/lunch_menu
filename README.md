# lunch-menu
- [x] 팀원들의 점심메뉴
- [x] 분석
- [ ] 알람(입력하지 않은 사람들에게...) 
- [ ] CSV to DB 

## Start
```bash
$ git branch -r
$ git checkout -t origin/0.4/Refactoring
$  git branch
$ pyenv versions
$ curl -sSL https://pdm-project.org/install-pdm.py | python -
$ pdm venv create
$ source .venv/bin/activate
$ pdm install
```

## Ready 
### Instal DB with docker
- https://hub.docker.com/_/postgres
```bash
$ sudo docker run --name local-postgres \
-e POSTGRES_USER=sunsin \
-e POSTGRES_PASSWORD=mysecretpassword \
-e POSTGRES_DB=sunsindb \
-p 5432:5432 \
-d postgres:15.10
```

### Create Table
- postgres
``` sql
CREATE TABLE public.lunch_menu (
	id serial NOT NULL,
	menu_name text NOT NULL,
	member_name text NOT NULL,
	dt date NOT NULL,
	CONSTRAINT lunch_menu_pk PRIMARY KEY (id)

alter table lunch_menu
add constraint unique_member_dt unique (member_name, dt);

create table member(
	id serial not NULL,
	name text unique not null 
	);
	
	select *from member;
	
	insert into member(name)
	values
	('TOM'),
	('cho'),
	('hyun'),
	('JERRY'),
	('SEO'),
	('jiwon'),
	('jacob'),
	('heejin'),
	('lucas'),
	('nuni');
	
	select *from member;

select json_object_agg(name,id)
	from member;
-- 새로운 컬럼 추가	
alter table lunch_menu 
add column member_id int;
	
select * from lunch_menu limit 1;

-- 기존의 제약조건을 삭제
alter table lunch_menu
drop constraint unique_member_dt;

-- 사용하지 않는 컬럼 삭제
alter table lunch_menu 
drop column member_name;

-- member_id null 값을 허용하지 않도록 설정
-- delete from lunch_menu; 	
alter table lunch_menu
alter column member_id set not null;

-- 새로운 제약조건 추가	
alter table lunch_menu
add constraint unique_memberid_dt unique (member_id, dt);	

-- 멤버 테이블에 기본키를 설정
alter table member
add constraint member_id_pk primary key(id);

--관계 조건 추가
alter table lunch_menu
add constraint menu_member_fk 
    foreign key (member_id)
    references member(id)
;

-- 테스트
select * from member;
select max(id) from member;	--10

insert into lunch_menu(menu_name, member_id, dt)
values('순대국',9,'2025-01-01');

select * from lunch_menu;
```

## Dev
```bash
# DB Check, Start, Stop
$ sudo docker ps -a
$ sudo docker start local-postgres
$ sudo docker stop local-postgres

# Into CONTAINER
$ sudo docker exec -it local-postgres bash

```
- RUN
```bash
# 디비 정보에 맞춰 수정
$ cp env.dummy .env

# 서버시작
$ streamlit run App.py
```

: D
