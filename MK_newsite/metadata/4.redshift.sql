DROP TABLE IF EXISTS ods.stgomnituresiteprehit;
DROP TABLE IF EXISTS ods.fctomnituresiteprehit;
DROP TABLE IF EXISTS ods.stgomnituresiteprelookupvalue;
DROP TABLE IF EXISTS dw.dimomnituresiteprelookupvalue;
DROP TABLE IF EXISTS ods.stgomnituresiteprevisit;
DROP TABLE IF EXISTS dw.fctomnituresiteprevisit;
DROP TABLE IF EXISTS dw.fctomnituresiteprepageview;
DROP TABLE IF EXISTS dw.fctomnituresiteprevisitor;
DROP TABLE IF EXISTS ods.stgomnituresitepreevent;
DROP TABLE IF EXISTS dw.fctomnituresitepreevent;
DROP TABLE IF EXISTS ods.fctomnituresiteprehitarchive;
DROP TABLE IF EXISTS dw.fctomnituresiteprepageviewarchive;
DROP TABLE IF EXISTS dw.fctomnituresiteprevisitarchive;
DROP TABLE IF EXISTS dw.fctomnituresitepreeventarchive;


CREATE TABLE ods.stgomnituresiteprehit
(
	hitkey VARCHAR(255) ENCODE zstd,
	visitkey VARCHAR(70) ENCODE zstd DISTKEY,
	visitorkey VARCHAR(60) ENCODE zstd,
	monthkey INTEGER ENCODE zstd,
	datekey INTEGER ENCODE zstd,
	hourkey INTEGER ENCODE zstd,
	accept_language VARCHAR(22) ENCODE zstd,
	browser BIGINT ENCODE zstd,
	color INTEGER ENCODE zstd,
	connection_type INTEGER ENCODE zstd,
	country INTEGER ENCODE zstd,
	curr_factor INTEGER ENCODE zstd,
	curr_rate REAL ENCODE runlength,
	daily_visitor INTEGER ENCODE zstd,
	date_time TIMESTAMP ENCODE zstd,
	domain VARCHAR(60) ENCODE zstd,
evarcolumns
	exclude_hit INTEGER ENCODE zstd,
	first_hit_page_url VARCHAR(255) ENCODE zstd,
	first_hit_pagename VARCHAR(255) ENCODE zstd,
	first_hit_referrer VARCHAR(255) ENCODE zstd,
	first_hit_time_gmt INTEGER ENCODE zstd,
	geo_city VARCHAR(60) ENCODE zstd,
	geo_country VARCHAR(60) ENCODE zstd,
	geo_region VARCHAR(60) ENCODE zstd,
	geo_zip VARCHAR(60) ENCODE zstd,
	hier1 VARCHAR(255) ENCODE zstd,
	hit_source INTEGER ENCODE zstd,
	hit_time_gmt INTEGER ENCODE delta,
	hitid_high BIGINT ENCODE zstd,
	hitid_low BIGINT ENCODE zstd,
	homepage VARCHAR(255) ENCODE zstd,
	hourly_visitor INTEGER ENCODE zstd,
	ip VARCHAR(100) ENCODE zstd,
	language INTEGER ENCODE zstd,
	last_hit_time_gmt INTEGER ENCODE delta,
	mobile_id INTEGER ENCODE zstd,
	monthly_visitor INTEGER ENCODE zstd,
	new_visit INTEGER ENCODE zstd,
	os BIGINT ENCODE bytedict,
	page_event_var1 VARCHAR(500) ENCODE zstd,
	browser_height INTEGER ENCODE zstd,
	browser_width BIGINT ENCODE zstd,
	channel VARCHAR(255) ENCODE zstd,
	cookies VARCHAR(255) ENCODE zstd,
	currency VARCHAR(255) ENCODE zstd,
	cust_hit_time_gmt INTEGER ENCODE delta,
	cust_visid VARCHAR(255) ENCODE zstd,
	event_list VARCHAR(255) ENCODE zstd,
	java_enabled VARCHAR(255) ENCODE zstd,
	mobileaction VARCHAR(255) ENCODE zstd,
	mobileappid VARCHAR(255) ENCODE zstd,
	mobiledayofweek VARCHAR(255) ENCODE zstd,
	mobiledayssincefirstuse VARCHAR(255) ENCODE zstd,
	mobiledayssincelastuse VARCHAR(255) ENCODE zstd,
	mobiledevice VARCHAR(255) ENCODE zstd,
	mobilehourofday VARCHAR(255) ENCODE zstd,
	mobileinstalldate VARCHAR(255) ENCODE zstd,
	mobilelaunchnumber VARCHAR(255) ENCODE zstd,
	mobileosversion VARCHAR(255) ENCODE zstd,
	mobileresolution VARCHAR(255) ENCODE zstd,
	page_event INTEGER ENCODE zstd,
	page_event_var2 VARCHAR(130) ENCODE zstd,
	page_url VARCHAR(255) ENCODE zstd,
	pagename VARCHAR(255) ENCODE zstd,
	pagename_no_url VARCHAR(130) ENCODE zstd,
	persistent_cookie VARCHAR(255) ENCODE zstd,
	product_list VARCHAR(255) ENCODE zstd,
	referrer VARCHAR(255) ENCODE zstd,
	t_time_info VARCHAR(255) ENCODE zstd,
	visid_high VARCHAR(25) ENCODE zstd,
	visid_low VARCHAR(25) ENCODE zstd,
	visid_type BIGINT ENCODE zstd,
propcolumns
	quarterly_visitor BIGINT ENCODE zstd,
	ref_domain VARCHAR(255) ENCODE zstd,
	ref_type INTEGER ENCODE zstd,
	resolution INTEGER ENCODE zstd,
	username VARCHAR(255) ENCODE zstd,
	visid_new VARCHAR(255) ENCODE zstd,
	visid_timestamp BIGINT ENCODE zstd,
	visit_num BIGINT ENCODE bytedict,
	visit_page_num BIGINT ENCODE bytedict,
	visit_referrer VARCHAR(255) ENCODE zstd,
	visit_search_engine VARCHAR(255) ENCODE zstd,
	visit_start_page_url VARCHAR(255) ENCODE zstd,
	visit_start_pagename VARCHAR(130) ENCODE zstd,
	visit_start_time_gmt BIGINT ENCODE zstd,
	weekly_visitor INTEGER ENCODE zstd,
	yearly_visitor INTEGER ENCODE zstd
)
SORTKEY
(
	monthkey,
	datekey,
	hitkey,
	visitkey
);




CREATE TABLE ods.fctomnituresiteprehit
(
	hitkey VARCHAR(255) ENCODE zstd,
	visitkey VARCHAR(70) ENCODE zstd DISTKEY,
	visitorkey VARCHAR(60) ENCODE zstd,
	monthkey INTEGER ENCODE zstd,
	datekey INTEGER ENCODE zstd,
	hourkey INTEGER ENCODE zstd,
	accept_language VARCHAR(22) ENCODE zstd,
	browser BIGINT ENCODE zstd,
	color INTEGER ENCODE zstd,
	connection_type INTEGER ENCODE zstd,
	country INTEGER ENCODE zstd,
	curr_factor INTEGER ENCODE zstd,
	curr_rate REAL ENCODE runlength,
	daily_visitor INTEGER ENCODE zstd,
	date_time TIMESTAMP ENCODE zstd,
	domain VARCHAR(60) ENCODE zstd,
evarcolumns
	exclude_hit INTEGER ENCODE zstd,
	first_hit_page_url VARCHAR(255) ENCODE zstd,
	first_hit_pagename VARCHAR(255) ENCODE zstd,
	first_hit_referrer VARCHAR(255) ENCODE zstd,
	first_hit_time_gmt INTEGER ENCODE zstd,
	geo_city VARCHAR(60) ENCODE zstd,
	geo_country VARCHAR(60) ENCODE zstd,
	geo_region VARCHAR(60) ENCODE zstd,
	geo_zip VARCHAR(60) ENCODE zstd,
	hier1 VARCHAR(255) ENCODE zstd,
	hit_source INTEGER ENCODE zstd,
	hit_time_gmt INTEGER ENCODE delta,
	hitid_high BIGINT ENCODE zstd,
	hitid_low BIGINT ENCODE zstd,
	homepage VARCHAR(255) ENCODE zstd,
	hourly_visitor INTEGER ENCODE zstd,
	ip VARCHAR(100) ENCODE zstd,
	language INTEGER ENCODE zstd,
	last_hit_time_gmt INTEGER ENCODE delta,
	mobile_id INTEGER ENCODE zstd,
	monthly_visitor INTEGER ENCODE zstd,
	new_visit INTEGER ENCODE zstd,
	os BIGINT ENCODE bytedict,
	page_event_var1 VARCHAR(500) ENCODE zstd,
	browser_height INTEGER ENCODE zstd,
	browser_width BIGINT ENCODE zstd,
	channel VARCHAR(255) ENCODE zstd,
	cookies VARCHAR(255) ENCODE zstd,
	currency VARCHAR(255) ENCODE zstd,
	cust_hit_time_gmt INTEGER ENCODE delta,
	cust_visid VARCHAR(255) ENCODE zstd,
	event_list VARCHAR(255) ENCODE zstd,
	java_enabled VARCHAR(255) ENCODE zstd,
	mobileaction VARCHAR(255) ENCODE zstd,
	mobileappid VARCHAR(255) ENCODE zstd,
	mobiledayofweek VARCHAR(255) ENCODE zstd,
	mobiledayssincefirstuse VARCHAR(255) ENCODE zstd,
	mobiledayssincelastuse VARCHAR(255) ENCODE zstd,
	mobiledevice VARCHAR(255) ENCODE zstd,
	mobilehourofday VARCHAR(255) ENCODE zstd,
	mobileinstalldate VARCHAR(255) ENCODE zstd,
	mobilelaunchnumber VARCHAR(255) ENCODE zstd,
	mobileosversion VARCHAR(255) ENCODE zstd,
	mobileresolution VARCHAR(255) ENCODE zstd,
	page_event INTEGER ENCODE zstd,
	page_event_var2 VARCHAR(130) ENCODE zstd,
	page_url VARCHAR(255) ENCODE zstd,
	pagename VARCHAR(255) ENCODE zstd,
	pagename_no_url VARCHAR(130) ENCODE zstd,
	persistent_cookie VARCHAR(255) ENCODE zstd,
	product_list VARCHAR(255) ENCODE zstd,
	referrer VARCHAR(255) ENCODE zstd,
	t_time_info VARCHAR(255) ENCODE zstd,
	visid_high VARCHAR(25) ENCODE zstd,
	visid_low VARCHAR(25) ENCODE zstd,
	visid_type BIGINT ENCODE zstd,
propcolumns
	quarterly_visitor BIGINT ENCODE zstd,
	ref_domain VARCHAR(255) ENCODE zstd,
	ref_type INTEGER ENCODE zstd,
	resolution INTEGER ENCODE zstd,
	username VARCHAR(255) ENCODE zstd,
	visid_new VARCHAR(255) ENCODE zstd,
	visid_timestamp BIGINT ENCODE zstd,
	visit_num BIGINT ENCODE bytedict,
	visit_page_num BIGINT ENCODE bytedict,
	visit_referrer VARCHAR(255) ENCODE zstd,
	visit_search_engine VARCHAR(255) ENCODE zstd,
	visit_start_page_url VARCHAR(255) ENCODE zstd,
	visit_start_pagename VARCHAR(130) ENCODE zstd,
	visit_start_time_gmt BIGINT ENCODE zstd,
	weekly_visitor INTEGER ENCODE zstd,
	yearly_visitor INTEGER ENCODE zstd,
	inserttime TIMESTAMP DEFAULT getdate() ENCODE delta32k
)
SORTKEY
(
	monthkey,
	datekey,
	hitkey,
	visitkey
);




CREATE TABLE ods.stgomnituresiteprelookupvalue
(
	reportsuiteid VARCHAR(50) ENCODE zstd,
	type VARCHAR(30) ENCODE zstd,
	keyid BIGINT ENCODE zstd,
	keyvalue VARCHAR(255) ENCODE zstd
)
DISTSTYLE ALL
SORTKEY
(
	reportsuiteid,
	type,
	keyid
);


CREATE TABLE dw.dimomnituresiteprelookupvalue
(
	reportsuiteid VARCHAR(50) ENCODE zstd,
	type VARCHAR(30) ENCODE zstd,
	keyid BIGINT ENCODE zstd,
	keyvalue VARCHAR(255) ENCODE zstd
)
DISTSTYLE ALL
SORTKEY
(
	reportsuiteid,
	type,
	keyid
);



CREATE TABLE ods.stgomnituresiteprevisit
(
	hitkey VARCHAR(80) ENCODE zstd,
	visitkey VARCHAR(70) ENCODE zstd DISTKEY,
	visitorkey VARCHAR(60) ENCODE zstd,
	date_time TIMESTAMP ENCODE zstd,
	username VARCHAR(255) ENCODE zstd,
	visit_num BIGINT ENCODE bytedict,
	cust_hit_time_gmt INTEGER ENCODE delta,
	visit_page_num BIGINT ENCODE bytedict,
	ref_type INTEGER ENCODE zstd,
	referrer VARCHAR(255) ENCODE zstd,
	ref_domain VARCHAR(255) ENCODE zstd,
	browser BIGINT ENCODE zstd,
	connection_type INTEGER ENCODE zstd,
	country INTEGER ENCODE zstd,
	language INTEGER ENCODE zstd,
	resolution INTEGER ENCODE zstd,
	color INTEGER ENCODE zstd,
	os BIGINT ENCODE bytedict,
	pagename VARCHAR(255) ENCODE zstd,
	page_event INTEGER ENCODE zstd,
	last_hit_time_gmt INTEGER ENCODE delta,
	channel VARCHAR(255) ENCODE zstd,
propcolumns
	exclude_hit INTEGER ENCODE zstd,
	hit_source INTEGER ENCODE zstd,
	page_url VARCHAR(255) ENCODE zstd
)
SORTKEY
(
	visitorkey,
	hitkey,
	visitkey
);


CREATE TABLE dw.fctomnituresiteprevisit
(
	visitkey VARCHAR(70) ENCODE zstd DISTKEY,
	visitorkey VARCHAR(60) ENCODE zstd,
	monthkey INTEGER ENCODE zstd,
	datekey INTEGER ENCODE zstd,
	hourkey INTEGER ENCODE zstd,
	reportsuiteid VARCHAR(50) ENCODE zstd,
	datetime TIMESTAMP ENCODE zstd,
	visitnum INTEGER ENCODE zstd,
	spenttime INTEGER ENCODE zstd,
	pathlength INTEGER ENCODE zstd,
	entrypage VARCHAR(255) ENCODE zstd,
	exitpage VARCHAR(255) ENCODE zstd,
	reftype INTEGER ENCODE zstd,
	refdomain VARCHAR(255) ENCODE zstd,
	referrer VARCHAR(255) ENCODE zstd,
	browser BIGINT ENCODE zstd,
	connectiontype BIGINT ENCODE zstd,
	country BIGINT ENCODE zstd,
	language BIGINT ENCODE zstd,
	resolution BIGINT ENCODE zstd,
	color BIGINT ENCODE zstd,
	os BIGINT ENCODE zstd,
	inserttime TIMESTAMP DEFAULT getdate() ENCODE zstd
)
SORTKEY
(
	visitkey,
	visitorkey,
	reportsuiteid,
	monthkey,
	datekey,
	hourkey
);



CREATE TABLE dw.fctomnituresiteprepageview
(
	hitkey VARCHAR(80) ENCODE zstd,
	visitkey VARCHAR(70) ENCODE zstd DISTKEY,
	visitorkey VARCHAR(60) ENCODE zstd,
	monthkey INTEGER ENCODE zstd,
	datekey INTEGER ENCODE zstd,
	hourkey INTEGER ENCODE zstd,
	reportsuiteid VARCHAR(50) ENCODE zstd,
	datetime TIMESTAMP ENCODE zstd,
	pagename VARCHAR(100) ENCODE zstd,
	pageurl VARCHAR(255) ENCODE zstd,
	spenttime INTEGER ENCODE zstd,
	visitpageseq INTEGER ENCODE zstd,
	channel VARCHAR(100) ENCODE zstd,
businesscolumns
	contactid BIGINT NOT NULL ENCODE zstd,
	pageevent INTEGER ENCODE zstd,
	islastpv INTEGER ENCODE zstd,
	inserttime TIMESTAMP DEFAULT getdate() ENCODE zstd
)
SORTKEY
(
	hitkey,
	visitkey,
	visitorkey,
	reportsuiteid,
	monthkey,
	datekey,
	hourkey
);



CREATE TABLE dw.fctomnituresiteprevisitor
(
	visitorkey VARCHAR(60) ENCODE zstd DISTKEY,
	reportsuiteid VARCHAR(550) ENCODE zstd,
	visitfirsttime TIMESTAMP ENCODE zstd,
	visitlasttime TIMESTAMP ENCODE zstd,
	cookies VARCHAR(100) ENCODE zstd,
	ip VARCHAR(50) ENCODE zstd,
	mobiledevice VARCHAR(50) ENCODE zstd,
	mobileosversion VARCHAR(50) ENCODE zstd,
	inserttime TIMESTAMP DEFAULT getdate() ENCODE zstd
)
SORTKEY
(
	visitorkey,
	reportsuiteid
);




CREATE TABLE ods.stgomnituresitepreevent
(
	hitkey VARCHAR(80) ENCODE zstd,
	visitkey VARCHAR(70) ENCODE zstd DISTKEY,
	visitorkey VARCHAR(60) ENCODE zstd,
	monthkey INTEGER ENCODE zstd,
	datekey INTEGER ENCODE zstd,
	hourkey INTEGER ENCODE zstd,
	reportsuiteid VARCHAR(50) ENCODE zstd,
	datetime TIMESTAMP ENCODE zstd,
	eventid VARCHAR(100) ENCODE zstd,
	eventvariable VARCHAR(50) ENCODE zstd,
	eventvalue VARCHAR(255) ENCODE zstd,
businesscolumns
	contactid BIGINT ENCODE zstd
)
SORTKEY
(
	visitkey,
	reportsuiteid,
	eventvalue,
	eventid,
	eventvariable
);


CREATE TABLE dw.fctomnituresitepreevent
(
	hitkey VARCHAR(80) ENCODE zstd,
	visitkey VARCHAR(70) ENCODE zstd DISTKEY,
	visitorkey VARCHAR(60) ENCODE zstd,
	monthkey INTEGER ENCODE zstd,
	datekey INTEGER ENCODE zstd,
	hourkey INTEGER ENCODE zstd,
	reportsuiteid VARCHAR(50) ENCODE zstd,
	datetime TIMESTAMP ENCODE zstd,
	eventid VARCHAR(100) ENCODE zstd,
	eventvariable VARCHAR(50) ENCODE zstd,
	eventvalue VARCHAR(255) ENCODE zstd,
businesscolumns
	contactid BIGINT ENCODE zstd,
	inserttime TIMESTAMP DEFAULT getdate() ENCODE zstd
)
SORTKEY
(
	visitkey,
	reportsuiteid,
	eventvalue,
	eventid,
	eventvariable
);






CREATE TABLE ods.fctomnituresiteprehitarchive
(
	hitkey VARCHAR(255) ENCODE zstd,
	visitkey VARCHAR(70) ENCODE zstd DISTKEY,
	visitorkey VARCHAR(60) ENCODE zstd,
	monthkey INTEGER ENCODE zstd,
	datekey INTEGER ENCODE zstd,
	hourkey INTEGER ENCODE zstd,
	accept_language VARCHAR(22) ENCODE zstd,
	browser BIGINT ENCODE zstd,
	color INTEGER ENCODE zstd,
	connection_type INTEGER ENCODE zstd,
	country INTEGER ENCODE zstd,
	curr_factor INTEGER ENCODE zstd,
	curr_rate REAL ENCODE runlength,
	daily_visitor INTEGER ENCODE zstd,
	date_time TIMESTAMP ENCODE zstd,
	domain VARCHAR(60) ENCODE zstd,
evarcolumns
	exclude_hit INTEGER ENCODE zstd,
	first_hit_page_url VARCHAR(255) ENCODE zstd,
	first_hit_pagename VARCHAR(255) ENCODE zstd,
	first_hit_referrer VARCHAR(255) ENCODE zstd,
	first_hit_time_gmt INTEGER ENCODE zstd,
	geo_city VARCHAR(60) ENCODE zstd,
	geo_country VARCHAR(60) ENCODE zstd,
	geo_region VARCHAR(60) ENCODE zstd,
	geo_zip VARCHAR(60) ENCODE zstd,
	hier1 VARCHAR(255) ENCODE zstd,
	hit_source INTEGER ENCODE zstd,
	hit_time_gmt INTEGER ENCODE delta,
	hitid_high BIGINT ENCODE zstd,
	hitid_low BIGINT ENCODE zstd,
	homepage VARCHAR(255) ENCODE zstd,
	hourly_visitor INTEGER ENCODE zstd,
	ip VARCHAR(100) ENCODE zstd,
	language INTEGER ENCODE zstd,
	last_hit_time_gmt INTEGER ENCODE delta,
	mobile_id INTEGER ENCODE zstd,
	monthly_visitor INTEGER ENCODE zstd,
	new_visit INTEGER ENCODE zstd,
	os BIGINT ENCODE bytedict,
	page_event_var1 VARCHAR(500) ENCODE zstd,
	browser_height INTEGER ENCODE zstd,
	browser_width BIGINT ENCODE zstd,
	channel VARCHAR(255) ENCODE zstd,
	cookies VARCHAR(255) ENCODE zstd,
	currency VARCHAR(255) ENCODE zstd,
	cust_hit_time_gmt INTEGER ENCODE delta,
	cust_visid VARCHAR(255) ENCODE zstd,
	event_list VARCHAR(255) ENCODE zstd,
	java_enabled VARCHAR(255) ENCODE zstd,
	mobileaction VARCHAR(255) ENCODE zstd,
	mobileappid VARCHAR(255) ENCODE zstd,
	mobiledayofweek VARCHAR(255) ENCODE zstd,
	mobiledayssincefirstuse VARCHAR(255) ENCODE zstd,
	mobiledayssincelastuse VARCHAR(255) ENCODE zstd,
	mobiledevice VARCHAR(255) ENCODE zstd,
	mobilehourofday VARCHAR(255) ENCODE zstd,
	mobileinstalldate VARCHAR(255) ENCODE zstd,
	mobilelaunchnumber VARCHAR(255) ENCODE zstd,
	mobileosversion VARCHAR(255) ENCODE zstd,
	mobileresolution VARCHAR(255) ENCODE zstd,
	page_event INTEGER ENCODE zstd,
	page_event_var2 VARCHAR(130) ENCODE zstd,
	page_url VARCHAR(255) ENCODE zstd,
	pagename VARCHAR(255) ENCODE zstd,
	pagename_no_url VARCHAR(130) ENCODE zstd,
	persistent_cookie VARCHAR(255) ENCODE zstd,
	product_list VARCHAR(255) ENCODE zstd,
	referrer VARCHAR(255) ENCODE zstd,
	t_time_info VARCHAR(255) ENCODE zstd,
	visid_high VARCHAR(25) ENCODE zstd,
	visid_low VARCHAR(25) ENCODE zstd,
	visid_type BIGINT ENCODE zstd,
propcolumns
	quarterly_visitor BIGINT ENCODE zstd,
	ref_domain VARCHAR(255) ENCODE zstd,
	ref_type INTEGER ENCODE zstd,
	resolution INTEGER ENCODE zstd,
	username VARCHAR(255) ENCODE zstd,
	visid_new VARCHAR(255) ENCODE zstd,
	visid_timestamp BIGINT ENCODE zstd,
	visit_num BIGINT ENCODE bytedict,
	visit_page_num BIGINT ENCODE bytedict,
	visit_referrer VARCHAR(255) ENCODE zstd,
	visit_search_engine VARCHAR(255) ENCODE zstd,
	visit_start_page_url VARCHAR(255) ENCODE zstd,
	visit_start_pagename VARCHAR(130) ENCODE zstd,
	visit_start_time_gmt BIGINT ENCODE zstd,
	weekly_visitor INTEGER ENCODE zstd,
	yearly_visitor INTEGER ENCODE zstd,
	inserttime TIMESTAMP DEFAULT getdate() ENCODE delta32k
)
SORTKEY
(
	monthkey,
	datekey,
	hitkey,
	visitkey
);



CREATE TABLE dw.fctomnituresiteprepageviewarchive
(
	hitkey VARCHAR(80) ENCODE zstd,
	visitkey VARCHAR(70) ENCODE zstd DISTKEY,
	visitorkey VARCHAR(60) ENCODE zstd,
	monthkey INTEGER ENCODE zstd,
	datekey INTEGER ENCODE zstd,
	hourkey INTEGER ENCODE zstd,
	reportsuiteid VARCHAR(50) ENCODE zstd,
	datetime TIMESTAMP ENCODE zstd,
	pagename VARCHAR(100) ENCODE zstd,
	pageurl VARCHAR(255) ENCODE zstd,
	spenttime INTEGER ENCODE zstd,
	visitpageseq INTEGER ENCODE zstd,
	channel VARCHAR(100) ENCODE zstd,
businesscolumns
	contactid BIGINT NOT NULL ENCODE zstd,
	pageevent INTEGER ENCODE zstd,
	islastpv INTEGER ENCODE zstd,
	inserttime TIMESTAMP DEFAULT getdate() ENCODE zstd
)
SORTKEY
(
	hitkey,
	visitkey,
	visitorkey,
	reportsuiteid,
	monthkey,
	datekey,
	hourkey
);




CREATE TABLE dw.fctomnituresiteprevisitarchive
(
	visitkey VARCHAR(70) ENCODE zstd DISTKEY,
	visitorkey VARCHAR(60) ENCODE zstd,
	monthkey INTEGER ENCODE zstd,
	datekey INTEGER ENCODE zstd,
	hourkey INTEGER ENCODE zstd,
	reportsuiteid VARCHAR(50) ENCODE zstd,
	datetime TIMESTAMP ENCODE zstd,
	visitnum INTEGER ENCODE zstd,
	spenttime INTEGER ENCODE zstd,
	pathlength INTEGER ENCODE zstd,
	entrypage VARCHAR(255) ENCODE zstd,
	exitpage VARCHAR(255) ENCODE zstd,
	reftype INTEGER ENCODE zstd,
	refdomain VARCHAR(255) ENCODE zstd,
	referrer VARCHAR(255) ENCODE zstd,
	browser BIGINT ENCODE zstd,
	connectiontype BIGINT ENCODE zstd,
	country BIGINT ENCODE zstd,
	language BIGINT ENCODE zstd,
	resolution BIGINT ENCODE zstd,
	color BIGINT ENCODE zstd,
	os BIGINT ENCODE zstd,
	inserttime TIMESTAMP DEFAULT getdate() ENCODE zstd
)
SORTKEY
(
	visitkey,
	visitorkey,
	reportsuiteid,
	monthkey,
	datekey,
	hourkey
);



CREATE TABLE dw.fctomnituresitepreeventarchive
(
	hitkey VARCHAR(80) ENCODE zstd,
	visitkey VARCHAR(70) ENCODE zstd DISTKEY,
	visitorkey VARCHAR(60) ENCODE zstd,
	monthkey INTEGER ENCODE zstd,
	datekey INTEGER ENCODE zstd,
	hourkey INTEGER ENCODE zstd,
	reportsuiteid VARCHAR(50) ENCODE zstd,
	datetime TIMESTAMP ENCODE zstd,
	eventid VARCHAR(100) ENCODE zstd,
	eventvariable VARCHAR(50) ENCODE zstd,
	eventvalue VARCHAR(255) ENCODE zstd,
businesscolumns
	contactid BIGINT ENCODE zstd,
	inserttime TIMESTAMP DEFAULT getdate() ENCODE zstd
)
SORTKEY
(
	visitkey,
	reportsuiteid,
	eventvalue,
	eventid,
	eventvariable
);


