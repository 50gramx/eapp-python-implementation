-- Alter the Universe table to comply with the code

ALTER TABLE universe
RENAME COLUMN universe_big_bang_at TO universe_created_at;

ALTER TABLE universe
ADD COLUMN universe_updated_at TIMESTAMP;
