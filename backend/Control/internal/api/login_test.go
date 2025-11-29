package api

import (
	"strconv"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestJWTToken(t *testing.T) {
	usersID := []int{
		0,
		-1,
		123,
	}

	for _, userId := range usersID {
		token, err := generateToken(userId)
		require.NoError(t, err, "generate jwt token error")

		jwtToken, err := parseToken(token)
		require.NoError(t, err, "parse jwt token error")
		assert.True(t, jwtToken.Valid, "invalid jwt token")

		sub, err := jwtToken.Claims.GetSubject()
		require.NoError(t, err, "get subject error")

		subInt, err := strconv.Atoi(sub)
		require.NoError(t, err, "parse subject error")
		assert.Equal(t, userId, subInt, "wrong subject")

		exp, err := jwtToken.Claims.GetExpirationTime()
		require.NoError(t, err, "get subject error")
		require.True(t, exp.After(time.Now()), "expired token")
	}
}