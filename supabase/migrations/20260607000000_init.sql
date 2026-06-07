-- CENet initial schema migration
-- Generated from backend/models.py (SQLAlchemy → PostgreSQL)

-- =====================
-- Independent tables
-- =====================

CREATE TABLE IF NOT EXISTS users (
    id                  SERIAL PRIMARY KEY,
    email               TEXT UNIQUE NOT NULL,
    password            TEXT,
    role                TEXT,
    auth_provider       TEXT DEFAULT 'local',
    provider_sub        TEXT,
    full_name           TEXT,
    province            TEXT,
    user_type           TEXT,
    ateco_sector        TEXT,
    email_confirmed     BOOLEAN DEFAULT FALSE,
    created_at          TIMESTAMP DEFAULT NOW(),
    last_login_at       TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_users_id    ON users (id);
CREATE INDEX IF NOT EXISTS ix_users_email ON users (email);

-- ----------------------

CREATE TABLE IF NOT EXISTS suppliers (
    id          SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    category    TEXT NOT NULL,
    province    TEXT NOT NULL,
    description TEXT,
    verified    BOOLEAN DEFAULT FALSE,
    plan_tier   TEXT NOT NULL DEFAULT 'free'
);

CREATE INDEX IF NOT EXISTS ix_suppliers_id ON suppliers (id);

-- ----------------------

CREATE TABLE IF NOT EXISTS gse_incentive_parameters (
    id              SERIAL PRIMARY KEY,
    name            TEXT NOT NULL,
    tariff_eur_kwh  DOUBLE PRECISION NOT NULL,
    description     TEXT,
    valid_from      TIMESTAMP,
    valid_to        TIMESTAMP,
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_gse_incentive_parameters_id ON gse_incentive_parameters (id);

-- ----------------------

CREATE TABLE IF NOT EXISTS calculation_parameters (
    id              SERIAL PRIMARY KEY,
    parameter_name  TEXT UNIQUE NOT NULL,
    parameter_value DOUBLE PRECISION NOT NULL,
    unit            TEXT,
    description     TEXT,
    updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_calculation_parameters_id ON calculation_parameters (id);

-- ----------------------

CREATE TABLE IF NOT EXISTS newsletter_subscribers (
    id                  SERIAL PRIMARY KEY,
    name                TEXT,
    email               TEXT UNIQUE NOT NULL,
    user_type           TEXT,
    preferences         JSONB,
    is_active           BOOLEAN DEFAULT TRUE,
    unsubscribe_token   TEXT UNIQUE NOT NULL,
    created_at          TIMESTAMP DEFAULT NOW(),
    unsubscribed_at     TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_newsletter_subscribers_id    ON newsletter_subscribers (id);
CREATE INDEX IF NOT EXISTS ix_newsletter_subscribers_email ON newsletter_subscribers (email);

-- ----------------------

CREATE TABLE IF NOT EXISTS subscription_contacts (
    id          SERIAL PRIMARY KEY,
    email       TEXT NOT NULL,
    name        TEXT,
    message     TEXT,
    source      TEXT DEFAULT 'website',
    status      TEXT NOT NULL DEFAULT 'new',
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_subscription_contacts_id    ON subscription_contacts (id);
CREATE INDEX IF NOT EXISTS ix_subscription_contacts_email ON subscription_contacts (email);

-- ----------------------

CREATE TABLE IF NOT EXISTS api_performance_logs (
    id            SERIAL PRIMARY KEY,
    endpoint      TEXT NOT NULL,
    method        TEXT NOT NULL,
    status_code   INTEGER NOT NULL,
    response_time DOUBLE PRECISION NOT NULL,
    timestamp     TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_api_performance_logs_id ON api_performance_logs (id);

-- =====================
-- Tables referencing users
-- =====================

CREATE TABLE IF NOT EXISTS match_requests (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    province    TEXT NOT NULL,
    need_type   TEXT NOT NULL,
    message     TEXT,
    status      TEXT NOT NULL DEFAULT 'pending',
    created_at  TIMESTAMP DEFAULT NOW(),
    closed_at   TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_match_requests_id ON match_requests (id);

-- ----------------------

CREATE TABLE IF NOT EXISTS simulations (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    simulation_type TEXT NOT NULL,
    title           TEXT NOT NULL,
    input_data      TEXT NOT NULL,
    result_data     TEXT,
    status          TEXT NOT NULL DEFAULT 'completed',
    created_at      TIMESTAMP DEFAULT NOW(),
    completed_at    TIMESTAMP,
    execution_time  DOUBLE PRECISION
);

CREATE INDEX IF NOT EXISTS ix_simulations_id ON simulations (id);

-- ----------------------

CREATE TABLE IF NOT EXISTS energy_communities (
    id              SERIAL PRIMARY KEY,
    community_code  TEXT UNIQUE,
    name            TEXT NOT NULL,
    province        TEXT NOT NULL,
    region          TEXT,
    description     TEXT,
    status          TEXT NOT NULL DEFAULT 'draft',
    manager_id      INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_energy_communities_id             ON energy_communities (id);
CREATE INDEX IF NOT EXISTS ix_energy_communities_community_code ON energy_communities (community_code);

-- ----------------------

CREATE TABLE IF NOT EXISTS contact_requests (
    id           SERIAL PRIMARY KEY,
    user_id      INTEGER NOT NULL REFERENCES users (id)     ON DELETE CASCADE,
    supplier_id  INTEGER NOT NULL REFERENCES suppliers (id) ON DELETE CASCADE,
    message      TEXT NOT NULL,
    status       TEXT NOT NULL DEFAULT 'pending',
    created_at   TIMESTAMP DEFAULT NOW(),
    responded_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_contact_requests_id ON contact_requests (id);

-- ----------------------

CREATE TABLE IF NOT EXISTS community_members (
    id           SERIAL PRIMARY KEY,
    community_id INTEGER NOT NULL REFERENCES energy_communities (id) ON DELETE CASCADE,
    user_id      INTEGER NOT NULL REFERENCES users (id)              ON DELETE CASCADE,
    member_role  TEXT NOT NULL DEFAULT 'member',
    pod_id       TEXT,
    status       TEXT NOT NULL DEFAULT 'active',
    joined_at    TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_community_members_id ON community_members (id);

-- ----------------------

CREATE TABLE IF NOT EXISTS event_logs (
    id          SERIAL PRIMARY KEY,
    event_type  TEXT NOT NULL,
    user_id     INTEGER REFERENCES users (id) ON DELETE SET NULL,
    details     JSONB,
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_event_logs_id         ON event_logs (id);
CREATE INDEX IF NOT EXISTS ix_event_logs_event_type ON event_logs (event_type);

-- ----------------------

CREATE TABLE IF NOT EXISTS module_usage (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER REFERENCES users (id) ON DELETE SET NULL,
    module_name TEXT NOT NULL,
    action      TEXT NOT NULL,
    details     JSONB,
    timestamp   TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_module_usage_id          ON module_usage (id);
CREATE INDEX IF NOT EXISTS ix_module_usage_module_name ON module_usage (module_name);

-- ----------------------

CREATE TABLE IF NOT EXISTS error_logs (
    id            SERIAL PRIMARY KEY,
    user_id       INTEGER REFERENCES users (id) ON DELETE SET NULL,
    module        TEXT,
    endpoint      TEXT,
    error_type    TEXT NOT NULL,
    error_message TEXT,
    timestamp     TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_error_logs_id ON error_logs (id);

-- ----------------------

CREATE TABLE IF NOT EXISTS rec_energy_uploads (
    id                SERIAL PRIMARY KEY,
    community_id      INTEGER NOT NULL REFERENCES energy_communities (id) ON DELETE CASCADE,
    uploaded_by       INTEGER REFERENCES users (id) ON DELETE SET NULL,
    filename          TEXT NOT NULL,
    file_type         TEXT NOT NULL,
    period_start      TIMESTAMP,
    period_end        TIMESTAMP,
    status            TEXT NOT NULL DEFAULT 'uploaded',
    validation_errors JSONB,
    created_at        TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_rec_energy_uploads_id ON rec_energy_uploads (id);

-- ----------------------

CREATE TABLE IF NOT EXISTS personal_energy_uploads (
    id                SERIAL PRIMARY KEY,
    user_id           INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    filename          TEXT NOT NULL,
    file_type         TEXT NOT NULL,
    period_start      TIMESTAMP,
    period_end        TIMESTAMP,
    status            TEXT NOT NULL DEFAULT 'uploaded',
    validation_errors JSONB,
    created_at        TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_personal_energy_uploads_id ON personal_energy_uploads (id);

-- ----------------------

CREATE TABLE IF NOT EXISTS manual_energy_inputs (
    id                      SERIAL PRIMARY KEY,
    user_id                 INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    annual_consumption_kwh  DOUBLE PRECISION NOT NULL,
    system_power_kw         DOUBLE PRECISION,
    province                TEXT,
    created_at              TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_manual_energy_inputs_id ON manual_energy_inputs (id);

-- ----------------------

CREATE TABLE IF NOT EXISTS energy_prices (
    id           SERIAL PRIMARY KEY,
    community_id INTEGER REFERENCES energy_communities (id) ON DELETE CASCADE,
    price_eur_kwh DOUBLE PRECISION NOT NULL,
    valid_from   TIMESTAMP NOT NULL,
    valid_to     TIMESTAMP,
    created_by   INTEGER REFERENCES users (id) ON DELETE SET NULL,
    created_at   TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_energy_prices_id ON energy_prices (id);

-- ----------------------

CREATE TABLE IF NOT EXISTS community_costs (
    id                    SERIAL PRIMARY KEY,
    community_id          INTEGER NOT NULL REFERENCES energy_communities (id) ON DELETE CASCADE,
    fixed_management_cost DOUBLE PRECISION NOT NULL DEFAULT 0,
    variable_cost         DOUBLE PRECISION NOT NULL DEFAULT 0,
    created_by            INTEGER REFERENCES users (id) ON DELETE SET NULL,
    created_at            TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_community_costs_id ON community_costs (id);

-- ----------------------

CREATE TABLE IF NOT EXISTS incentive_allocations (
    id               SERIAL PRIMARY KEY,
    community_id     INTEGER NOT NULL REFERENCES energy_communities (id) ON DELETE CASCADE,
    member_user_id   INTEGER NOT NULL REFERENCES users (id)              ON DELETE CASCADE,
    period_start     TIMESTAMP,
    period_end       TIMESTAMP,
    gross_incentive  DOUBLE PRECISION NOT NULL DEFAULT 0,
    cost_share       DOUBLE PRECISION NOT NULL DEFAULT 0,
    net_reimbursement DOUBLE PRECISION NOT NULL DEFAULT 0,
    created_at       TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_incentive_allocations_id ON incentive_allocations (id);

-- =====================
-- Tables referencing uploads
-- =====================

CREATE TABLE IF NOT EXISTS rec_energy_readings (
    id           SERIAL PRIMARY KEY,
    community_id INTEGER NOT NULL REFERENCES energy_communities (id)  ON DELETE CASCADE,
    upload_id    INTEGER NOT NULL REFERENCES rec_energy_uploads (id)  ON DELETE CASCADE,
    pod_id       TEXT,
    reading_date TIMESTAMP NOT NULL,
    kwh_produced DOUBLE PRECISION NOT NULL DEFAULT 0,
    kwh_consumed DOUBLE PRECISION NOT NULL DEFAULT 0,
    kwh_shared   DOUBLE PRECISION NOT NULL DEFAULT 0,
    created_at   TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_rec_energy_readings_id ON rec_energy_readings (id);

-- ----------------------

CREATE TABLE IF NOT EXISTS personal_energy_readings (
    id                SERIAL PRIMARY KEY,
    user_id           INTEGER NOT NULL REFERENCES users (id)                    ON DELETE CASCADE,
    upload_id         INTEGER          REFERENCES personal_energy_uploads (id)  ON DELETE CASCADE,
    pod_id            TEXT,
    reading_date      TIMESTAMP NOT NULL,
    kwh_consumed      DOUBLE PRECISION NOT NULL DEFAULT 0,
    kwh_produced      DOUBLE PRECISION NOT NULL DEFAULT 0,
    kwh_fed_to_grid   DOUBLE PRECISION NOT NULL DEFAULT 0,
    kwh_self_consumed DOUBLE PRECISION NOT NULL DEFAULT 0,
    created_at        TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_personal_energy_readings_id ON personal_energy_readings (id);
