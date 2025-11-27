package db

import (
	"database/sql"
	"fmt"

	_ "github.com/lib/pq"
)

var db *sql.DB

type ConnData struct {
	Host 		string
	Port 		int
	User 		string
	Password 	string
	DBname		string
}

func Init(data ConnData) error {
	var err error

	connStr := fmt.Sprintf(
		"host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		data.Host,
		data.Port,
		data.User,
		data.Password,
		data.DBname,
	)

	db, err = sql.Open("postgres", connStr)

	if err != nil {
		return err
	}

	return nil
}

func Close() error {
	err := db.Close()

	return err
}

func checkConnection() bool {
	err := db.Ping()

	return err == nil
}