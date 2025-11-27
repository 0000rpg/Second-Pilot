FROM golang:1.25 AS builder

WORKDIR /usr/src/app

# pre-copy/cache go.mod for pre-downloading dependencies and only redownloading them in subsequent builds if they change
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -v -o /app/ ./cmd

FROM scratch AS runner

COPY --from=builder /app/cmd /server

EXPOSE 80

CMD ["/server"]
