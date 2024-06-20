-- 01-identity-create-tables.sql

-- Universe Table
CREATE TABLE universe
(
    universe_id          VARCHAR(255) PRIMARY KEY,
    universe_name        VARCHAR(255) NOT NULL UNIQUE,
    universe_description VARCHAR(255) NOT NULL,
    universe_created_at TIMESTAMP    NOT NULL,
    universe_updated_at TIMESTAMP
);
-- Galaxy Table
CREATE TABLE galaxy
(
    galaxy_id         VARCHAR(255) PRIMARY KEY,
    galaxy_name       VARCHAR(255)                                   NOT NULL,
    universe_id       VARCHAR(255) REFERENCES universe (universe_id) NOT NULL,
    galaxy_created_at TIMESTAMP                                      NOT NULL
);

-- Account Table
CREATE TABLE account
(
    account_analytics_id      VARCHAR(255) UNIQUE,
    account_id                VARCHAR(255) PRIMARY KEY,
    account_personal_email_id VARCHAR(255) UNIQUE,
    account_work_email_id     VARCHAR(255) UNIQUE,
    account_country_code      VARCHAR(6)                                 NOT NULL,
    account_mobile_number     VARCHAR(10) UNIQUE                         NOT NULL,
    account_first_name        VARCHAR(40)                                NOT NULL,
    account_last_name         VARCHAR(40)                                NOT NULL,
    account_gender            VARCHAR(10)                                NOT NULL,
    account_birth_at          TIMESTAMP                                  NOT NULL,
    account_galaxy_id         VARCHAR(255) REFERENCES galaxy (galaxy_id) NOT NULL,
    account_created_at        TIMESTAMP                                  NOT NULL,
    account_billing_active    BOOLEAN
);


-- AccountDevices Table
CREATE TABLE account_devices
(
    account_id                       VARCHAR(255) PRIMARY KEY REFERENCES account (account_id),
    account_device_os                INTEGER             NOT NULL,
    account_device_token             VARCHAR(255) UNIQUE NOT NULL,
    account_device_token_accessed_at TIMESTAMP           NOT NULL
);

-- AccountSecrets Table
CREATE TABLE account_secrets
(
    account_id                             VARCHAR(255) PRIMARY KEY REFERENCES account (account_id),
    account_password                       VARCHAR(255) NOT NULL,
    account_password_last_updated_geo_lat  VARCHAR(255) NOT NULL,
    account_password_last_updated_geo_long VARCHAR(255) NOT NULL,
    account_password_last_updated_at       TIMESTAMP,
    account_password_created_at            TIMESTAMP    NOT NULL
);

-- AccountConvenienceSecrets Table
CREATE TABLE account_convenience_secrets
(
    account_id                         VARCHAR(255) PRIMARY KEY REFERENCES account (account_id),
    account_convenience_pin            VARCHAR(6) NOT NULL,
    account_convenience_pin_created_at TIMESTAMP  NOT NULL
);


-- Space Table
CREATE TABLE space
(
    space_id                 VARCHAR(255) PRIMARY KEY,
    space_admin_id           VARCHAR(255) REFERENCES account (account_id),
    galaxy_id                VARCHAR(255) REFERENCES galaxy (galaxy_id) NOT NULL,
    space_accessibility_type VARCHAR(255)                               NOT NULL,
    space_isolation_type     VARCHAR(255)                               NOT NULL,
    space_entity_type        VARCHAR(255)                               NOT NULL,
    space_created_at         TIMESTAMP                                  NOT NULL
);

-- AccountAssistant Table
CREATE TABLE account_assistant
(
    account_assistant_id        VARCHAR(255) PRIMARY KEY,
    account_assistant_name_code INTEGER      NOT NULL,
    account_assistant_name      VARCHAR(255) NOT NULL,
    account_id                  VARCHAR(255) REFERENCES account (account_id),
    created_at                  TIMESTAMP    NOT NULL,
    last_assisted_at            TIMESTAMP    NOT NULL
);

-- AccountAssistantNameCode Table
CREATE TABLE account_assistant_name_code
(
    account_assistant_name      VARCHAR(255),
    account_assistant_name_code INTEGER,
    account_id                  VARCHAR(255) REFERENCES account (account_id),
    PRIMARY KEY (account_assistant_name, account_assistant_name_code, account_id)
);

-- CoreCollaborator Table
CREATE TABLE core_collaborator
(
    collaborator_first_name     VARCHAR(255),
    collaborator_last_name      VARCHAR(255),
    collaborator_community_code INTEGER,
    PRIMARY KEY (collaborator_first_name, collaborator_last_name, collaborator_community_code)
);