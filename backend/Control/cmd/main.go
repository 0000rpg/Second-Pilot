package main

import (
	"fmt"
	"net/http"

	"github.com/go-chi/chi/v5"
)

func main() {
	r := chi.NewRouter()

	err := http.ListenAndServe(":80", r)
	if (err != nil) {
		fmt.Printf("Listen and serve server error: %s\n", err.Error())
	}
}