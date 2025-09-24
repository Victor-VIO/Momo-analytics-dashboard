Justification of Design Decisions

1. Users as a separate entity
   Both sender and receiver are users.
   Instead of duplicating sender/receiver attributes inside each transaction, I normalized them into a single Users table. This prevents redundancy.

2. Categories as a separate entity
   Each transaction belongs to a category (Payment, Transfer, etc.).

By creating a Categories table, we can easily expand with more categories and avoid repetition.

3. Transactions as a central linking entity
   Transactions hold the actual event: amount, time, and status.

It connects Users (sender/receiver) and Categories.

Both sender_id and receiver_id are foreign keys pointing back to the Users table, making it a self-referencing relationship (a user can transact with another user).

4. Relationships
   One User → Many Transactions (as sender).

One User → Many Transactions (as receiver).

One Category → Many Transactions.

This structure reflects the real-world scenario where:

A user can send/receive multiple transactions.

A category can apply to multiple transactions.
