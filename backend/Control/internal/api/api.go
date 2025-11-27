package api

import (
	"encoding/json"
	"net/http"

	"github.com/go-chi/chi/v5"
)

func Init(r chi.Router) {
	r.Post("/auth", HandlerAuth)
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
			"ok": false,
			"error": err,
		}, 
		code,
	)
}