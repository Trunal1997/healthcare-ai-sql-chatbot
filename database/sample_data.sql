INSERT INTO patients (name, age, gender, city, phone, blood_group) VALUES
('Rahul Sharma', 55, 'Male', 'Pune', '9876543210', 'B+'),
('Priya Verma', 42, 'Female', 'Nagpur', '9876543211', 'A+'),
('Amit Joshi', 63, 'Male', 'Pune', '9876543212', 'O+'),
('Sneha Patil', 29, 'Female', 'Mumbai', '9876543213', 'AB+'),
('Karan Mehta', 48, 'Male', 'Pune', '9876543214', 'B-'),
('Neha Kulkarni', 58, 'Female', 'Pune', '9876543215', 'A-'),
('Ramesh Pawar', 67, 'Male', 'Nagpur', '9876543216', 'O-');

INSERT INTO doctors (name, specialization, hospital_name) VALUES
('Dr. Mehta', 'Cardiology', 'Ruby Hall Clinic'),
('Dr. Patil', 'Diabetology', 'Jehangir Hospital'),
('Dr. Shah', 'Neurology', 'Sahyadri Hospital'),
('Dr. Deshmukh', 'Orthopedics', 'Noble Hospital');

INSERT INTO appointments (patient_id, doctor_id, appointment_date, status) VALUES
(1, 2, CURRENT_DATE, 'Scheduled'),
(2, 1, CURRENT_DATE, 'Completed'),
(3, 2, CURRENT_DATE + 1, 'Scheduled'),
(4, 3, CURRENT_DATE, 'Cancelled'),
(5, 4, CURRENT_DATE + 2, 'Scheduled'),
(6, 2, CURRENT_DATE, 'Scheduled');

INSERT INTO diagnosis (patient_id, disease, diagnosis_date, severity) VALUES
(1, 'Diabetes', CURRENT_DATE - 10, 'High'),
(3, 'Diabetes', CURRENT_DATE - 20, 'Medium'),
(2, 'Hypertension', CURRENT_DATE - 15, 'Low'),
(4, 'Migraine', CURRENT_DATE - 5, 'Medium'),
(5, 'Asthma', CURRENT_DATE - 8, 'Low'),
(6, 'Diabetes', CURRENT_DATE - 2, 'High'),
(7, 'Hypertension', CURRENT_DATE - 30, 'High');

INSERT INTO billing (patient_id, amount, payment_status, bill_date) VALUES
(1, 5200, 'UNPAID', CURRENT_DATE),
(2, 3400, 'PAID', CURRENT_DATE),
(3, 8700, 'UNPAID', CURRENT_DATE),
(4, 1500, 'PAID', CURRENT_DATE),
(5, 6200, 'UNPAID', CURRENT_DATE - 1),
(6, 9400, 'UNPAID', CURRENT_DATE),
(7, 2800, 'PAID', CURRENT_DATE - 3);
