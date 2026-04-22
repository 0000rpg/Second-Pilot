package api

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"os"
	"strings"

	"github.com/0000rpg/Second-Pilot/backend/internal/auth"
	"github.com/0000rpg/Second-Pilot/backend/internal/db"
	"golang.org/x/crypto/bcrypt"
)

type authRequest struct {
	Login    string `json:"login"`
	Password string `json:"password"`
}

type authResponse struct {
	OK       bool   `json:"ok"`
	Token    string `json:"token"`
	Username string `json:"username"`
}

func HandlerRegister(w http.ResponseWriter, req *http.Request) {
	var data authRequest
	if err := json.NewDecoder(req.Body).Decode(&data); err != nil {
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

	secret := os.Getenv("JWT_SECRET")
	token, err := auth.GenerateToken(id, data.Login, secret)
	if err != nil {
		writeJsonError(w, "internal server error", http.StatusInternalServerError)
		return
	}

	writeJson(w, authResponse{OK: true, Token: token, Username: data.Login}, http.StatusCreated)
}

func HandlerVerify(w http.ResponseWriter, req *http.Request) {
	authHeader := req.Header.Get("Authorization")
	if !strings.HasPrefix(authHeader, "Bearer ") {
		writeJsonError(w, "missing or invalid authorization header", http.StatusUnauthorized)
		return
	}

	tokenString := strings.TrimPrefix(authHeader, "Bearer ")
	secret := os.Getenv("JWT_SECRET")
	claims, err := auth.ValidateToken(tokenString, secret)
	if err != nil {
		writeJsonError(w, "invalid or expired token", http.StatusUnauthorized)
		return
	}

	writeJson(w, authResponse{OK: true, Token: tokenString, Username: claims.Username}, http.StatusOK)
}

func HandlerLogin(w http.ResponseWriter, req *http.Request) {
	var data authRequest
	if err := json.NewDecoder(req.Body).Decode(&data); err != nil {
		writeJsonError(w, "invalid request body", http.StatusBadRequest)
		return
	}

	if data.Login == "" || data.Password == "" {
		writeJsonError(w, "login and password are required", http.StatusBadRequest)
		return
	}

	user, err := db.FindUserByUsername(data.Login)
	if err == sql.ErrNoRows || user == nil {
		writeJsonError(w, "invalid username or password", http.StatusUnauthorized)
		return
	}
	if err != nil {
		writeJsonError(w, "internal server error", http.StatusInternalServerError)
		return
	}

	if err := bcrypt.CompareHashAndPassword([]byte(user.PasswordHash), []byte(data.Password)); err != nil {
		writeJsonError(w, "invalid username or password", http.StatusUnauthorized)
		return
	}

	secret := os.Getenv("JWT_SECRET")
	token, err := auth.GenerateToken(user.ID, user.Username, secret)
	if err != nil {
		writeJsonError(w, "internal server error", http.StatusInternalServerError)
		return
	}

	writeJson(w, authResponse{OK: true, Token: token, Username: user.Username}, http.StatusOK)
}
