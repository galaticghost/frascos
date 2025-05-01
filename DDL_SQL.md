# Tabela de usuários

```sql
-- public.users definition

-- Drop table

-- DROP TABLE public.users;

CREATE TABLE public.users (
	id serial4 NOT NULL,
	email varchar(128) NOT NULL,
	username varchar(64) NOT NULL,
	"password" varchar(256) NOT NULL,
	about_me varchar(150) NULL,
	profile_picture varchar(256) DEFAULT 'd3badb0b2c80449763ef7610bd10915c.jpeg'::character varying NULL,
	last_seen timestamp DEFAULT now() NULL,
	CONSTRAINT users_email_key UNIQUE (email),
	CONSTRAINT users_pkey PRIMARY KEY (id),
	CONSTRAINT users_username_key UNIQUE (username)
);

-- Permissões

ALTER TABLE public.users OWNER TO "admin";
GRANT ALL ON TABLE public.users TO "admin";
GRANT UPDATE, SELECT, INSERT, DELETE ON TABLE public.users TO frascos_db;
```

# Tabela de posts

```sql
-- public.posts definition

-- Drop table

-- DROP TABLE public.posts;

CREATE TABLE public.posts (
	id serial4 NOT NULL,
	body varchar(300) NOT NULL,
	created_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
	user_id int4 NULL,
	CONSTRAINT posts_pkey PRIMARY KEY (id)
);

-- Permissões

ALTER TABLE public.posts OWNER TO "admin";
GRANT ALL ON TABLE public.posts TO "admin";
GRANT UPDATE, SELECT, INSERT, DELETE ON TABLE public.posts TO frascos_db;

-- public.posts chaves estrangeiras

ALTER TABLE public.posts ADD CONSTRAINT posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);

```

# Tabela de seguidores

```sql
-- public.followers definition

-- Drop table

-- DROP TABLE public.followers;

CREATE TABLE public.followers (
	follower_id int4 NULL,
	followed_id int4 NULL
);

-- Permissões

ALTER TABLE public.followers OWNER TO "admin";
GRANT ALL ON TABLE public.followers TO "admin";
GRANT UPDATE, SELECT, INSERT, DELETE ON TABLE public.followers TO frascos_db;


-- public.followers chaves estrangeiras

ALTER TABLE public.followers ADD CONSTRAINT followers_followed_id_fkey FOREIGN KEY (followed_id) REFERENCES public.users(id);
ALTER TABLE public.followers ADD CONSTRAINT followers_follower_id_fkey FOREIGN KEY (follower_id) REFERENCES public.users(id);
```
