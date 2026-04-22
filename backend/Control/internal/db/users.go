package db

import "fmt"

type User struct {
	ID           int64
	Username     string
	PasswordHash string
}

func GetAllUsers() ([]*User, error) {
	if db == nil {
		return nil, fmt.Errorf("database not initialized")
	}

	rows, err := db.Query(`SELECT id, username FROM users ORDER BY id`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var users []*User
	for rows.Next() {
		u := &User{}
		if err := rows.Scan(&u.ID, &u.Username); err != nil {
			return nil, err
		}
		users = append(users, u)
	}
	return users, nil
}

func DeleteUser(id int64) error {
	if db == nil {
		return fmt.Errorf("database not initialized")
	}
	_, err := db.Exec(`DELETE FROM users WHERE id = $1`, id)
	return err
}

func UpdateUsername(id int64, newUsername string) error {
	if db == nil {
		return fmt.Errorf("database not initialized")
	}
	_, err := db.Exec(`UPDATE users SET username = $1 WHERE id = $2`, newUsername, id)
	return err
}

func CreateUser(username, passwordHash string) (int64, error) {
	if db == nil {
		return 0, fmt.Errorf("database not initialized")
	}

	var id int64
	err := db.QueryRow(
		`INSERT INTO users (username, password_hash) VALUES ($1, $2) RETURNING id`,
		username, passwordHash,
	).Scan(&id)

	if err != nil {
		return 0, err
	}

	return id, nil
}

func FindUserByUsername(username string) (*User, error) {
	if db == nil {
		return nil, fmt.Errorf("database not initialized")
	}

	user := &User{}
	err := db.QueryRow(
		`SELECT id, username, password_hash FROM users WHERE username = $1`,
		username,
	).Scan(&user.ID, &user.Username, &user.PasswordHash)

	if err != nil {
		return nil, err
	}

	return user, nil
}
