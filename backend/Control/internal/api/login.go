package api

import (
	"bytes"
	"encoding/json"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

type authData struct {
	Login 		string `json:"login"`
	Password 	string `json:"password"`
}

var secretKey = []byte(os.Getenv("JWT_KEY"))

func HandlerAuth(w http.ResponseWriter, req *http.Request) {
	var (
		buf bytes.Buffer
		data authData
	)

	_, err := buf.ReadFrom(req.Body)

	if err != nil {
		writeJsonError(w, err.Error(), http.StatusBadRequest)
		return
	}

	err = json.Unmarshal(buf.Bytes(), &data)

	if err != nil {
		writeJsonError(w, err.Error(), http.StatusBadRequest)
		return
	}

	var ( 
		check = false
		userID int
	)

	// ПРОВЕРКА, bcrypt
	check = true
	userID = 0

	if !check {
		writeJsonError(w, "wrong login or password", http.StatusBadRequest)
		return
	}

	token, err := generateToken(userID)

	if err != nil {
		writeJsonError(w, "failed creating token", http.StatusBadRequest)
		return
	}

	writeJson(
		w, 
		map[string]any {
			"ok": true,
			"token": token,
		},
		http.StatusOK,
	)
}

func generateToken(userID int) (string, error) {
	claims := jwt.RegisteredClaims {
		Subject: strconv.Itoa(userID),
		ExpiresAt: jwt.NewNumericDate(time.Now().AddDate(0,0,1)),
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(secretKey)
}

func parseToken(token string) (*jwt.Token, error) {
	return jwt.Parse(token, func(*jwt.Token) (interface{}, error) {
		return secretKey, nil
	})
}

func auth(handler http.HandlerFunc) func(http.ResponseWriter, *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		authHeader := r.Header.Get("Authorization")

		if authHeader == "" {
			writeJsonError(w, "unauthorized", http.StatusUnauthorized)
			return
		}

		token := strings.TrimPrefix(authHeader, "Bearer ")
		jwtToken, err := parseToken(token)

		if err != nil {
			writeJsonError(w, "failed to parse token", http.StatusUnauthorized)
			return
		}

		if !jwtToken.Valid {
			writeJsonError(w, "token is invalid", http.StatusUnauthorized)
			return
		}

		claims, ok := jwtToken.Claims.(jwt.MapClaims)

		if !ok {
			writeJsonError(w, "failed casting claims", http.StatusUnauthorized)
			return
		}

		user_id, err := claims.GetSubject()

		if err != nil {
			writeJsonError(w, "failed getting subject from token", http.StatusUnauthorized)
			return
		}

		exp, err := claims.GetExpirationTime()
		
		if err != nil {
			writeJsonError(w, "failed getting expiration time from token", http.StatusUnauthorized)
			return
		}

		if exp.Before(time.Now()) {
			writeJsonError(w, "token expires", http.StatusUnauthorized)
			return
		}

		r.Header.Add("user_id", user_id)
		
		handler(w, r)
	}
}
