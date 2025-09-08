-- Initialize the BookWise database
CREATE DATABASE IF NOT EXISTS bookwise CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE bookwise;

-- Grant privileges to the bookwise user
GRANT ALL PRIVILEGES ON bookwise.* TO 'bookwise_user'@'%';
FLUSH PRIVILEGES;