package db

import (
	"database/sql"
	"fmt"
	"os"
	"path/filepath"
	"sort"

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

func RunMigrations(migrationsDir string) error {
	entries, err := os.ReadDir(migrationsDir)
	if err != nil {
		return fmt.Errorf("read migrations dir: %w", err)
	}

	var files []string
	for _, e := range entries {
		if !e.IsDir() && filepath.Ext(e.Name()) == ".sql" {
			files = append(files, filepath.Join(migrationsDir, e.Name()))
		}
	}
	sort.Strings(files)

	for _, f := range files {
		sql, err := os.ReadFile(f)
		if err != nil {
			return fmt.Errorf("read migration %s: %w", f, err)
		}
		if _, err = db.Exec(string(sql)); err != nil {
			return fmt.Errorf("exec migration %s: %w", f, err)
		}
	}

	return nil
}