package api

import (
	"bytes"
	"encoding/json"
	"net/http"
)

type authData struct {
	Login 		string `json:"login"`
	Password 	string `json:"password"`
}

func HandlerAuth(w http.ResponseWriter, req *http.Request) {
	var (
		buf bytes.Buffer
		data authData
	)

	_, err := buf.ReadFrom(req.Body)

	if err != nil {
		writeJsonError(w, err.Error(), http.StatusBadRequest);
	}

	err = json.Unmarshal(buf.Bytes(), &data)

	if err != nil {
		writeJsonError(w, err.Error(), http.StatusBadRequest);
	}

	
}

func auth(http.HandlerFunc) func(http.ResponseWriter, *http.Request) {
	return func(w http.ResponseWriter, req *http.Request) {
		
	}
}