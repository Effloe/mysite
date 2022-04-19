CREATE TABLE "user" (
	"id" INTEGER NOT NULL,
	"username" TEXT NULL,
	"password" TEXT NULL,
	"email" VARCHAR(100) NULL DEFAULT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE "history" (
	"id" INTEGER NOT NULL,
	"imgname" VARCHAR(30),
	"result" VARCHAR(20),
	"calctime" REAL,
    "create_dt" DATETIME,
	PRIMARY KEY ("id")
);


