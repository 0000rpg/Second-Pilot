package db

import (
	"encoding/json"
	"fmt"
	"time"
)

type Chat struct {
	ID        int64
	UserID    int64
	Name      string
	Messages  json.RawMessage
	CreatedAt time.Time
	UpdatedAt time.Time
}

func GetChatsByUserID(userID int64) ([]*Chat, error) {
	if db == nil {
		return nil, fmt.Errorf("database not initialized")
	}

	rows, err := db.Query(
		`SELECT id, user_id, name, messages, created_at, updated_at
		 FROM chats WHERE user_id = $1 ORDER BY updated_at DESC`,
		userID,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var chats []*Chat
	for rows.Next() {
		c := &Chat{}
		if err := rows.Scan(&c.ID, &c.UserID, &c.Name, &c.Messages, &c.CreatedAt, &c.UpdatedAt); err != nil {
			return nil, err
		}
		chats = append(chats, c)
	}
	return chats, nil
}

func GetChatByID(id, userID int64) (*Chat, error) {
	if db == nil {
		return nil, fmt.Errorf("database not initialized")
	}

	c := &Chat{}
	err := db.QueryRow(
		`SELECT id, user_id, name, messages, created_at, updated_at
		 FROM chats WHERE id = $1 AND user_id = $2`,
		id, userID,
	).Scan(&c.ID, &c.UserID, &c.Name, &c.Messages, &c.CreatedAt, &c.UpdatedAt)
	if err != nil {
		return nil, err
	}
	return c, nil
}

func CreateChat(userID int64, name string) (*Chat, error) {
	if db == nil {
		return nil, fmt.Errorf("database not initialized")
	}

	c := &Chat{}
	err := db.QueryRow(
		`INSERT INTO chats (user_id, name, messages)
		 VALUES ($1, $2, '[]')
		 RETURNING id, user_id, name, messages, created_at, updated_at`,
		userID, name,
	).Scan(&c.ID, &c.UserID, &c.Name, &c.Messages, &c.CreatedAt, &c.UpdatedAt)
	if err != nil {
		return nil, err
	}
	return c, nil
}

func UpdateChat(id, userID int64, name string, messages json.RawMessage) error {
	if db == nil {
		return fmt.Errorf("database not initialized")
	}

	_, err := db.Exec(
		`UPDATE chats SET name = $1, messages = $2, updated_at = NOW()
		 WHERE id = $3 AND user_id = $4`,
		name, messages, id, userID,
	)
	return err
}

func DeleteChat(id, userID int64) error {
	if db == nil {
		return fmt.Errorf("database not initialized")
	}

	_, err := db.Exec(`DELETE FROM chats WHERE id = $1 AND user_id = $2`, id, userID)
	return err
}

func DeleteAllChatsByUserID(userID int64) error {
	if db == nil {
		return fmt.Errorf("database not initialized")
	}

	_, err := db.Exec(`DELETE FROM chats WHERE user_id = $1`, userID)
	return err
}
