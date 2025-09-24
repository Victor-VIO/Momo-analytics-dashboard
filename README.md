# Team Name:

## Project: MoMo SMS Analytics Dashboard

#Team Members
Victor Idowu
Elyse ISHIMWE
Divine KUZO
Crispin HIRWA

##Project Description
This project processes MoMo SMS data in XML format, cleans and categorizes the data, stores it in a relational database, and provides a frontend dashboard for analytics and visualization.

## Scrum Board

https://github.com/users/Victor-VIO/projects/4/views/1[Link to scrum board]

## Architecture Diagram

https://drive.google.com/file/d/168doz9eupF_xOoHJLmqCt6lxX3chw3cY/view?usp=drive_link[Diagram Link]

## Database design and implimentation

### Overview

We use a relational schema to store MoMo transactions, user (sender/receiver) details, categories, and ETL system logs. The main tables are: Users, Transaction_Categories, Transactions, and System_Logs.

### Tables & Key Columns

- _Users_
  - user_id (INT, PK), name (VARCHAR), phone_number (VARCHAR), email (VARCHAR)
- _Transaction_Categories_
  - category_id (INT, PK), category_name, description
- _Transactions_
  - transaction_id (INT, PK), sender_id (FK → Users.user_id), receiver_id (FK → Users.user_id),
    category_id (FK → Transaction_Categories.category_id), amount (DECIMAL), transaction_time (DATETIME), status (ENUM)
- _System_Logs_
  - log_id (INT, PK), transaction_id (FK → Transactions.transaction_id), log_time, message

### Relationships

- One _User_ can be sender or receiver in many _Transactions_ (1 : M).
- One _Category_ applies to many _Transactions_ (1 : M).
- One _Transaction_ may have many _System_Logs_ (1 : M).

### Sample Query (join to get full transaction details)

```sql
SELECT t.transaction_id, s.name AS sender_name, r.name AS receiver_name,
       c.category_name, t.amount, t.transaction_time, t.status
FROM Transactions t
JOIN Users s ON t.sender_id = s.user_id
JOIN Users r ON t.receiver_id = r.user_id
JOIN Transaction_Categories c ON t.category_id = c.category_id
WHERE t.transaction_id = 101;


```

### Documentation

See [Database Design Rationale](/docs/database_design_rationale.md) for a detailed 200–300 word explanation of our design decisions.
