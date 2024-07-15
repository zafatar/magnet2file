# Makefile for magnet2file

# Variables
CC = gcc
CFLAGS = -Wall -Wextra
TARGET = magnet2file

# Default target
all: $(TARGET)

# Build target
$(TARGET): main.c
	$(CC) $(CFLAGS) -o $@ $^

# Clean target
clean:
	echo -e "Cleaning..."

# Help target
help:
	@echo "Available targets:"
	@echo "  all     : Build the $(TARGET) executable"
	@echo "  clean   : Remove the $(TARGET) executable"
	@echo "  help    : Show this help message"

.PHONY: all clean help