import streamlit as st
from supabase import create_client, Client
from twilio.rest import Client as TwilioClient

# Initialize Supabase Cloud Connection securely
try:
    url: str = st.secrets["supabase"]["url"]
    key: str = st.secrets["supabase"]["key"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("❌ Critical Error: Supabase secrets invalid.")

def add_staff_member(first_name, last_name, nrc_number, phone_number, hourly_rate):
    data = {
        "first_name": first_name, 
        "last_name": last_name, 
        "nrc_number": nrc_number, 
        "phone_number": phone_number, 
        "hourly_rate": hourly_rate
    }
    return supabase.table("staff").insert(data).execute()

def fetch_all_staff():
    return supabase.table("staff").select("*").order("first_name").execute().data

def get_active_status(staff_id):
    """
    Checks if a staff member is actively on the clock.
    """
    return len(supabase.table("timecards").select("is_active").eq("staff_id", staff_id).eq("is_active", True).execute().data) > 0

def punch_in_staff(staff_id):
    """
    Inserts a live timecard record. Bypasses old payroll_periods dependency.
    """
    return supabase.table("timecards").insert({
        "staff_id": staff_id, 
        "is_active": True
    }).execute()

def punch_out_staff(staff_id):
    """
    Flips the open timecard card to inactive, logging the clock-out event.
    """
    res = supabase.table("timecards").select("timecard_id").eq("staff_id", staff_id).eq("is_active", True).execute()
    if res.data:
        return supabase.table("timecards").update({"is_active": False}).eq("timecard_id", res.data[0]["timecard_id"]).execute()

def add_shortage_entry(staff_id, date, amount, reason):
    """
    Records a financial deduction securely linked directly to the staff profile.
    """
    return supabase.table("shortages").insert({
        "staff_id": staff_id, 
        "date": str(date), 
        "amount": amount, 
        "reason": reason
    }).execute()

def fetch_shift_summaries():
    return supabase.table("v_shift_summaries").select("*").order("clock_in_cat", desc=True).execute().data

def fetch_payroll_summary():
    return supabase.table("v_payroll_summary").select("*").execute().data

def generate_payslip_text(first_name, start_dt, end_dt, hours, gross, shortages, net):
    date_range_str = f"{start_dt.strftime('%d %b')} to {end_dt.strftime('%d %b')}"
    return (
        f"Mobix Slip: {first_name}\n"
        f"Dates: {date_range_str}\n"
        f"------------------\n"
        f"Hours: {hours:.2f} hrs\n"
        f"Gross: ZMW {gross:,.2f}\n"
        f"Shortage: ZMW {shortages:,.2f}\n"
        f"------------------\n"
        f"NET PAY: ZMW {net:,.2f}"
    )

def send_payslip_sms(phone_number, message_body):
    client = TwilioClient(st.secrets["twilio"]["account_sid"], st.secrets["twilio"]["auth_token"])
    return client.messages.create(
        body=message_body,
        from_=st.secrets["twilio"]["from_number"], 
        to=phone_number
    ).sid

def login_user(email, password):
    try:
        return supabase.auth.sign_in_with_password({"email": email, "password": password}).user
    except:
        return None

def logout_user():
    try:
        supabase.auth.sign_out()
    except:
        pass
