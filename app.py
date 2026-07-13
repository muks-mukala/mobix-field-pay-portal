import streamlit as st
import datetime
import pandas as pd

# Clean module imports for our separate layers
import src.db_utils as db

st.set_page_config(page_title="Mobix Pay Portal", page_icon="📊", layout="wide")

# DESIGN LAYER SEPARATION: Read and inject external stylesheet asset cleanly
with open("src/styles.css") as f:
    st.html(f"<style>{f.read()}</style>")

# Initialize login session state variables if they don't exist
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None

# --- AUTHENTICATION SCREEN ---
if not st.session_state["logged_in"]:
    _, center_col, _ = st.columns([1, 1.2, 1])
    
    with center_col:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center;'>🔒 Mobix Portal Login</h2>", unsafe_allow_html=True)
            st.write("Please authenticate to access the command center.")
            
            with st.form("login_form", clear_on_submit=False):
                email = st.text_input("Email Address")
                password = st.text_input("Password", type="password")
                login_button = st.form_submit_button("Access Portal", use_container_width=True, type="primary")
                
                if login_button:
                    user = db.login_user(email, password)
                    if user:
                        st.session_state["logged_in"] = True
                        st.session_state["user_email"] = email
                        st.success("🔒 Access Granted!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password.")
    st.stop() 

# --- AUTHORIZED PORTAL CODES ---
st.sidebar.write(f"👤 Active: **{st.session_state['user_email']}**")

page = st.sidebar.radio(
    label="", 
    options=["Staff Onboarding", "Log Hours (Timecards)", "Log Shortages", "Dashboard Overview"]
)

# Logout Utility Button at bottom of sidebar
st.sidebar.write("---")
if st.sidebar.button("🚪 Log Out Session", use_container_width=True):
    db.logout_user()
    st.session_state["logged_in"] = False
    st.session_state["user_email"] = None
    st.rerun()

# 1. PAGE: Staff Onboarding
if page == "Staff Onboarding":
    st.markdown('<div class="sticky-heading"><h1>👤 Staff Onboarding</h1></div>', unsafe_allow_html=True)
    st.write("Register a new staff member directly into the database.")
    
    with st.form("onboarding_form", clear_on_submit=True):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        nrc_number = st.text_input("NRC Number")
        phone_number = st.text_input("Notification Destination (Email or Gateway Address)")
        hourly_rate = st.number_input("Hourly Pay Rate (ZMW)", min_value=0.0, step=5.0)
        submit_button = st.form_submit_button("Register Staff Member")
        
        if submit_button:
            if first_name and last_name and nrc_number and phone_number:
                try:
                    db.add_staff_member(first_name, last_name, nrc_number, phone_number, hourly_rate)
                    st.success(f"🎉 Registered {first_name} {last_name} successfully!")
                except Exception as e:
                    st.error(f"Error handling database execution: {e}")
            else:
                st.error("Please fill out all mandatory fields.")

# 2. PAGE: Log Hours (Timecards)
elif page == "Log Hours (Timecards)":
    st.markdown('<div class="sticky-heading"><h1>⏱️ Live Punch Clock Station</h1></div>', unsafe_allow_html=True)
    try:
        staff_data = db.fetch_all_staff()
    except Exception as e:
        st.error(f"Database connection issue: {e}")
        staff_data = []

    if staff_data:
        staff_options = {f"{s['first_name']} {s['last_name']}": s['staff_id'] for s in staff_data}
        selected_display = st.selectbox("Select Staff Member", options=list(staff_options.keys()))
        chosen_uuid = staff_options[selected_display]
        
        try:
            is_clocked_in = db.get_active_status(chosen_uuid)
            st.write("---")
            
            if not is_clocked_in:
                st.info(f"🟢 Status: Clocked Out.")
                if st.button("🚀 PUNCH IN (Start Shift)", use_container_width=True, type="primary"):
                    db.punch_in_staff(chosen_uuid)
                    st.success("⚡ Clocked In!")
                    st.rerun()
            else:
                st.warning(f"🔴 Status: On the Clock.")
                if st.button("🛑 PUNCH OUT (End Shift)", use_container_width=True, type="secondary"):
                    db.punch_out_staff(chosen_uuid)
                    st.success("💾 Shift logged!")
                    st.rerun()
        except Exception as e:
            st.error(f"Error executing punch status change: {e}")

# 3. PAGE: Log Shortages
elif page == "Log Shortages":
    st.markdown('<div class="sticky-heading"><h1>💸 Log Shortages & Deductions</h1></div>', unsafe_allow_html=True)
    try:
        staff_data = db.fetch_all_staff()
    except Exception as e:
        staff_data = []

    if staff_data:
        staff_options = {f"{s['first_name']} {s['last_name']}": s['staff_id'] for s in staff_data}
        with st.form("shortage_form"):
            selected_display = st.selectbox("Select Staff Member", options=list(staff_options.keys()))
            chosen_uuid = staff_options[selected_display]
            selected_date = st.date_input("Date of Deductions", value=datetime.date.today())
            amount = st.number_input("Deduction Amount (ZMW)", min_value=0.0, step=10.0)
            reason = st.text_input("Reason")
            submit_shortage = st.form_submit_button("Save Shortage Log")
            
            if submit_shortage:
                try:
                    db.add_shortage_entry(chosen_uuid, selected_date, amount, reason)
                    st.success(f"💸 Recorded ZMW {amount} deduction!")
                except Exception as e:
                    st.error(f"Failed to submit shortage log: {e}")

# 4. PAGE: Dashboard Overview
elif page == "Dashboard Overview":
    st.markdown('<div class="sticky-heading"><h1>📈 Operational Dashboard & Payroll Command</h1></div>', unsafe_allow_html=True)
    
    st.write("### 📅 Filter Operational Timeline")
    col_start, col_end = st.columns(2)
    with col_start:
        start_date = st.date_input("Start Date", value=datetime.date.today() - datetime.timedelta(days=7))
    with col_end:
        end_date = st.date_input("End Date", value=datetime.date.today())
        
    st.write("---")
    
    try:
        payroll = db.fetch_payroll_summary()
        shifts = db.fetch_shift_summaries()
    except Exception as e:
        st.error(f"Could not connect to cloud engine metrics: {e}")
        payroll = []
        shifts = []
        
    if not payroll or not shifts:
        st.info("📊 No logged payroll records found in the cloud database yet.")
    else:
        df_pay = pd.DataFrame(payroll)
        df_shifts = pd.DataFrame(shifts)
        
        df_shifts['clock_in_date'] = pd.to_datetime(df_shifts['clock_in_cat'], format='ISO8601').dt.date
        
        df_shifts_filtered = df_shifts[
            (df_shifts['clock_in_date'] >= start_date) & 
            (df_shifts['clock_in_date'] <= end_date)
        ].copy()
        
        if not df_shifts_filtered.empty:
            summary_totals = df_shifts_filtered.groupby('staff_id').agg(
                total_hours=('hours_worked', 'sum'),
                total_gross_pay=('gross_pay', 'sum')
            ).reset_index()
            
            df_pay_filtered = df_pay.drop(columns=['total_hours', 'total_gross_pay']).merge(summary_totals, on='staff_id', how='inner')
            df_pay_filtered['net_pay'] = df_pay_filtered['total_gross_pay'] - df_pay_filtered['total_deductions']
        else:
            df_pay_filtered = pd.DataFrame(columns=df_pay.columns)

        if df_pay_filtered.empty:
            st.warning("⚠️ No operational work records exist inside this specific calendar range.")
        else:
            df_pay_filtered['total_gross_pay'] = df_pay_filtered['total_gross_pay'].fillna(0.0).astype(float)
            df_pay_filtered['total_deductions'] = df_pay_filtered['total_deductions'].fillna(0.0).astype(float)
            df_pay_filtered['net_pay'] = df_pay_filtered['net_pay'].fillna(0.0).astype(float)
            df_pay_filtered['total_hours'] = df_pay_filtered['total_hours'].fillna(0.0).astype(float)

            # DYNAMIC METRICS BLOCKS
            total_gross = df_pay_filtered['total_gross_pay'].sum()
            total_deductions = df_pay_filtered['total_deductions'].sum()
            total_net = df_pay_filtered['net_pay'].sum()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Gross Payroll Committed", f"ZK {total_gross:,.2f}")
            with col2:
                st.metric("Total Deductions (Shortages)", f"ZK {total_deductions:,.2f}", delta=f"-ZK {total_deductions:,.2f}", delta_color="inverse")
            with col3:
                st.metric("Net Payroll Outstanding", f"ZK {total_net:,.2f}")
                
            # TABLE: Main Summary Sheet
            st.write("### 🧮 Staff Payroll Sheets Summary")
            df_pay_filtered['Staff Member'] = df_pay_filtered['first_name'] + " " + df_pay_filtered['last_name']
            
            display_pay = df_pay_filtered[['Staff Member', 'nrc_number', 'total_hours', 'total_gross_pay', 'total_deductions', 'net_pay']].copy()
            display_pay.columns = ['Staff Member', 'NRC Number', 'Accumulated Hours', 'Gross Pay (ZMW)', 'Shortages (ZMW)', 'Net Payout (ZMW)']
            
            st.dataframe(display_pay, use_container_width=True, hide_index=True)
            
            # Export to CSV Button Widget
            csv_data = display_pay.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Current View to CSV",
                data=csv_data,
                file_name=f"mobix_pay_summary_{start_date}_to_{end_date}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            # EXPANDER: Live Auditable Shift Logs
            with st.expander("📝 View Detailed Shift Log History"):
                df_shifts_filtered['Clock In'] = pd.to_datetime(df_shifts_filtered['clock_in_cat'], format='ISO8601').dt.strftime('%Y-%m-%d %H:%M')
                df_shifts_filtered['Clock Out'] = pd.to_datetime(df_shifts_filtered['clock_out_cat'], format='ISO8601').dt.strftime('%Y-%m-%d %H:%M').fillna("On the Clock")
                df_shifts_filtered['Staff Member'] = df_shifts_filtered['first_name'] + " " + df_shifts_filtered['last_name']
                
                unique_staff_in_logs = ["All Team Members"] + sorted(df_shifts_filtered['Staff Member'].unique().tolist())
                selected_audit_person = st.selectbox(
                    "🔍 Filter history by name:", 
                    options=unique_staff_in_logs,
                    key="shift_log_audit_filter"
                )
                
                if selected_audit_person != "All Team Members":
                    df_logs_to_show = df_shifts_filtered[df_shifts_filtered['Staff Member'] == selected_audit_person]
                else:
                    df_logs_to_show = df_shifts_filtered
                
                if not df_logs_to_show.empty:
                    display_shifts = df_logs_to_show[['Staff Member', 'Clock In', 'Clock Out', 'hours_worked', 'gross_pay']].copy()
                    display_shifts.columns = ['Staff Member', 'Clock In Time (CAT)', 'Clock Out Time (CAT)', 'Hours Worked', 'Gross Earnings (ZMW)']
                    st.dataframe(display_shifts, use_container_width=True, hide_index=True)
                else:
                    st.info("No recorded work shifts matching this name in this date window.")

            # ACTION INTERFACE: Selective Broadcast Engine
            st.write("---")
            st.write("### 📲 Feature Phone Payslip Dispatcher")
            st.write("Select which team members should receive their notifications for the active date range above.")
            
            all_recipients = df_pay_filtered['Staff Member'].tolist()
            selected_recipients = st.multiselect(
                "Select Recipients (Leave empty to target everyone):", 
                options=all_recipients,
                placeholder="Choose specific staff members..."
            )
            
            if selected_recipients:
                df_dispatch_pool = df_pay_filtered[df_pay_filtered['Staff Member'].isin(selected_recipients)]
            else:
                df_dispatch_pool = df_pay_filtered

            # Message Length & Character Safety Preview Counter
            sample_row = df_dispatch_pool.iloc[0] if not df_dispatch_pool.empty else None
            if sample_row is not None:
                sample_text = db.generate_payslip_text(
                    sample_row['first_name'],
                    start_date,
                    end_date,
                    float(sample_row['total_hours']), 
                    float(sample_row['total_gross_pay']), 
                    float(sample_row['total_deductions']), 
                    float(sample_row['net_pay'])
                )
                char_count = len(sample_text)
                sms_segments = (char_count // 160) + 1
                
                with st.expander("👁️ Review SMS Character Blueprint Preview"):
                    st.code(sample_text, language="text")
                    if char_count <= 160:
                        st.success(f"📏 Character Weight: {char_count}/160 ({sms_segments} standard SMS segment) — Safe for feature phone networks.")
                    else:
                        st.warning(f"⚠️ Character Weight: {char_count}/160 ({sms_segments} SMS segments) — Longer message might split or incur extra carrier costs.")

            st.info(
                f"📋 **Dispatch Summary Confirmation:**\n"
                f"* **Target Period:** {start_date.strftime('%d %b %Y')} to {end_date.strftime('%d %b %Y')}\n"
                f"* **Recipients Queue Count:** {len(df_dispatch_pool)} staff member(s)"
            )
            
            if st.button("🚀 BROADCAST PAYSLIPS VIA SMS/MAIL", use_container_width=True, type="primary"):
                success_count = 0
                error_count = 0
                
                with st.spinner("Processing calculations and dispatching notifications..."):
                    try:
                        staff_directory = db.fetch_all_staff()
                        phone_lookup = {s['staff_id']: s['phone_number'] for s in staff_directory}
                    except Exception as conn_err:
                        st.error(f"Unable to read contact lookups from Supabase: {conn_err}")
                        phone_lookup = {}

                    for _, row in df_dispatch_pool.iterrows():
                        staff_id = row['staff_id']
                        target_destination = phone_lookup.get(staff_id)
                        
                        if target_destination:
                            try:
                                custom_body = db.generate_payslip_text(
                                    first_name=row['first_name'],
                                    start_dt=start_date,
                                    end_dt=end_date,
                                    hours=float(row['total_hours']),
                                    gross=float(row['total_gross_pay']),
                                    shortages=float(row['total_deductions']),
                                    net=float(row['net_pay'])
                                )
                                db.send_payslip_sms(target_destination, custom_body)
                                success_count += 1
                            except Exception as sms_err:
                                st.error(f"Transmission dropout out to {row['first_name']}: {sms_err}")
                                error_count += 1
                
                if success_count > 0:
                    st.success(f"🎉 Successfully dispatched {success_count} notifications out to the field!")
