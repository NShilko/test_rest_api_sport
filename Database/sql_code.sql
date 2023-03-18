-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS pereval_id_seq;

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS pereval_areas_id_seq;

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS pereval_added_id_seq;

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS spr_activities_id_seq;


-- Table Definition for Users
CREATE TABLE "public"."users" (
"email" text NOT NULL,
"password" text NOT NULL,
PRIMARY KEY ("email")
);

-- Table Definition for PerevalAdded
CREATE TABLE "public"."pereval_added" (
"id" int4 NOT NULL DEFAULT nextval('pereval_id_seq'::regclass),
"user_email" text NOT NULL,
"date_added" timestamp NOT NULL DEFAULT now(),
"beauty_title" text,
"title" text,
"other_titles" text,
"level_summer" smallserial,
"level_autumn" smallserial,
"level_winter" smallserial,
"level_spring" smallserial,
"connect" text,
"add_time" timestamp,
"status" text NOT NULL DEFAULT 'new',
"coord_id" int8 NOT NULL,
PRIMARY KEY ("id"),
CONSTRAINT "pereval_added_user_email_fkey" FOREIGN KEY ("user_email") REFERENCES "public"."users"("email") ON DELETE CASCADE ON UPDATE CASCADE
);

-- Table Definition for Coords
CREATE TABLE "public"."coords" (
"id" int8 NOT NULL DEFAULT nextval('pereval_areas_id_seq'::regclass),
"latitude" float8 NOT NULL,
"longitude" float8 NOT NULL,
"height" int4 NOT NULL,
PRIMARY KEY ("id")
);

-- Table Definition for PerevalImages
CREATE TABLE "public"."pereval_images" (
"id" int4 NOT NULL DEFAULT nextval('pereval_added_id_seq'::regclass),
"pereval_id" int4 NOT NULL,
"img" bytea NOT NULL,
PRIMARY KEY ("id"),
CONSTRAINT "pereval_images_pereval_id_fkey" FOREIGN KEY ("pereval_id") REFERENCES "public"."pereval_added"("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- Table Definition for SprActivitiesTypes
CREATE TABLE "public"."spr_activities_types" (
"id" int4 NOT NULL DEFAULT nextval('spr_activities_id_seq'::regclass),
"title" text,
PRIMARY KEY ("id")
);

-- Table Definition for PerevalAreas
CREATE TABLE "public"."pereval_areas" (
"id" int8 NOT NULL DEFAULT nextval('pereval_areas_id_seq'::regclass),
"id_parent" int8 NOT NULL,
"title" text,
PRIMARY KEY ("id")
);

-- Add Unique Constraint for Email
ALTER TABLE "public"."users" ADD CONSTRAINT "users_email_key" UNIQUE ("email");

-- Add Unique Constraint for Coord
ALTER TABLE "public"."coords" ADD CONSTRAINT "coords_latitude_longitude_height_key" UNIQUE ("latitude", "longitude", "height");

-- Add Foreign Key Constraint for Coord ID
ALTER TABLE "public"."pereval_added" ADD CONSTRAINT "pereval_added_coord_id_fkey" FOREIGN KEY ("coord_id") REFERENCES "public"."coords"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- Create Indexes
CREATE INDEX "pereval_areas_id_parent_idx" ON "public"."pereval_areas" USING btree ("id_parent");
CREATE INDEX "pereval_images_pereval_id_idx" ON "public"."pereval_images" USING btree ("pereval_id");
CREATE INDEX "pereval_added_coord_id_idx" ON "public"."pereval_added" USING btree ("coord_id");