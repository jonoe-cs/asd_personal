class Complaint:
    def __init__(self, complaint_id, customer_name, medicine, category, description, severity, assigned_staff="Unassigned", status="Open", date_submitted="", resolution="Pending"):
        self.complaint_id = complaint_id
        self.customer_name = customer_name
        self.medicine = medicine
        self.category = category
        self.description = description
        self.severity = severity
        self.assigned_staff = assigned_staff
        self.status = status
        self.date_submitted = date_submitted
        self.resolution = resolution

    def to_tuple(self):
        return (
            self.complaint_id,
            self.customer_name,
            self.medicine,
            self.category,
            self.description,
            self.severity,
            self.assigned_staff,
            self.status,
            self.date_submitted,
            self.resolution
        )
