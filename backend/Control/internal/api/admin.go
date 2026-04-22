package api

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/0000rpg/Second-Pilot/backend/internal/db"
	"github.com/go-chi/chi/v5"
	"golang.org/x/crypto/bcrypt"
)

type userResponse struct {
	ID       int64  `json:"id"`
	Username string `json:"username"`
}

type createUserRequest struct {
	Login    string `json:"login"`
	Password string `json:"password"`
}

type renameUserRequest struct {
	Login string `json:"login"`
}

func HandlerGetUsers(w http.ResponseWriter, r *http.Request) {
	users, err := db.GetAllUsers()
	if err != nil {
		writeJsonError(w, "internal server error", http.StatusInternalServerError)
		return
	}

	result := make([]userResponse, 0, len(users))
	for _, u := range users {
		result = append(result, userResponse{ID: u.ID, Username: u.Username})
	}

	writeJson(w, map[string]any{"ok": true, "users": result}, http.StatusOK)
}

func HandlerCreateUser(w http.ResponseWriter, r *http.Request) {
	var data createUserRequest
	if err := json.NewDecoder(r.Body).Decode(&data); err != nil {
		writeJsonError(w, "invalid request body", http.StatusBadRequest)
		return
	}

	if data.Login == "" || data.Password == "" {
		writeJsonError(w, "login and password are required", http.StatusBadRequest)
		return
	}

	existing, err := db.FindUserByUsername(data.Login)
	if err != nil && err != sql.ErrNoRows {
		writeJsonError(w, "internal server error", http.StatusInternalServerError)
		return
	}
	if existing != nil {
		writeJsonError(w, "username already taken", http.StatusConflict)
		return
	}

	hash, err := bcrypt.GenerateFromPassword([]byte(data.Password), bcrypt.DefaultCost)
	if err != nil {
		writeJsonError(w, "internal server error", http.StatusInternalServerError)
		return
	}

	id, err := db.CreateUser(data.Login, string(hash))
	if err != nil {
		writeJsonError(w, "internal server error", http.StatusInternalServerError)
		return
	}

	writeJson(w, map[string]any{"ok": true, "user": userResponse{ID: id, Username: data.Login}}, http.StatusCreated)
}

func HandlerRenameUser(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		writeJsonError(w, "invalid user id", http.StatusBadRequest)
		return
	}

	var data renameUserRequest
	if err := json.NewDecoder(r.Body).Decode(&data); err != nil {
		writeJsonError(w, "invalid request body", http.StatusBadRequest)
		return
	}

	if data.Login == "" {
		writeJsonError(w, "login is required", http.StatusBadRequest)
		return
	}

	existing, err := db.FindUserByUsername(data.Login)
	if err != nil && err != sql.ErrNoRows {
		writeJsonError(w, "internal server error", http.StatusInternalServerError)
		return
	}
	if existing != nil && existing.ID != id {
		writeJsonError(w, "username already taken", http.StatusConflict)
		return
	}

	if err := db.UpdateUsername(id, data.Login); err != nil {
		writeJsonError(w, "internal server error", http.StatusInternalServerError)
		return
	}

	writeJson(w, map[string]any{"ok": true}, http.StatusOK)
}

func HandlerDeleteUser(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		writeJsonError(w, "invalid user id", http.StatusBadRequest)
		return
	}

	if err := db.DeleteUser(id); err != nil {
		writeJsonError(w, "internal server error", http.StatusInternalServerError)
		return
	}

	writeJson(w, map[string]any{"ok": true}, http.StatusOK)
}
