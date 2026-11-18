import streamlit as st
from datetime import datetime
from complaints.complaint import Complaint
from complaints.complaint_manager import ComplaintManager

def load_dummy_data():
    """Injects sample mock complaints for testing."""
    sample_complaints = [
        Complaint("CMP001", "John Smith", "Paracetamol", "Side effect", "Customer reports a mild skin rash after 2 days.", "Medium", "Lead Pharmacist", "Open", "15/11/2026", "Pending"),
        Complaint("CMP002", "Sarah Jenkins", "Amoxicillin", "Incorrect dosage", "Received 250mg capsules instead of prescribed 500mg.", "High", "Assistant Pharmacist", "In Progress", "16/11/2026", "Pending"),
        Complaint("CMP003", "David Lee", "Ibuprofen", "Packaging defect", "Blister pack was already punctured upon opening.", "Low", "Unassigned", "Open", "17/11/2026", "Pending"),
        Complaint("CMP004", "Emma Watson", "Metformin", "Delivery issue", "Home delivery arrived 3 days late, medication exposed to heat.", "Critical", "Customer Support Lead", "Resolved", "10/11/2026", "Replacement sent"),
        Complaint("CMP005", "Michael Brown", "Lipitor", "Side effect", "Severe dizziness experienced shortly after taking the evening dose.", "High", "Lead Pharmacist", "In Progress", "18/11/2026", "Consulting doctor")
    ]
    
    for c in sample_complaints:
        try:
            ComplaintManager.add_complaint(c)
        except Exception:
            pass

def render_complaint_app():
    st.title("💊 Pharmacy Complaint Tracking System")
    st.markdown("Milestone 1: Form entry, SQLite storage, Table view, Status updates, and Staff assignment.")

    menu = ["View Complaints", "Submit New Complaint", "Update / Manage Complaint"]
    choice = st.sidebar.selectbox("Navigation Menu", menu)

    st.sidebar.divider()
    if st.sidebar.button("⚡ Load Test Complaints"):
        load_dummy_data()
        st.sidebar.success("Test data loaded! Refresh or change tabs to view.")
        st.rerun()

    # 1. VIEW COMPLAINTS
    if choice == "View Complaints":
        st.subheader("📋 All Logged Complaints")
        df = ComplaintManager.get_all_complaints_df()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            st.info(f"Total complaints recorded: {len(df)}")
        else:
            st.warning("No complaints recorded in the database yet.")

    # 2. SUBMIT COMPLAINT FORM
    elif choice == "Submit New Complaint":
        st.subheader("📝 Submit a New Complaint")
        
        with st.form("complaint_form"):
            df = ComplaintManager.get_all_complaints_df()
            next_id = f"CMP{len(df) + 1:03d}"
            
            col1, col2 = st.columns(2)
            with col1:
                complaint_id = st.text_input("Complaint ID", value=next_id)
                customer_name = st.text_input("Customer Name", placeholder="e.g. John Smith")
                medicine = st.text_input("Medicine", placeholder="e.g. Paracetamol")
                category = st.selectbox("Complaint Category", ["Side effect", "Packaging defect", "Incorrect dosage", "Delivery issue", "Other"])
                severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
                
            with col2:
                assigned_staff = st.selectbox("Assign Staff", ["Unassigned", "Lead Pharmacist", "Assistant Pharmacist", "Customer Support Lead"])
                status = "Open"
                date_submitted = datetime.now().strftime("%d/%m/%Y")
                resolution = "Pending"
                
            description = st.text_area("Complaint Description", placeholder="Enter detailed description of the issue...")
            
            submitted = st.form_submit_button("Submit Complaint")
            
            if submitted:
                if not complaint_id or not customer_name or not medicine:
                    st.error("Please fill out all mandatory fields.")
                else:
                    try:
                        new_complaint = Complaint(
                            complaint_id, customer_name, medicine, category, 
                            description, severity, assigned_staff, status, date_submitted, resolution
                        )
                        ComplaintManager.add_complaint(new_complaint)
                        st.success(f"Successfully recorded complaint ID: {complaint_id}")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # 3. UPDATE / MANAGE COMPLAINT
    elif choice == "Update / Manage Complaint":
        st.subheader("⚙️ Update Status & Staff Assignment")
        df = ComplaintManager.get_all_complaints_df()
        
        if df.empty:
            st.warning("No complaints available to update.")
        else:
            selected_id = st.selectbox("Select Complaint ID to Manage", df["complaint_id"].tolist())
            record = df[df["complaint_id"] == selected_id].iloc[0]
            
            st.write(f"**Customer:** {record['customer_name']} | **Medicine:** {record['medicine']} | **Current Staff:** {record['assigned_staff']}")
            
            with st.form("update_form"):
                status_options = ["Open", "In Progress", "Resolved", "Closed"]
                current_status_idx = status_options.index(record["status"]) if record["status"] in status_options else 0
                new_status = st.selectbox("Update Status", status_options, index=current_status_idx)
                
                staff_options = ["Unassigned", "Lead Pharmacist", "Assistant Pharmacist", "Customer Support Lead"]
                current_staff_idx = staff_options.index(record["assigned_staff"]) if record["assigned_staff"] in staff_options else 0
                new_staff = st.selectbox("Assign/Reassign Staff (Authorised)", staff_options, index=current_staff_idx)
                
                current_resolution = "" if record["resolution"] == "Pending" else record["resolution"]
                new_resolution = st.text_area("Resolution Notes", value=current_resolution)
                
                update_btn = st.form_submit_button("Save Changes")
                
                if update_btn:
                    final_resolution = new_resolution.strip() if new_resolution.strip() else "Pending"
                    ComplaintManager.update_complaint_status(selected_id, new_status, final_resolution)
                    ComplaintManager.assign_staff(selected_id, new_staff)
                    st.success(f"Complaint {selected_id} updated successfully!")
                    st.rerun()