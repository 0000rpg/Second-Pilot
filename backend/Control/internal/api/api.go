package api

import (
	"encoding/json"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/cors"
)

func Init(r chi.Router) {
	r.Use(cors.Handler(cors.Options{
		AllowedOrigins: []string{"http://localhost:5173"},
		AllowedMethods: []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowedHeaders: []string{"Content-Type", "Authorization"},
	}))

	r.Post("/auth/register", HandlerRegister)
	r.Post("/auth/login", HandlerLogin)
	r.Get("/auth/verify", HandlerVerify)

	r.Group(func(r chi.Router) {
		r.Use(AuthMiddleware)
		r.Get("/admin/users", HandlerGetUsers)
		r.Post("/admin/users", HandlerCreateUser)
		r.Put("/admin/users/{id}", HandlerRenameUser)
		r.Delete("/admin/users/{id}", HandlerDeleteUser)
	})
}

func writeJson(w http.ResponseWriter, data any, code int) {
	jsonData, err := json.Marshal(data)

	if err != nil {
		writeJsonError(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(code)
	w.Write(jsonData)
}

func writeJsonError(w http.ResponseWriter, err string, code int) {
	writeJson(
		w,
		map[string]any{
			"ok":    false,
			"error": err,
		},
		code,
	)
}
