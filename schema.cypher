// 1. Uniqueness Constraints
CREATE CONSTRAINT unique_person_id IF NOT EXISTS
FOR (p:Person) REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT unique_account_no IF NOT EXISTS
FOR (a:Account) REQUIRE a.account_number IS UNIQUE;

CREATE CONSTRAINT unique_bank_bic IF NOT EXISTS
FOR (b:Bank) REQUIRE b.bic IS UNIQUE;

// 2. Indexes for Performance
CREATE INDEX account_risk_idx IF NOT EXISTS
FOR (a:Account) ON (a.risk_score);

CREATE INDEX person_name_idx IF NOT EXISTS
FOR (p:Person) ON (p.name);