-- 1. Create Staff Table (with NRC field)
create table staff (
  staff_id UUID default gen_random_uuid () primary key,
  nrc_number VARCHAR(20) not null unique, -- Added unique constraint to prevent duplicate IDs
  first_name VARCHAR(50) not null,
  last_name VARCHAR(50) not null,
  phone_number VARCHAR(15) not null unique, -- E.164 format (e.g., +260XXXXXXXXX)
  hourly_rate NUMERIC(10, 2) not null check (hourly_rate >= 0),
  created_at timestamp with time zone default TIMEZONE ('utc'::text, NOW()) not null
);

-- Optimize searching by NRC
create index idx_staff_nrc on staff (nrc_number);

-- 2. Create Timecards Table
create table timecards (
  timecard_id UUID default gen_random_uuid () primary key,
  staff_id UUID references staff (staff_id) on delete CASCADE not null,
  date DATE not null,
  hours_worked NUMERIC(5, 2) not null check (hours_worked >= 0),
  created_at timestamp with time zone default TIMEZONE ('utc'::text, NOW()) not null,
  unique (staff_id, date) -- Prevents duplicate daily entries per employee
);

-- 3. Create Shortages & Deductions Table
create table shortages (
  shortage_id UUID default gen_random_uuid () primary key,
  staff_id UUID references staff (staff_id) on delete CASCADE not null,
  date DATE not null,
  amount NUMERIC(10, 2) not null check (amount >= 0),
  reason TEXT not null,
  created_at timestamp with time zone default TIMEZONE ('utc'::text, NOW()) not null
);

-- 4. Create Payout Log Table
create table payout_log (
  payout_id UUID default gen_random_uuid () primary key,
  staff_id UUID references staff (staff_id) on delete RESTRICT not null,
  period_start DATE not null,
  period_end DATE not null,
  gross_earnings NUMERIC(10, 2) not null,
  total_deductions NUMERIC(10, 2) not null,
  net_pay NUMERIC(10, 2) not null,
  sms_status VARCHAR(20) default 'Pending' check (sms_status in ('Pending', 'Sent', 'Failed')),
  created_at timestamp with time zone default TIMEZONE ('utc'::text, NOW()) not null
);
