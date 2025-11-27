package main

import (
	"fmt"
	"net/http"
	"os"

	"github.com/0000rpg/Second-Pilot/backend/internal/api"
	"github.com/0000rpg/Second-Pilot/backend/internal/db"
	"github.com/go-chi/chi/v5"
)

func main() {
	dbdata := db.ConnData{
		Host: "database",
		Port: 5432,
		User: os.Getenv("DB_USER"),
		Password: os.Getenv("DB_PASSWORD"),
		DBname: os.Getenv("DB_NAME"),
	}

	err := db.Init(dbdata)

	if err != nil {
		fmt.Printf("Connect database error: %s\n", err.Error())
		return
	}

	r := chi.NewRouter()

	r.Route("/api", api.Init)

	fmt.Println("Server start")

	err = http.ListenAndServe(":80", r)
	
	if (err != nil) {
		fmt.Printf("Listen and serve server error: %s\n", err.Error())
		return
	}
}