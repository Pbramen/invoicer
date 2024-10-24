/* customers */
INSERT OR IGNORE INTO 'auth_user' ('id','password','last_login','is_superuser','username','last_name','email','is_staff','is_active','date_joined','first_name') VALUES ('1','pbkdf2_sha256$870000$A1ZD0nfHbxd63Abi3zp483$gIUOBqgyiOn4FfusZAz/KQkymX9myzzxMobII4fZHMo=','2024-10-14 21:36:58.017597','0','guest','banh','peterbanh@gmail.com','0','1','2024-10-14 21:36:47.523038','peter');
INSERT OR IGNORE INTO 'custom_users_contact' ('id', 'name') VALUES ('1', 'peter banh');
INSERT OR IGNORE INTO 'custom_users_usercontactinfo' ('id', 'alert_timeframes', 'contact_id', 'user_id') VALUES ('1', '30d', '1', '1');
INSERT OR IGNORE INTO 'custom_users_address' ('id', 'category', 'street', 'city', 'state', 'zipcode') VALUES ('1', 'H', '100 Work str', 'San Antonio', 'Texas', '79102');
INSERT OR IGNORE INTO 'custom_users_contact_address' ('id', 'contact_id', 'address_id') VALUES (1, 1, 1);
INSERT OR IGNORE INTO 'custom_users_contact_phoneNumber' ('id', 'contact_id', 'phoneNumber_id') VALUES (1, 1, 1);
INSERT OR IGNORE INTO 'custom_users_phonenumber' ('id', 'category', 'phone_number') VALUES (1, 'M', '210 555-5555');
INSERT OR IGNORE INTO 'custom_users_customer' ('id', 'customer_name', 'customer_contact_id', 'is_registered') VALUES (1, 'peter banh', 1, true);
INSERT OR IGNORE INTO 'custom_users_vendorcustomer' ('id', 'date_created', 'customer_id', 'vendor_id') VALUES (1, '2024-10-14 21:36:47.523038', 1, 2);

INSERT OR IGNORE INTO 'auth_user' ('id','password','last_login','is_superuser','username','last_name','email','is_staff','is_active','date_joined','first_name') VALUES ('3','pbkdf2_sha256$870000$A1ZD0nfHbxd63Abi3zp483$gIUOBqgyiOn4FfusZAz/KQkymX9myzzxMobII4fZHMo=','2024-10-14 21:36:58.017597','0','carl','wheezler','carlwheezler@gmail.com','0','1','2024-10-14 21:36:47.523038','carl');
INSERT OR IGNORE INTO 'custom_users_contact' ('id', 'name') VALUES ('3', 'carl wheezler');
INSERT OR IGNORE INTO 'custom_users_usercontactinfo' ('id', 'alert_timeframes', 'contact_id', 'user_id') VALUES ('1', '30d', '3', '3');
INSERT OR IGNORE INTO 'custom_users_address' ('id', 'category', 'street', 'city', 'state', 'zipcode') VALUES ('2', 'H', '8012 Blue Bulevard', 'Salt Lake City', 'Utah', '32156');
INSERT OR IGNORE INTO 'custom_users_contact_address' ('id', 'contact_id', 'address_id') VALUES (3, 3, 2);

/* employee */
INSERT OR IGNORE INTO 'auth_user' ('id','password','last_login','is_superuser','username','last_name','email','is_staff','is_active','date_joined','first_name') VALUES ('2','pbkdf2_sha256$870000$A1ZD0nfHbxd63Abi3zp483$gIUOBqgyiOn4FfusZAz/KQkymX9myzzxMobII4fZHMo=','2024-10-14 21:36:58.017597','0','johnSmith','smith','johnSmith@gmail.com','0','1','2024-10-14 21:36:47.523038','john');
INSERT OR IGNORE INTO 'custom_users_contact' ('id', 'name') VALUES ('2', 'john smith');
INSERT OR IGNORE INTO 'custom_users_usercontactinfo' ('id', 'alert_timeframes', 'contact_id', 'user_id') VALUES ('2', '30d', '2', '2');
INSERT OR IGNORE INTO 'custom_users_contact_address' ('id', 'contact_id', 'address_id') VALUES (2, 2, 2);
INSERT OR IGNORE INTO 'custom_users_employees' ('id', 'employee_id', 'vendor_id', 'role') VALUES ( 1, 2, 1, 'E' );
INSERT OR IGNORE INTO 'custom_users_address' ('id', 'category', 'street', 'city', 'state', 'zipcode') VALUES (3, 'J', '2342 Worked AVE', 'New York City', 'New York', '20231-3241');


INSERT OR IGNORE INTO 'custom_users_vendor' ('id', 'uuid', 'status', 'vendor_name', 'vendor_contact_id') VALUES (1, '123abc', true, 'Apex Housing', 2);
INSERT OR IGNORE INTO 'custom_users_contact' ('id', 'name') VALUES ('4', 'Apex Housing');
INSERT OR IGNORE INTO 'custom_users_contact_address' ('id', 'contact_id', 'address_id') VALUES (4, 4, 3);


INSERT OR IGNORE INTO 'invoice_jobsite' ('id', 'name', 'address_id') VALUES ('1', '2342 Worked AVE New York City, New York, 20231-3241', 3);
INSERT OR IGNORE INTO 'invoice_jobsite' ('id', 'name', 'address_id') VALUES ('2', '2342 Worked AVE New York City, New York, 20231-3241', 3);

INSERT OR IGNORE INTO 'invoice_workorder' ('id', 'order_title', 'order_descript', 'vendor_id', 'completion_date', 'job_site_id', 'status') VALUES (1, 'Bathroom Rennovation', 'Complete overhall of downstairs bathroom', 1, null, 1, 'N');
INSERT OR IGNORE INTO 'invoice_workorder' ('id', 'order_title', 'order_descript', 'vendor_id', 'completion_date', 'job_site_id', 'status') VALUES (2, 'Foundation inspection', 'Inspection for insurance claim', 1, null, 2, 'N');

INSERT OR IGNORE INTO 'invoice_workorder' ('id', 'order_title', 'order_descript', 'vendor_id', 'completion_date', 'job_site_id', 'status') VALUES (3, 'Roof Replacement', 'Roof tile replacement after hail damage', 1, null, 2, 'A');
INSERT OR IGNORE INTO 'invoice_workitem' ('id', 'cost', 'memo', 'descript', 'work_order_id') VALUES (1, 300.00, 'service', 'installation fees', 3);
INSERT OR IGNORE INTO 'invoice_workitem' ('id', 'cost', 'memo', 'descript', 'work_order_id') VALUES (2, 750.40, 'tiles', 'material fees',  3);


/***************************************************************************************************************************************************/


CREATE OR IGNORE VIEW 