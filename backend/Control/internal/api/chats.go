package api

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/0000rpg/Second-Pilot/backend/internal/auth"
	"github.com/0000rpg/Second-Pilot/backend/internal/db"
	"github.com/go-chi/chi/v5"
)

type chatResponse struct {
	ID        int64           `json:"id"`
	UserID    int64           `json:"user_id"`
	Name      string          `json:"name"`
	Messages  json.RawMessage `json:"messages"`
	CreatedAt string          `json:"created_at"`
	UpdatedAt string          `json:"updated_at"`
}

type createChatRequest struct {
	Name string `json:"name"`
}

type updateChatRequest struct {
	Name     string          `json:"name"`
	Messages json.RawMessage `json:"messages"`
}

func chatToResponse(c *db.Chat) chatResponse {
	msgs := c.Messages
	if msgs == nil {
		msgs = json.RawMessage("[]")
	}
	return chatResponse{
		ID:        c.ID,
		UserID:    c.UserID,
		Name:      c.Name,
		Messages:  msgs,
		CreatedAt: c.CreatedAt.UTC().Format("2006-01-02T15:04:05Z"),
		UpdatedAt: c.UpdatedAt.UTC().Format("2006-01-02T15:04:05Z"),
	}
}

func getUserID(r *http.Request) int64 {
	claims := r.Context().Value(claimsKey).(*auth.Claims)
	return claims.UserID
}

func HandlerGetChats(w http.ResponseWriter, r *http.Request) {
	userID := getUserID(r)

	chats, err := db.GetChatsByUserID(userID)
	if err != nil {
		writeJsonError(w, "internal server error", http.StatusInternalServerError)
		return
	}

	result := make([]chatResponse, 0, len(chats))
	for _, c := range chats {
		result = append(result, chatToResponse(c))
	}

	writeJson(w, map[string]any{"ok": true, "chats": result}, http.StatusOK)
}

func HandlerGetChat(w http.ResponseWriter, r *http.Request) {
	userID := getUserID(r)

	idStr := chi.URLParam(r, "id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		writeJsonError(w, "invalid chat id", http.StatusBadRequest)
		return
	}

	chat, err := db.GetChatByID(id, userID)
	if err != nil {
		if err == sql.ErrNoRows {
			writeJsonError(w, "chat not found", http.StatusNotFound)
			return
		}
		writeJsonError(w, "internal server error", http.StatusInternalServerError)
		return
	}

	writeJson(w, map[string]any{"ok": true, "chat": chatToResponse(chat)}, http.StatusOK)
}

func HandlerCreateChat(w http.ResponseWriter, r *http.Request) {
	userID := getUserID(r)

	var data createChatRequest
	if err := json.NewDecoder(r.Body).Decode(&data); err != nil {
		writeJsonError(w, "invalid request body", http.StatusBadRequest)
		return
	}

	name := data.Name
	if name == "" {
		name = "Новый чат"
	}

	chat, err := db.CreateChat(userID, name)
	if err != nil {
		writeJsonError(w, "internal server error", http.StatusInternalServerError)
		return
	}

	writeJson(w, map[string]any{"ok": true, "chat": chatToResponse(chat)}, http.StatusCreated)
}

func HandlerUpdateChat(w http.ResponseWriter, r *http.Request) {
	userID := getUserID(r)

	idStr := chi.URLParam(r, "id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		writeJsonError(w, "invalid chat id", http.StatusBadRequest)
		return
	}

	var data updateChatRequest
	if err := json.NewDecoder(r.Body).Decode(&data); err != nil {
		writeJsonError(w, "invalid request body", http.StatusBadRequest)
		return
	}

	if data.Name == "" {
		writeJsonError(w, "name is required", http.StatusBadRequest)
		return
	}

	messages := data.Messages
	if messages == nil {
		messages = json.RawMessage("[]")
	}

	if err := db.UpdateChat(id, userID, data.Name, messages); err != nil {
		writeJsonError(w, "internal server error", http.StatusInternalServerError)
		return
	}

	writeJson(w, map[string]any{"ok": true}, http.StatusOK)
}

func HandlerDeleteChat(w http.ResponseWriter, r *http.Request) {
	userID := getUserID(r)

	idStr := chi.URLParam(r, "id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		writeJsonError(w, "invalid chat id", http.StatusBadRequest)
		return
	}

	if err := db.DeleteChat(id, userID); err != nil {
		writeJsonError(w, "internal server error", http.StatusInternalServerError)
		return
	}

	writeJson(w, map[string]any{"ok": true}, http.StatusOK)
}
