CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('developer', 'admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE Developer_Profiles (
    developer_id SERIAL PRIMARY KEY,
    user_id INT UNIQUE NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,
    full_name VARCHAR(100) NOT NULL,
    bio TEXT,
    location VARCHAR(100),
    years_experience INT,
    contact_link TEXT,
    avatar_url TEXT
);

CREATE TABLE Skills (
    skill_id SERIAL PRIMARY KEY,
    skill_name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50)
);

CREATE TABLE Projects (
    project_id SERIAL PRIMARY KEY,
    owner_id INT NOT NULL REFERENCES Developer_Profiles(developer_id) ON DELETE CASCADE,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    location VARCHAR(100),
    slots_needed INT DEFAULT 1,
    status VARCHAR(20) DEFAULT 'open' CHECK (status IN ('open', ,'closed','in_progress', 'completed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Developer_Skills (
    developer_id INT REFERENCES Developer_Profiles(developer_id) ON DELETE CASCADE,
    skill_id INT REFERENCES Skills(skill_id) ON DELETE CASCADE,
    proficiency_level VARCHAR(20) CHECK (proficiency_level IN ('beginner', 'intermediate', 'expert')),
    PRIMARY KEY (developer_id, skill_id)
);

CREATE TABLE Project_Skills (
    project_id INT REFERENCES Projects(project_id) ON DELETE CASCADE,
    skill_id INT REFERENCES Skills(skill_id) ON DELETE CASCADE,
    is_required BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (project_id, skill_id)
);

CREATE TABLE Requests (
    request_id SERIAL PRIMARY KEY,
    developer_id INT NOT NULL REFERENCES Developer_Profiles(developer_id) ON DELETE CASCADE,
    project_id INT NOT NULL REFERENCES Projects(project_id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Matches (
    match_id SERIAL PRIMARY KEY,
    developer_id INT NOT NULL REFERENCES Developer_Profiles(developer_id) ON DELETE CASCADE,
    project_id INT NOT NULL REFERENCES Projects(project_id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'completed')),
    matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE TABLE Ratings (
    rating_id SERIAL PRIMARY KEY,
    match_id INT NOT NULL REFERENCES Matches(match_id) ON DELETE CASCADE,
    rater_id INT NOT NULL REFERENCES Developer_Profiles(developer_id) ON DELETE CASCADE,
    rated_id INT NOT NULL REFERENCES Developer_Profiles(developer_id) ON DELETE CASCADE,
    score INT CHECK (score BETWEEN 1 AND 5),
    review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (match_id, rater_id)
);