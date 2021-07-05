CREATE TABLE IF NOT EXISTS events(
    id INT AUTO_INCREMENT PRIMARY KEY,
    event VARCHAR(100),
    date DATE
);

INSERT INTO events(event, date) VALUES ('start_date', current_date);
INSERT INTO events(event, date) VALUES ('last_update', null);
