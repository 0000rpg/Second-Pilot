package main

import (
	"fmt"
	"net/http"

	"github.com/0000rpg/Second-Pilot/backend/internal/api"
	"github.com/go-chi/chi/v5"
)

func main() {
	r := chi.NewRouter()

	r.Route("/api", api.ApiHandlers)

	err := http.ListenAndServe(":80", r)
	if (err != nil) {
		fmt.Printf("Listen and serve server error: %s\n", err.Error())
	}
}