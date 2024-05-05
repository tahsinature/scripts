package main

import (
	"fmt"
	"os"
)

func main() {
	fmt.Println("FROM GO")
	printAllEnvVars()	
}

func printEnvVars(variable string) {
	fmt.Println("Value of", variable, "is", os.Getenv(variable))
}

func printAllEnvVars() {
	for _, env := range os.Environ() {
		fmt.Println(env)
	}
}