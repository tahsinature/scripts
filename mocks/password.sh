#!/bin/sh

no_pass=false

# Check if the --no-pass flag is provided
while [ "$#" -gt 0 ]; do
  case "$1" in
    --no-pass)
      no_pass=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

if [ "$no_pass" = "true" ]; then
    # Output the string without asking for a password
    echo "Token: test"
else
    # Prompt the user for a password
    echo "Enter password:"
    stty -echo
    read -r password
    stty echo
    echo

    # Check if the entered password is valid (e.g., "1234")
    if [ "$password" = "1234" ]; then
        echo "verifying..." && sleep 10
        echo "Token: test"
    else
        echo "Error: Invalid password"
    fi
fi
